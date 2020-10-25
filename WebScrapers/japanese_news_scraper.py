import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz
from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import re
import time

time_now = datetime.now(tz=pytz.FixedOffset(540))


class JapaneseNewsScrap:
    def __init__(self, secnds=24 * 60 * 60):
        self.request_timeout = 120
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
        }

        self.session = requests.Session()
        retries = Retry(
            total=5, backoff_factor=0.5, status_forcelist=[502, 503, 504]
        )
        self.session.mount("http://", HTTPAdapter(max_retries=retries))
        self.secnds = secnds

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

    def get_cointelegraph_news(self):
        url = "https://jp.cointelegraph.com"
        content = self.__request(url)
        soup = BeautifulSoup(content, "html.parser")
        l1 = [
            text["href"]
            for text in soup.find_all("a", href=True)
            if len(text["href"]) > 62
            and "https://jp.cointelegraph.com/news/" in text["href"]
        ]
        l1 = set(l1)
        d1 = {"time": [], "heading": [], "news": [], "link": []}
        for link in l1:
            try:
                content = self.__request(link)
                soup1 = BeautifulSoup(content, "html.parser")
                t = pd.to_datetime(
                    soup1.find("div", attrs={"class": "date"})["datetime"]
                )
                news1 = soup1.find(
                    "div", attrs={"class", "post-content"}
                ).text.split("【関連記事")[0]
                if news1.split("  ")[-1] != "":
                    news1 = news1.split("  ")[-1]
                else:
                    news1 = news1.split("  ")[-2]
                if (time_now - t).days == 0 and (
                    time_now - t
                ).seconds < self.secnds:
                    d1["heading"].append(soup1.find("h1").text)
                    d1["time"].append(t)
                    d1["news"].append(news1)
                    d1["link"].append(link)
                else:
                    pass
            except:
                pass
        df = pd.DataFrame(data=d1)
        df.sort_values("time", ascending=False, inplace=True)
        df["time"] = df["time"].apply(
            lambda x: x.strftime(format="%Y-%m-%d %H:%M:%S")
        )
        df.reset_index(drop=True, inplace=True)
        df["source"] = ["Cointelegraph"] * len(df)
        return df

    def get_coin_desk_news(self):
        url = "https://www.coindeskjapan.com/"
        content = self.__request(url)
        soup = BeautifulSoup(content, "html.parser")
        l1 = [
            text["href"]
            for text in soup.find_all("a", href=True)
            if "/www.coindeskjapan.com/2" in text["href"]
            or "/www.coindeskjapan.com/1" in text["href"]
            or "/www.coindeskjapan.com/3" in text["href"]
            or "/www.coindeskjapan.com/4" in text["href"]
            or "/www.coindeskjapan.com/5" in text["href"]
            or "/www.coindeskjapan.com/6" in text["href"]
        ]
        l1 = set(l1)
        d1 = {"time": [], "heading": [], "news": [], "link": []}
        time_now = datetime.now()
        for link in l1:
            try:
                content = self.__request(link)
                soup1 = BeautifulSoup(content, "html.parser")
                t = soup1.find(
                    "div", attrs={"class": "timestamp"}
                ).span.text.split("公開日：")[1]
                t1 = re.findall("[0-9]+", t)
                t = pd.to_datetime("-".join(t1[:3]) + " " + ":".join(t1[3:]))
                h1 = soup1.find("h1").text
                news1 = (
                    soup1.find("div", attrs={"class": "entry-content"})
                    .text.split("翻訳")[0]
                    .strip()
                )
                if (time_now - t).days == 0 and (
                    time_now - t
                ).seconds < self.secnds:
                    d1["heading"].append(soup1.find("h1").text)
                    d1["time"].append(t)
                    d1["news"].append(news1)
                    d1["link"].append(link)
                else:
                    pass
            except:
                pass
        df = pd.DataFrame(data=d1)
        df.sort_values("time", ascending=False, inplace=True)
        df["time"] = df["time"].apply(
            lambda x: x.strftime(format="%Y-%m-%d %H:%M:%S")
        )
        df.reset_index(drop=True, inplace=True)
        df["source"] = ["CoinDesk"] * len(df)
        return df

    def get_coin_post_news(self):
        url = "https://coinpost.jp"
        content = self.__request(url)
        soup = BeautifulSoup(content, "html.parser")
        l1 = [
            text["href"]
            for text in soup.find_all("a", href=True)
            if "https://coinpost.jp/?p=" in text["href"]
        ]
        l1 = set(l1)
        d1 = {"time": [], "heading": [], "news": [], "link": []}
        for link in l1:
            try:
                content = self.__request(link)
                soup1 = BeautifulSoup(content, "html.parser")
                t = pd.to_datetime(soup1.time["datetime"])
                news1 = [
                    text.text.split("\n\n \n\n")[-1]
                    .strip()
                    .replace("\n", " ")
                    .replace("\u3000", " ")
                    for text in soup1.find_all(
                        "div", attrs={"class": "entry-content"}
                    )
                ]
                h1 = soup1.h1.text.strip().replace("\u3000", " ")
                if (time_now - t).days == 0 and (
                    time_now - t
                ).seconds < self.secnds:
                    d1["heading"].append(h1)
                    d1["time"].append(t)
                    d1["news"].append(news1[0])
                    d1["link"].append(link)
                else:
                    pass
            except:
                pass
        df = pd.DataFrame(data=d1)
        df.sort_values("time", ascending=False, inplace=True)
        df["time"] = df["time"].apply(
            lambda x: x.strftime(format="%Y-%m-%d %H:%M:%S")
        )
        df.reset_index(drop=True, inplace=True)
        df["source"] = ["CoinPost"] * len(df)
        return df

    def get_nikkei_news(self):
        url = "https://www.nikkei.com"
        content = self.__request(url)
        soup = BeautifulSoup(content, "html.parser")
        l1 = [
            text["href"]
            for text in soup.find_all("a", href=True)
            if "/article/D" in text["href"] and len(text["href"]) == 38
        ]
        for i, link in enumerate(l1):
            l1[i] = "https://www.nikkei.com" + link
        l1 = set(l1)
        d1 = {"time": [], "heading": [], "news": [], "link": []}
        time_now = datetime.now()
        for link in l1:
            try:
                content = self.__request(link)
                soup1 = BeautifulSoup(content, "html.parser")
                t = pd.to_datetime(
                    soup1.find("dd", attrs={"class": "cmnc-publish"}).text
                )
                news1 = soup1.find(
                    "div", attrs={"class": "cmn-article_text"}
                ).text.strip()
                h1 = (
                    soup1.h1.text.strip()
                    .replace("\u3000", " ")
                    .replace("\n", "")
                )
                if (time_now - t).days == 0 and (
                    time_now - t
                ).seconds < self.secnds:
                    d1["heading"].append(h1)
                    d1["time"].append(t)
                    d1["news"].append(news1)
                    d1["link"].append(link)
                else:
                    pass
            except:
                pass
        df = pd.DataFrame(data=d1)
        df.sort_values("time", ascending=False, inplace=True)
        df["time"] = df["time"].apply(
            lambda x: x.strftime(format="%Y-%m-%d %H:%M:%S")
        )
        df.reset_index(drop=True, inplace=True)
        df["source"] = ["Nikkei"] * len(df)
        return df

    def get_all_news(self):
        n1 = self.get_cointelegraph_news()
        n2 = self.get_coin_desk_news()
        n3 = self.get_coin_post_news()
        n4 = self.get_nikkei_news()
        all_news = pd.concat([n1, n2, n3, n4], axis=0)
        all_news.reset_index(drop=True, inplace=True)
        all_news = all_news.sort_values("time", ascending=False).reset_index(
            drop=True
        )
        return all_news
