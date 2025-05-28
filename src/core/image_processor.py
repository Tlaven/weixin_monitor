# 图像编码与处理

import base64
from typing import Optional
from PIL import Image
from utils.logger import LOGGER

class ImageProcessor:
    def encode_image(self, image: Image.Image) -> Optional[str]:
        """将图像编码为base64"""
        try:
            from io import BytesIO
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            encoded = base64.b64encode(buffered.getvalue()).decode("utf-8")
            LOGGER.debug("Encoded image to base64")
            return encoded
        except Exception as e:
            LOGGER.error(f"Failed to encode image: {e}")
            return None

    def save_image(self, image: Image.Image, folder: str, grayscale: bool = False) -> Optional[str]:
        """保存图像（复用file_utils）"""
        from utils.file_utils import save_image
        return save_image(image, folder, grayscale)