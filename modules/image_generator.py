import time
from pathlib import Path
from urllib.parse import quote
import requests


class ImageGenerator:
    """Pollinations.ai 기반 무료 이미지 생성."""

    BASE_URL = "https://image.pollinations.ai/prompt"

    def generate_thumbnail(self, title: str, output_dir: str = "images") -> str:
        """블로그 썸네일 이미지 생성."""
        prompt = f"Modern Korean blog thumbnail, clean design, topic: {title}, minimal text, professional"
        return self._generate(prompt, output_dir, "thumbnail")

    def generate_summary_card(self, points: list[str], output_dir: str = "images") -> str:
        """요약 카드 이미지 생성."""
        points_text = ", ".join(points[:3])
        prompt = f"Infographic summary card, 3 key points, clean design, Korean style: {points_text}"
        return self._generate(prompt, output_dir, "summary")

    def _generate(self, prompt: str, output_dir: str, prefix: str) -> str:
        """Pollinations.ai API로 이미지 생성 및 저장."""
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        encoded_prompt = quote(prompt)
        url = f"{self.BASE_URL}/{encoded_prompt}?width=1280&height=720&model=flux"

        response = requests.get(url, timeout=60)
        response.raise_for_status()

        timestamp = int(time.time())
        filename = f"{prefix}_{timestamp}.jpg"
        filepath = str(Path(output_dir) / filename)

        with open(filepath, "wb") as f:
            f.write(response.content)

        return filepath
