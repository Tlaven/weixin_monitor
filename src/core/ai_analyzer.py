# AI分析接口

from abc import ABC, abstractmethod
from openai import OpenAI
from utils.logger import LOGGER
import os

class AIAnalyzer(ABC):
    @abstractmethod
    def analyze_image(self, image_data: str, prompt: str) -> str:
        """分析图像，返回结果"""
        pass

    @abstractmethod
    def analyze_text(self, text: str, prompt: str) -> str:
        """分析文本，返回结果"""
        pass

class DashscopeAnalyzer(AIAnalyzer):
    def __init__(self, api_key: str = None, base_url: str = None):
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        self.base_url = base_url
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        LOGGER.info("Initialized DashscopeAnalyzer")

    def analyze_image(self, image_data: str, prompt: str) -> str:
        """调用Dashscope API分析图像"""
        try:
            completion = self.client.chat.completions.create(
                model="qwen-vl-max-latest",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_data}"}},
                            {"type": "text", "text": prompt}
                        ]
                    }
                ]
            )
            result = completion.choices[0].message.content
            LOGGER.info(f"AI image analysis result: {result}")
            return result
        except Exception as e:
            LOGGER.error(f"Failed to analyze image: {e}")
            return None

    def analyze_text(self, prompt: str, chat_text: str) -> str:
        """调用Dashscope API分析文本"""
        try:
            completion = self.client.chat.completions.create(
                model="qwen-turbo-latest",
                messages=[
                    {'role': 'system', 'content': f"{prompt}"},
                    {"role": "user","content": f"{chat_text}"}
                ]
            )
            result = completion.choices[0].message.content
            LOGGER.info(f"AI text analysis result: {result}")
            return result
        except Exception as e:
            LOGGER.error(f"Failed to analyze text: {e}")
            return None