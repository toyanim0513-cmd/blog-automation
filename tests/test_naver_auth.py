import json
import unittest
from unittest.mock import patch, MagicMock
from modules.naver_auth import NaverAuth


class TestNaverAuth(unittest.TestCase):

    def test_get_authorize_url(self):
        auth = NaverAuth("test_id", "test_secret", "http://localhost:8888/callback")
        url = auth.get_authorize_url()
        self.assertIn("https://nid.naver.com/oauth2.0/authorize", url)
        self.assertIn("client_id=test_id", url)
        self.assertIn("response_type=code", url)

    @patch("modules.naver_auth.requests.post")
    def test_fetch_token_returns_tokens(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.json.return_value = {
            "access_token": "abc123",
            "refresh_token": "ref456",
            "token_type": "Bearer",
            "expires_in": "3600",
        }
        mock_post.return_value = mock_resp

        auth = NaverAuth("test_id", "test_secret", "http://localhost:8888/callback")
        tokens = auth.fetch_token("fake_code", "fake_state")
        self.assertEqual(tokens["access_token"], "abc123")
        self.assertEqual(tokens["refresh_token"], "ref456")

    @patch("modules.naver_auth.requests.post")
    def test_refresh_access_token(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.json.return_value = {
            "access_token": "new_token",
            "token_type": "Bearer",
            "expires_in": "3600",
        }
        mock_post.return_value = mock_resp

        auth = NaverAuth("test_id", "test_secret", "http://localhost:8888/callback")
        new_token = auth.refresh_access_token("ref456")
        self.assertEqual(new_token, "new_token")


if __name__ == "__main__":
    unittest.main()
