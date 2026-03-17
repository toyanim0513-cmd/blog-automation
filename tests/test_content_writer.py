import unittest
from unittest.mock import patch, MagicMock
from modules.content_writer import ContentWriter


class TestContentWriter(unittest.TestCase):

    @patch("modules.content_writer.OpenAI")
    def test_write_returns_html_content(self, mock_openai_class):
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        html_content = "<h3>도입부</h3><p>요즘 금리 때문에 난리죠?</p>"
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = html_content
        mock_client.chat.completions.create.return_value = mock_response

        writer = ContentWriter("fake-key")
        result = writer.write(
            title="한은 기준금리 동결",
            description="한국은행이 기준금리를 동결했다.",
            category="경제",
            blog_title="금리 동결, 내 대출은?",
            curiosity={
                "why_trending": "금리 동결이 화제",
                "impact_on_me": "대출 이자 영향",
                "future_outlook": "하반기 인하 가능성",
                "top3_questions": ["질문1", "질문2", "질문3"],
            },
        )

        self.assertIn("<h3>", result)
        self.assertIsInstance(result, str)


if __name__ == "__main__":
    unittest.main()
