"""네이버 OAuth 2.0 인증 모듈."""

import json
import secrets
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlencode, urlparse, parse_qs

import requests

TOKEN_FILE = Path(".naver_tokens.json")


class NaverAuth:
    """네이버 OAuth 2.0 Authorization Code Flow."""

    AUTHORIZE_URL = "https://nid.naver.com/oauth2.0/authorize"
    TOKEN_URL = "https://nid.naver.com/oauth2.0/token"

    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self._state = secrets.token_urlsafe(16)

    def get_authorize_url(self) -> str:
        """브라우저로 열 네이버 로그인 URL 생성."""
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "state": self._state,
        }
        return f"{self.AUTHORIZE_URL}?{urlencode(params)}"

    def start_callback_server(self) -> tuple[str, str]:
        """localhost:8888에서 콜백을 수신하여 code, state를 반환."""
        result = {}

        class CallbackHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                query = parse_qs(urlparse(self.path).query)
                result["code"] = query.get("code", [None])[0]
                result["state"] = query.get("state", [None])[0]
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write("✅ 인증 완료! 이 창을 닫아주세요.".encode("utf-8"))

            def log_message(self, format, *args):
                pass  # 로그 출력 억제

        parsed = urlparse(self.redirect_uri)
        server = HTTPServer((parsed.hostname, parsed.port), CallbackHandler)
        server.handle_request()
        server.server_close()

        return result.get("code", ""), result.get("state", "")

    def fetch_token(self, code: str, state: str) -> dict:
        """인증 코드를 access_token + refresh_token으로 교환."""
        data = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "state": state,
        }
        resp = requests.post(self.TOKEN_URL, data=data)
        return resp.json()

    def refresh_access_token(self, refresh_token: str) -> str:
        """만료된 access_token 갱신. 새 access_token 반환."""
        data = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": refresh_token,
        }
        resp = requests.post(self.TOKEN_URL, data=data)
        return resp.json()["access_token"]

    def save_tokens(self, tokens: dict) -> None:
        """토큰을 .naver_tokens.json에 저장."""
        TOKEN_FILE.write_text(json.dumps(tokens, ensure_ascii=False, indent=2), encoding="utf-8")

    def load_tokens(self) -> dict | None:
        """저장된 토큰 로드. 없으면 None 반환."""
        if TOKEN_FILE.exists():
            return json.loads(TOKEN_FILE.read_text(encoding="utf-8"))
        return None

    def login(self) -> str:
        """전체 OAuth 흐름 오케스트레이션. access_token 반환.

        저장된 토큰이 있으면 refresh 시도, 없으면 브라우저 로그인.
        """
        tokens = self.load_tokens()

        if tokens and tokens.get("refresh_token"):
            try:
                new_token = self.refresh_access_token(tokens["refresh_token"])
                tokens["access_token"] = new_token
                self.save_tokens(tokens)
                return new_token
            except Exception:
                pass  # refresh 실패 시 새로 로그인

        # 브라우저로 로그인
        url = self.get_authorize_url()
        webbrowser.open(url)
        code, state = self.start_callback_server()
        tokens = self.fetch_token(code, state)
        self.save_tokens(tokens)
        return tokens["access_token"]
