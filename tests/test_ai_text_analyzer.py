# 单元测试 - AIAnalyzer


from openai import OpenAI
import os


class TestDashscopeAnalyzer:
    def __init__(self, api_key: str = None, base_url: str = None):
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        self.base_url = base_url
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def analyze_image(self, prompt: str, chat_text: str) -> str:
        """调用Dashscope API分析图像"""
        try:
            completion = self.client.chat.completions.create(
                model="qwen-turbo-latest",
                messages=[
                    {'role': 'system', 'content': f"{prompt}"},
                    {"role": "user","content": f"{chat_text}"}
                ]
            )
            result = completion.choices[0].message.content
            print(f"Analysis result: {result}")
            return result
        except Exception as e:
            print(f"Error: {e}")
            return None
        
if __name__ == "__main__":
    api_key = os.getenv("DASHSCOPE_API_KEY")
    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    analyzer = TestDashscopeAnalyzer(api_key, base_url)
    result = analyzer.analyze_image("The above is part of the chat record. Based on this, please guess whether Python should be used to solve the content description in the text? Please answer 'yes', 'no' or 'not sure'.", "***极的聊天记录\n×\n2C25 -5 -15\n***极@微信5/1521：52:19\n我现在的项目差些东西，需要在DataGrip里加入hive，然后导入IDEA里\n***极@微信5/1521：52:23\n这是需求\n***极@微信5/1521:53:50\n数据是现成的，只需要把数据导入hive里\n***极@微信5/1521:53:59\njava")
    print(result)