import requests
from bs4 import BeautifulSoup


class CYCCMinutesCrawler:
    def __init__(self):
        self.base_url = "https://www.cycc.gov.tw/"

    def fetch(self, url: str):
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.text

    def parse(self, html: str):
        soup = BeautifulSoup(html, "html.parser")
        return soup.title.text if soup.title else "No Title"


if __name__ == "__main__":
    crawler = CYCCMinutesCrawler()
    print("CYCC Minutes Crawler Initialized")
