# 分析服务

from typing import Optional
from core.ai_analyzer import AIAnalyzer
from core.image_processor import ImageProcessor
from config.config import CONFIG
from utils.logger import LOGGER
from utils.file_utils import copy_image

class AnalysisService:
    def __init__(self, ai_analyzer: AIAnalyzer, image_processor: ImageProcessor):
        self.ai_analyzer = ai_analyzer
        self.image_processor = image_processor
        self.prompt = CONFIG.get("ai.prompt")
        self.judgment_folder = CONFIG.get("paths.judgments")

    async def analyze_image(self, image_path: str) -> bool:
        """分析图像并处理结果，返回是否需要保存"""
        from PIL import Image
        image = Image.open(image_path)
        base64_image = self.image_processor.encode_image(image)
        if not base64_image:
            return False

        result = self.ai_analyzer.analyze_image(base64_image, self.prompt)
        if result and "yes" in result.lower():
            LOGGER.info(f"AI recommends Python for {image_path}")
            copy_image(image_path, self.judgment_folder)
            return True
        return False
    
    async def analyze_text(self, text: Optional[str]) -> bool:
        """分析文本并处理结果，返回是否需要保存"""
        if not text:
            LOGGER.warning("No text provided for analysis")
            return False
        result = self.ai_analyzer.analyze_text(text, self.prompt)
        if result and "yes" in result.lower():
            LOGGER.info(f"AI recommends Python for {text}")
            return True
        return False