import json
from pathlib import Path
from openai import OpenAI


class TitleGenerator:
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.prompt_template = Path("prompts/title_prompt.txt").read_text(encoding="utf-8")

    def generate(self, title: str, why_trending: str, impact_on_me: str) -> list[str]:
        """클릭 유도 제목 3개 생성."""
        prompt = self.prompt_template.format(
            title=title, why_trending=why_trending, impact_on_me=impact_on_me
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
            response_format={"type": "json_object"},
        )

        data = json.loads(response.choices[0].message.content)
        return data["titles"]
