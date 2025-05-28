# AI分析接口

from openai import OpenAI
from PIL import Image
import base64
import os


class DashscopeAnalyzer():
    def __init__(self, api_key = None, base_url = None):
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        self.base_url = base_url
        print(self.base_url)
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def analyze_image(self, image_data, prompt):
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
            return result
        except Exception as e:
            print(f"Error analyzing image: {e}")
            return None
        

def main():
    """Run the AI test."""
    screenshot_path = r"tests\screenshot_20250515_220101.png"
    image = Image.open(screenshot_path)
    from io import BytesIO
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    encoded = base64.b64encode(buffered.getvalue()).decode("utf-8")
    ai_analyzer = DashscopeAnalyzer(base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1")
    result = ai_analyzer.analyze_image(encoded, "这里面有什么")
    print(result)



if __name__ == "__main__":
    main()