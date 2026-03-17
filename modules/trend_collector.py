import re
import requests


class TrendCollector:
    NAVER_NEWS_URL = "https://openapi.naver.com/v1/search/news.json"

    def __init__(self, client_id: str, client_secret: str):
        self.headers = {
            "X-Naver-Client-Id": client_id,
            "X-Naver-Client-Secret": client_secret,
        }

    def search_news(self, query: str, display: int = 10, sort: str = "date") -> list[dict]:
        """네이버 뉴스 검색 API로 뉴스 검색."""
        params = {"query": query, "display": display, "sort": sort}
        resp = requests.get(self.NAVER_NEWS_URL, headers=self.headers, params=params)
        resp.raise_for_status()

        items = resp.json().get("items", [])
        return [
            {
                "title": self._clean_html(item["title"]),
                "description": self._clean_html(item["description"]),
                "link": item["link"],
                "pubDate": item["pubDate"],
            }
            for item in items
        ]

    def collect_trends(self) -> list[dict]:
        """카테고리별 트렌드 뉴스 수집 후 통합 리스트 반환."""
        from config import TREND_CATEGORIES, NEWS_DISPLAY_COUNT

        trends = []
        seen_titles = set()

        for category, keywords in TREND_CATEGORIES.items():
            for keyword in keywords:
                articles = self.search_news(keyword, display=NEWS_DISPLAY_COUNT)
                for article in articles:
                    if article["title"] not in seen_titles:
                        seen_titles.add(article["title"])
                        trends.append({"category": category, **article})

        return trends

    @staticmethod
    def _clean_html(text: str) -> str:
        return re.sub(r"<[^>]+>", "", text).strip()
