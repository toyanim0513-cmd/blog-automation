import json
from pathlib import Path
from openai import OpenAI


class CuriosityEngine:
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.prompt_template = Path("prompts/curiosity_prompt.txt").read_text(encoding="utf-8")

    def extract(self, title: str, description: str, category: str) -> dict:
        """뉴스에서 궁금증 포인트를 추출."""
        prompt = self.prompt_template.format(
            title=title, description=description, category=category
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            response_format={"type": "json_object"},
        )

        return json.loads(response.choices[0].message.content)
