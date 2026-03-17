import unittest
from unittest.mock import patch, MagicMock
from modules.blog_publisher import BlogPublisher


class TestBlogPublisher(unittest.TestCase):

    @patch("modules.blog_publisher.requests.post")
    def test_publish_sends_correct_request(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<?xml version="1.0"?><methodResponse><params><param><value><string>12345</string></value></param></params></methodResponse>'
        mock_post.return_value = mock_response

        publisher = BlogPublisher("test_id", "test_password")
        result = publisher.publish(
            title="테스트 제목",
            content="<p>테스트 내용</p>",
        )

        mock_post.assert_called_once()
        self.assertIsNotNone(result)

    def test_wrap_content_includes_template(self):
        publisher = BlogPublisher("test_id", "test_password")
        wrapped = publisher.wrap_content("<p>테스트</p>")

        self.assertIn("<p>테스트</p>", wrapped)
        self.assertIn("AI가 분석한", wrapped)


if __name__ == "__main__":
    unittest.main()
