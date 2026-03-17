import unittest
from unittest.mock import patch, MagicMock
from modules.trend_collector import TrendCollector


class TestTrendCollector(unittest.TestCase):

    @patch("modules.trend_collector.requests.get")
    def test_search_news_returns_articles(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [
                {
                    "title": "테스트 뉴스 <b>제목</b>",
                    "description": "테스트 뉴스 설명",
                    "link": "https://example.com/1",
                    "pubDate": "Mon, 17 Mar 2026 10:00:00 +0900",
                }
            ]
        }
        mock_get.return_value = mock_response

        collector = TrendCollector("test_id", "test_secret")
        results = collector.search_news("테스트")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "테스트 뉴스 제목")
        self.assertNotIn("<b>", results[0]["title"])

    @patch("modules.trend_collector.requests.get")
    def test_collect_trends_returns_categorized(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [
                {
                    "title": "뉴스 제목",
                    "description": "설명",
                    "link": "https://example.com",
                    "pubDate": "Mon, 17 Mar 2026 10:00:00 +0900",
                }
            ]
        }
        mock_get.return_value = mock_response

        collector = TrendCollector("test_id", "test_secret")
        trends = collector.collect_trends()

        self.assertIsInstance(trends, list)
        self.assertTrue(len(trends) > 0)
        self.assertIn("category", trends[0])
        self.assertIn("title", trends[0])


if __name__ == "__main__":
    unittest.main()
