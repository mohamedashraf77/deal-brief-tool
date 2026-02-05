from openai import OpenAI
from prompts import SYSTEM_PROMPT, USER_PROMPT
import dotenv
import os


dotenv.load_dotenv()

class llm:
    def __init__(self):
        self.client = OpenAI(
            base_url=os.getenv("BASE_URL"),
            api_key=os.getenv("API_KEY"),
        )

    def extract_with_llm(self, text: str) -> str:
        response = self.client.chat.completions.create(
            model=os.getenv("MODEL_NAME"),
            temperature=0.7,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": USER_PROMPT + text}
            ]
        )
        
        return response.choices[0].message.content
