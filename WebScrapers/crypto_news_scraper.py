import pandas as pd
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import re
import time


class NewsScrap:
    def __init__(self):
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

    @staticmethod
    def get_news(soup):
        list1 = []
        cats = ["News", " News", "Analysis", "Sponsored", "Market Update"]
        for cat in cats:
            for n in [i for i, e in enumerate(soup) if e == cat]:
                list1.append((soup[n : n + 6]))

        news = pd.DataFrame(list1)
        news.drop([3], axis=1, inplace=True)
        news.columns = ["category", "heading", "news", "author", "time"]
        news["category"] = news["category"].apply(
            lambda x: x.replace(" News", "News")
        )

        def get_date(x):
            now = datetime.now()
            num = int(re.findall("\d+", x)[0])
            if "MINUTES" in x:
                return (now - timedelta(minutes=num)).strftime(
                    format="%Y-%m-%d %H:%M:%S"
                )
            else:
                return (now - timedelta(hours=num)).strftime(
                    format="%Y-%m-%d %H:%M:%S"
                )

        news["time"] = news["time"].apply(get_date)
        news["source"] = "CoinTelegraph"
        return news

    def cointelegraph_news(self):
        url = "https://cointelegraph.com/"
        content = self.__request(url)
        soup = BeautifulSoup(content, "html.parser")
        for text in soup.find_all("div", attrs={"class": "main-page"}):
            b = text.text.split("  ")
            c = [n.replace("Subscribe", "") for n in b if len(n) > 2]
        news = NewsScrap.get_news(c)
        news.sort_values("time", ascending=False, inplace=True)
        news.reset_index(drop=True, inplace=True)
        return news

    def coin_desk_news(self):
        url = "https://www.coindesk.com/"
        content = self.__request(url)
        soup = BeautifulSoup(content, "html.parser")

        l1 = [
            text["href"]
            for text in soup.find_all(
                "a", attrs={"class": "stream-article"}, href=True
            )
        ]
        cat = []
        heads = []
        newss = []
        authors = []
        times = []
        for link in l1:
            content = self.__request(link)
            soup1 = BeautifulSoup(content, "html.parser")
            list1 = [
                text
                for text in soup1.find_all(
                    "article", attrs={"class": "coindesk-article"}
                )
            ]
            list1 = [
                text
                for text in list1[0].text.replace("\n", " ").split("  ")
                if len(text) > 1 and "Updated" not in text
            ]
            cat.append(list1[3])
            heads.append(list1[0])
            newss.append(list1[4])
            authors.append(list1[1])
            times.append(list1[2][:-3])
        df = pd.DataFrame(data=[cat, heads, newss, authors, times]).T
        df.columns = ["category", "heading", "news", "author", "time"]
        df["category"] = df["category"].apply(
            lambda x: x.replace(" news", "news")
        )

        df["source"] = "CoinDesk"

        df["time"] = pd.to_datetime(
            df["time"].apply(lambda x: " ".join(x.split("at")))
        )
        df.sort_values("time", ascending=False, inplace=True)
        df.reset_index(drop=True, inplace=True)

        return df

    def cryptonewsz(self):
        url = "https://www.cryptonewsz.com/category/cryptocurrency/"
        content = self.__request(url)
        soup = BeautifulSoup(content, "html.parser")
        links = [
            text["href"]
            for text in soup.find_all("a", attrs={"class": "post-thumb"})
        ]
        author = []
        heading = []
        time1 = []
        news1 = []
        links = set(links)
        for link in links:
            content = self.__request(link)
            soup1 = BeautifulSoup(content, "html.parser")
            aa = [
                text.text
                for text in soup1.find_all(
                    "div", attrs={"class": "entry-content"}
                )
            ]
            news1.append(" ".join(aa[0].split("  ")))

            aa = [
                text.div.text
                for text in soup1.find_all(
                    "article", attrs={"class": "container-wrapper"}
                )
            ]

            aa = [text for text in aa[0].split("  ") if len(text) > 2]

            heading.append(aa[0])
            author.append(aa[1])
            time1.append(aa[-1])
            time.sleep(1)

        cats = ["news"] * len(author)

        data1 = pd.DataFrame(data=[cats, heading, news1, author, time1]).T
        data1.columns = ["category", "heading", "news", "author", "time"]

        def get_cat(x):
            if x.startswith("Crypto"):
                return "Cryptocurrency"
            elif x.startswith("Blockchain"):
                return "Blockchain"
            else:
                return "Price Analysis"

        data1["category"] = data1["heading"].apply(get_cat)
        data1["heading"] = data1.apply(
            lambda x: x["heading"].replace(x["category"], ""), axis=1
        )

        data1["time"] = data1["time"].apply(lambda x: x.split("ago")[0])

        def get_date(x):
            now = datetime.now()
            num = int(re.findall("\d+", x)[0])
            if "hour" in x:
                return (now - timedelta(hours=num)).strftime(
                    format="%Y-%m-%d %H:%M:%S"
                )
            elif "day" in x:
                return (now - timedelta(days=num)).strftime(
                    format="%Y-%m-%d %H:%M:%S"
                )
            else:
                return (now - timedelta(minutes=num)).strftime(
                    format="%Y-%m-%d %H:%M:%S"
                )

        data1["time"] = data1["time"].apply(get_date)

        data1.sort_values("time", ascending=False, inplace=True)
        data1.reset_index(drop=True, inplace=True)
        data1["source"] = "cryptonewsz"
        return data1

    def get_all_news(self):
        print("Getting news from CoinDesk!!")
        n1 = self.coin_desk_news()
        print("Getting news from Cointelegraph!!")
        n2 = self.cointelegraph_news()
        print("Getting news from cryptonewsz!! This will take 1-2 mintues. 😉")
        n3 = self.cryptonewsz()
        all_news = pd.concat([n1, n2, n3], axis=0)
        all_news.reset_index(drop=True, inplace=True)
        return all_news
