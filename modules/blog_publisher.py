import re
from pathlib import Path
import requests


class BlogPublisher:
    """네이버 블로그 XML-RPC API 발행."""

    API_URL = "https://api.blog.naver.com/xmlrpc"

    def __init__(self, blog_id: str, api_password: str):
        self.blog_id = blog_id
        self.api_password = api_password
        self.template = Path("templates/blog_template.html").read_text(encoding="utf-8")

    def wrap_content(self, content: str) -> str:
        """콘텐츠를 블로그 템플릿으로 감싸기."""
        return self.template.replace("{content}", content)

    def publish(self, title: str, content: str, tags: list[str] | None = None) -> str | None:
        """네이버 블로그에 글 발행. 성공 시 포스트 ID 반환."""
        wrapped = self.wrap_content(content)
        tag_str = ", ".join(tags) if tags else ""

        xml_body = f"""<?xml version="1.0" encoding="UTF-8"?>
<methodCall>
  <methodName>metaWeblog.newPost</methodName>
  <params>
    <param><value><string>{self.blog_id}</string></value></param>
    <param><value><string>{self.blog_id}</string></value></param>
    <param><value><string>{self.api_password}</string></value></param>
    <param><value><struct>
      <member>
        <name>title</name>
        <value><string>{self._escape_xml(title)}</string></value>
      </member>
      <member>
        <name>description</name>
        <value><string>{self._escape_xml(wrapped)}</string></value>
      </member>
      <member>
        <name>categories</name>
        <value><array><data>
          <value><string>{tag_str}</string></value>
        </data></array></value>
      </member>
    </struct></value></param>
    <param><value><boolean>1</boolean></value></param>
  </params>
</methodCall>"""

        headers = {"Content-Type": "text/xml; charset=utf-8"}
        response = requests.post(self.API_URL, data=xml_body.encode("utf-8"), headers=headers)

        if response.status_code == 200 and "<fault>" not in response.text:
            return self._extract_post_id(response.text)
        return None

    def get_blog_url(self, post_id: str) -> str:
        return f"https://blog.naver.com/{self.blog_id}/{post_id}"

    @staticmethod
    def _escape_xml(text: str) -> str:
        return (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
        )

    @staticmethod
    def _extract_post_id(xml_text: str) -> str | None:
        match = re.search(r"<string>(\d+)</string>", xml_text)
        return match.group(1) if match else None
