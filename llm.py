from openai import OpenAI
from prompts import SYSTEM_PROMPT, USER_PROMPT
import dotenv
import os


dotenv.load_dotenv()

class llm:
    def __init__(self):
        self.client = OpenAI(
            base_url=os.getenv("base_url"),
            api_key=os.getenv("api_key"),
        )

    def extract_with_llm(self, text: str) -> str:
        response = self.client.chat.completions.create(
            model=os.getenv("model_name"),
            temperature=0.2,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": USER_PROMPT + text}
            ]
        )
        return response.choices[0].message.content
