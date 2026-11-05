import unittest
from unittest.mock import MagicMock, patch

from app.services.crawler import Crawler


class TestCrawler(unittest.TestCase):

    @patch('requests.get')
    def test_get_all_urls(self, mock_get):
        # Mock the response from requests.get
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><body><a href="/page2">Page 2</a></body></html>'
        mock_get.return_value = mock_response

        crawler = Crawler("http://example.com")
        urls = crawler.get_all_urls()

        self.assertIn("http://example.com", urls)
        self.assertIn("http://example.com/page2", urls)

    @patch('requests.get')
    def test_extract_text_from_url(self, mock_get):
        # Mock the response from requests.get
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><head><title>Test Title</title></head><body><article>This is the article content.</article></body></html>'
        mock_get.return_value = mock_response

        crawler = Crawler("http://example.com")
        text, title = crawler.extract_text_from_url("http://example.com")

        self.assertEqual(title, "Test Title")
        self.assertEqual(text, "This is the article content.")

if __name__ == '__main__':
    unittest.main()
