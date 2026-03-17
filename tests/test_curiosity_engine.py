import json
import unittest
from unittest.mock import patch, MagicMock
from modules.curiosity_engine import CuriosityEngine


class TestCuriosityEngine(unittest.TestCase):

    @patch("modules.curiosity_engine.OpenAI")
    def test_extract_curiosity_returns_structured(self, mock_openai_class):
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        expected = {
            "why_trending": "금리가 동결되어 화제",
            "impact_on_me": "대출 이자에 영향",
            "future_outlook": "하반기 인하 가능성",
            "top3_questions": ["질문1", "질문2", "질문3"],
        }
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = json.dumps(expected, ensure_ascii=False)
        mock_client.chat.completions.create.return_value = mock_response

        engine = CuriosityEngine("fake-key")
        result = engine.extract(
            title="한은 기준금리 동결",
            description="한국은행이 기준금리를 동결했다.",
            category="경제",
        )

        self.assertEqual(result["why_trending"], "금리가 동결되어 화제")
        self.assertEqual(len(result["top3_questions"]), 3)


if __name__ == "__main__":
    unittest.main()
