from pathlib import Path
from openai import OpenAI


class ContentWriter:
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.prompt_template = Path("prompts/content_prompt.txt").read_text(encoding="utf-8")

    def write(
        self,
        title: str,
        description: str,
        category: str,
        blog_title: str,
        curiosity: dict,
    ) -> str:
        """블로그 콘텐츠 HTML 생성."""
        prompt = self.prompt_template.format(
            title=title,
            description=description,
            category=category,
            blog_title=blog_title,
            why_trending=curiosity["why_trending"],
            impact_on_me=curiosity["impact_on_me"],
            future_outlook=curiosity["future_outlook"],
            top3_questions=", ".join(curiosity["top3_questions"]),
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=3000,
        )

        return response.choices[0].message.content
