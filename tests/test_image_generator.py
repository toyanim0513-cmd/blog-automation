import unittest
from unittest.mock import patch, MagicMock
from modules.image_generator import ImageGenerator


class TestImageGenerator(unittest.TestCase):

    @patch("modules.image_generator.requests.get")
    def test_generate_thumbnail_saves_file(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"fake_image_data"
        mock_get.return_value = mock_response

        gen = ImageGenerator()
        path = gen.generate_thumbnail("금리 동결 뉴스", output_dir="tests/temp")

        self.assertTrue(path.endswith(".jpg"))
        mock_get.assert_called_once()

    @patch("modules.image_generator.requests.get")
    def test_generate_summary_card_saves_file(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"fake_image_data"
        mock_get.return_value = mock_response

        gen = ImageGenerator()
        path = gen.generate_summary_card(
            ["포인트1", "포인트2", "포인트3"], output_dir="tests/temp"
        )

        self.assertTrue(path.endswith(".jpg"))

    def tearDown(self):
        import shutil
        from pathlib import Path
        temp = Path("tests/temp")
        if temp.exists():
            shutil.rmtree(temp)


if __name__ == "__main__":
    unittest.main()
