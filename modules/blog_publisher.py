from pathlib import Path
import requests


class BlogPublisher:
    """네이버 블로그 OAuth REST API 발행."""

    API_URL = "https://openapi.naver.com/blog/writePost.json"

    def __init__(self, access_token: str):
        self.access_token = access_token
        self.template = Path("templates/blog_template.html").read_text(encoding="utf-8")

    def wrap_content(self, content: str) -> str:
        """콘텐츠를 블로그 템플릿으로 감싸기."""
        return self.template.replace("{content}", content)

    def publish(self, title: str, content: str, tags: list[str] | None = None) -> str | None:
        """네이버 블로그에 글 발행. 성공 시 응답 메시지 반환."""
        wrapped = self.wrap_content(content)

        headers = {
            "Authorization": f"Bearer {self.access_token}",
        }
        data = {
            "title": title,
            "contents": wrapped,
        }

        response = requests.post(self.API_URL, headers=headers, data=data)

        if response.status_code == 200:
            result = response.json()
            return result.get("message")
        return None

    def get_blog_url(self, post_url: str) -> str:
        """발행된 포스트의 URL 반환."""
        return post_url
