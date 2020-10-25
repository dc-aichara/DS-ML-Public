import pandas as pd
from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class InshortsNews:
    def __init__(self, category="national"):
        self.category = category
        self.url = "https://www.inshorts.com/en/read/" + str(self.category)
        self.request_timeout = 120
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
        }

        self.session = requests.Session()
        retries = Retry(
            total=5, backoff_factor=0.5, status_forcelist=[502, 503, 504]
        )
        self.session.mount("http://", HTTPAdapter(max_retries=retries))

    def __request(self):
        try:
            response = self.session.get(
                self.url, timeout=self.request_timeout, headers=self.headers
            )
            response.raise_for_status()
            content = response.content.decode("utf-8")
            return content
        except Exception as e:
            raise

    def get_news(self):
        content = self.__request()
        soup = BeautifulSoup(content, "html.parser")
        headings = [
            text.span.text
            for text in soup.find_all("div", attrs={"class": "news-card-title"})
        ]

        newss = [
            text.text.strip().split("\n\n")[0]
            for text in soup.find_all(
                "div", attrs={"class": "news-card-content"}
            )
        ]

        short_by = [
            " ".join(text.div.text.strip().split("/ \n      ")[0].split()[2:])
            for text in soup.find_all("div", attrs={"class": "news-card-title"})
        ]

        times = [
            text.text.strip()
            .split("\n\n")[1]
            .split("/ \n      ")[1]
            .split(" ")[0:]
            for text in soup.find_all("div", attrs={"class": "news-card-title"})
        ]
        times = pd.to_datetime(
            [" ".join(text[3:6] + text[:2]) for text in times]
        )

        data = pd.DataFrame(data=[headings, newss, short_by, times]).T
        data.columns = ["headings", "news", "short_by", "time"]
        data.sort_values("time", inplace=True, ascending=False)
        data.reset_index(drop=True, inplace=True)
        data["category"] = self.category
        return data

    def get_all_news(self):
        categories = [
            "national",
            "business",
            "sports",
            "world",
            "politics",
            "technology",
            "startup",
            "entertainment",
            "miscellaneous",
            "hatke",
            "science",
            "automobile",
        ]
        data = pd.DataFrame(
            columns=["headings", "news", "short_by", "time", "category"]
        )
        for category in categories:
            data1 = InshortsNews(category).get_news()
            data = pd.concat([data, data1], axis=0)
        data.reset_index(drop=True, inplace=True)
        return data
