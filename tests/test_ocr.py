import os
import glob
import logging
from PIL import Image
import cv2
import numpy as np
from paddleocr import PaddleOCR

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class OCRTester:
    def __init__(self, screenshot_folder):
        """Initialize with the folder containing screenshots."""
        self.screenshot_folder = screenshot_folder
        # Initialize PaddleOCR with Chinese model
        self.ocr = PaddleOCR(
            use_angle_cls=True,  # Enable angle classification
            lang='ch',  # Chinese (simplified)
            ocr_version='PP-OCRv4',  # Latest model
            rec_char_dict_path=None  # Use default dictionary
        )
        logger.info(f"Initialized OCRTester with screenshot folder: {screenshot_folder}")

    def preprocess_image(self, img):
        """Preprocess image for better OCR accuracy."""
        try:
            # Convert PIL Image to OpenCV format
            img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            # Convert to grayscale
            gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
            # Apply contrast enhancement
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            enhanced = clahe.apply(gray)
            # Binarize image
            _, thresh = cv2.threshold(enhanced, 180, 255, cv2.THRESH_BINARY)
            # Save preprocessed image for debugging
            # debug_path = os.path.join(self.screenshot_folder, f"preprocessed_{os.path.basename(img.filename)}.png")
            # cv2.imwrite(debug_path, thresh)
            return thresh
        except Exception as e:
            logger.error(f"Image preprocessing failed: {e}")
            return None

    def extract_text(self, image_path):
        """Extract text from an image using PaddleOCR."""
        try:
            # Open image
            img = Image.open(image_path)
            # Preprocess
            processed_img = self.preprocess_image(img)
            if processed_img is None:
                return None
            # Convert to RGB for PaddleOCR
            processed_rgb = cv2.cvtColor(processed_img, cv2.COLOR_GRAY2RGB)
            # Perform OCR directly on array to avoid temporary file
            result = self.ocr.ocr(processed_rgb, cls=True)
            # Extract text
            text = ""
            if result and result[0]:
                text = "\n".join([line[1][0] for line in result[0]])
            logger.info(f"Extracted text from {image_path}: {text}")
            return text.strip()
        except Exception as e:
            logger.error(f"OCR failed for {image_path}: {e}")
            return None

    def test_screenshots(self):
        """Test OCR on all screenshots in the folder."""
        screenshot_files = glob.glob(os.path.join(self.screenshot_folder, "*.png"))
        if not screenshot_files:
            logger.warning(f"No screenshots found in {self.screenshot_folder}")
            return

        logger.info(f"Found {len(screenshot_files)} screenshots to test")
        results = []
        for file_path in screenshot_files:
            logger.info(f"Processing {file_path}")
            text = self.extract_text(file_path)
            results.append({
                "file": os.path.basename(file_path),
                "text": text if text else None
            })

        # Save results to JSON
        import json
        output_path = os.path.join(self.screenshot_folder, "ocr_results.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        logger.info(f"Saved OCR results to {output_path}")

        # Log summary
        logger.info("\n=== OCR Test Summary ===")
        for result in results:
            text_preview = (result["text"][:50] + "...") if result["text"] else "None"
            logger.info(f"File: {result['file']}, Text: {text_preview}")

def main():
    """Run the OCR test."""
    try:
        screenshot_folder = os.path.dirname(os.path.abspath(__file__))
        if not os.path.exists(screenshot_folder):
            logger.error(f"Screenshot folder {screenshot_folder} does not exist")
            return

        tester = OCRTester(screenshot_folder)
        tester.test_screenshots()
    except Exception as e:
        logger.error(f"Test failed: {e}")

if __name__ == "__main__":
    main()