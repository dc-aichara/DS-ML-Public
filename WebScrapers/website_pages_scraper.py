import pandas as pd
from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import re


class WebScraper:
    def __init__(self, main_page_url="https://www.exaple.com/"):
        self.url = main_page_url
        self.domain = main_page_url.split(".")[-2]
        self.request_timeout = 120
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
        }

        self.session = requests.Session()
        retries = Retry(
            total=5, backoff_factor=0.5, status_forcelist=[502, 503, 504]
        )
        self.session.mount("http://", HTTPAdapter(max_retries=retries))

    def __request(self, url):
        try:
            response = self.session.get(
                url, timeout=self.request_timeout, headers=self.headers
            )
            response.raise_for_status()
            content = response.content.decode("utf-8")
            return content
        except Exception as e:
            raise

    def get_urls(self, urls=[]):
        """
        Find all urls on each page of given url
        :param urls: list of urls
        :return: list
        """
        all_urls = []
        for link in urls:
            try:
                c = self.__request(link)
                soup = BeautifulSoup(c, "html.parser")
                links = [
                    text["href"]
                    for text in soup.find_all("a", href=True)
                    if len(text["href"]) > 2
                ]
                for i, l in enumerate(links):
                    if l.startswith("http") or l.startswith("www"):
                        links[i] = l
                    else:
                        links[i] = self.url + l
                new_urls = set(links)
                new_urls = [
                    url
                    for url in new_urls
                    if url.startswith(self.url)
                    and "tel" not in url
                    and "#" not in url
                    and "pdf" not in url
                    and "http:" not in url
                    and "java" not in url
                    and "///www" not in url
                    and "mailto" not in url
                    and "privacy" not in url
                ]
                all_urls = all_urls + new_urls
            except Exception as e:
                print(e)
        return list(set(all_urls))

    def scrap_website(self, depth=2):
        """
        Scrape pages of a website to given depth
        :param depth: int
        :return: pandas DataFrame
        """
        urls_list = [[i] for i in range(depth)]
        all_urls = [self.url]
        for i in range(depth):
            if i == 0:
                urls_list[i] = self.get_urls(urls=[self.url])
                all_urls = all_urls + urls_list[i]
            else:
                urls_list[i] = self.get_urls(urls=urls_list[i - 1])
                all_urls = all_urls + urls_list[i]
        del urls_list
        data = {"url": [], "title": [], "text": []}

        tags = ["h1", "h2", "h3", "span", "li", "ul", "section", "article", "p"]
        for url in set(all_urls):
            try:
                c = self.__request(url)
                soup = BeautifulSoup(c, "html.parser")
                texts = []
                for tag in tags:
                    t = [
                        " ".join(
                            re.sub("\n\r|\n|\r|\t|\xa0", "", text.text).split()
                        )
                        for text in soup.find_all(tag)
                    ]
                    t = [text for text in t if len(text) > 2]
                    texts = texts + t
                texts = " ".join(texts)
                data["url"].append(url)
                data["title"].append(soup.title.text)
                data["text"].append(texts)
            except Exception as e:
                print(e)
        df = pd.DataFrame(data=data)
        return df
