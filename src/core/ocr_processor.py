import cv2
import numpy as np
from typing import Optional
from PIL import Image
from paddleocr import PaddleOCR
from utils.logger import LOGGER
import json
import os
from datetime import datetime

class OCRProcessor:
    def __init__(self, output_dir: str, lang: str = "ch"):
        """Initialize OCRProcessor with output directory for JSON results.

        Args:
            output_dir (str): Directory to save ocr_results.json.
            lang (str): Language for OCR (default: 'ch' for Chinese).
        """
        self.output_dir = output_dir
        self.ocr = PaddleOCR(
            use_angle_cls=True,  # Enable angle classification
            lang=lang,  # Language for OCR
            ocr_version='PP-OCRv4',  # Latest model
            rec_char_dict_path=None  # Use default dictionary
        )
        self.json_path = os.path.join(output_dir, "ocr_results.json")
        os.makedirs(output_dir, exist_ok=True)
        LOGGER.info(f"Initialized OCRProcessor with output_dir: {output_dir}")

    def preprocess_image(self, img: Image.Image) -> Optional[np.ndarray]:
        """Preprocess image for better OCR accuracy.

        Args:
            img (Image): PIL Image to preprocess.

        Returns:
            np.ndarray: Preprocessed image array, or None if failed.
        """
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
            return thresh
        except Exception as e:
            LOGGER.error(f"Image preprocessing failed: {e}")
            return None

    def extract_text(self, image: Image.Image, filename: Optional[str] = None) -> Optional[str]:
        """Extract text from a single image using PaddleOCR and append to JSON.

        Args:
            image (Image): PIL Image to process.
            filename (str, optional): Name for the image in JSON output. If None, generates a timestamp-based name.

        Returns:
            str: Extracted text, or None if failed.
        """
        try:
            # Generate filename if not provided
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"screenshot_{timestamp}.png"

            # Preprocess image
            processed_img = self.preprocess_image(image)
            if processed_img is None:
                return None

            # Convert to RGB for PaddleOCR
            processed_rgb = cv2.cvtColor(processed_img, cv2.COLOR_GRAY2RGB)
            # Perform OCR
            result = self.ocr.ocr(processed_rgb, cls=True)
            # Extract text
            text = ""
            if result and result[0]:
                text = "\n".join([line[1][0] for line in result[0]])
            LOGGER.info(f"Extracted text from {filename}: {text}")

            # Append result to JSON
            self._append_to_json(filename, text)
            return text.strip() if text else None
        except Exception as e:
            LOGGER.error(f"OCR failed for {filename}: {e}")
            return None

    def _append_to_json(self, filename: str, text: str):
        """Append OCR result to ocr_results.json.

        Args:
            filename (str): Name of the image file.
            text (str): Extracted text.
        """
        try:
            # Load existing results
            results = []
            if os.path.exists(self.json_path):
                with open(self.json_path, "r", encoding="utf-8") as f:
                    results = json.load(f)
            # Append new result
            results.append({
                "file": filename,
                "text": text if text else None
            })
            # Write back to JSON
            with open(self.json_path, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            LOGGER.info(f"Appended OCR result to {self.json_path}")
        except Exception as e:
            LOGGER.error(f"Failed to append to JSON: {e}")