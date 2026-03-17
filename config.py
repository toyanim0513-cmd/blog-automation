import os
from dotenv import load_dotenv

load_dotenv()

# Naver API
NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")
NAVER_BLOG_ID = os.getenv("NAVER_BLOG_ID")
NAVER_BLOG_API_PASSWORD = os.getenv("NAVER_BLOG_API_PASSWORD")

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AI_MODEL = "gpt-4o-mini"

# Pollinations (무료, 키 불필요)
POLLINATIONS_URL = "https://image.pollinations.ai/prompt"

# 트렌드 수집 설정
TREND_CATEGORIES = {
    "뉴스": ["정치", "사회", "IT", "생활"],
    "경제": ["증시", "부동산", "환율", "금리"],
    "핫이슈": ["연예", "스포츠", "트렌드"],
}
NEWS_DISPLAY_COUNT = 10
