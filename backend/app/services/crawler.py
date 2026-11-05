from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from app.core.logging import get_logger

logger = get_logger(__name__)

class Crawler:
    def __init__(self, base_url):
        self.base_url = base_url
        self.visited_urls = set()

    def get_all_urls(self):
        urls_to_visit = [self.base_url]
        all_urls = set()

        while urls_to_visit:
            url = urls_to_visit.pop(0)
            if url in self.visited_urls:
                continue

            try:
                response = requests.get(url)
                response.raise_for_status()
                self.visited_urls.add(url)
                all_urls.add(url)
                logger.info(f"Crawled {url}")

                soup = BeautifulSoup(response.text, 'html.parser')
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    full_url = urljoin(self.base_url, href)
                    if self._is_valid_url(full_url):
                        urls_to_visit.append(full_url)

            except requests.RequestException as e:
                logger.error(f"Error crawling {url}: {e}")

        return list(all_urls)

    def _is_valid_url(self, url):
        parsed_base = urlparse(self.base_url)
        parsed_url = urlparse(url)
        return parsed_url.netloc == parsed_base.netloc and url not in self.visited_urls

    def extract_text_from_url(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Remove nav and footer elements
            for element in soup(['nav', 'footer']):
                element.decompose()

            # Remove code blocks
            for element in soup.find_all('pre'):
                element.decompose()

            main_content = soup.find('article') or soup.find('main') or soup.body

            title = soup.title.string if soup.title else "No Title"

            return main_content.get_text(separator='\n', strip=True), title
        except requests.RequestException as e:
            logger.error(f"Error extracting text from {url}: {e}")
            return None, None
