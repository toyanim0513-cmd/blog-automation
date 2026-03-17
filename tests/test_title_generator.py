import json
import unittest
from unittest.mock import patch, MagicMock
from modules.title_generator import TitleGenerator


class TestTitleGenerator(unittest.TestCase):

    @patch("modules.title_generator.OpenAI")
    def test_generate_returns_three_titles(self, mock_openai_class):
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        expected = {"titles": ["제목A", "제목B", "제목C"]}
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = json.dumps(expected, ensure_ascii=False)
        mock_client.chat.completions.create.return_value = mock_response

        gen = TitleGenerator("fake-key")
        titles = gen.generate(
            title="한은 기준금리 동결",
            why_trending="금리 동결이 화제",
            impact_on_me="대출 이자 영향",
        )

        self.assertEqual(len(titles), 3)
        self.assertEqual(titles[0], "제목A")


if __name__ == "__main__":
    unittest.main()
