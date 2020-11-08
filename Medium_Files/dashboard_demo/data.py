import pandas as pd
import numpy as np
from datetime import datetime
from pycoingecko import CoinGeckoAPI
from PriceIndices import Indices, MarketHistory


cg = CoinGeckoAPI()
history = MarketHistory()


def get_coin_data(
    crypto="bitcoin", start_date="20130428", end_date="2021501", save_data=None
):
    try:
        df = history.get_price(crypto, start_date, end_date)
        assert df is not None
    except:
        date1 = 1367074800
        date2 = int(datetime.today().timestamp())
        data = cg.get_coin_market_chart_range_by_id("bitcoin-cash", "usd", date1, date2)["prices"]
        df = pd.DataFrame(data=data, columns=["date", "price"])
        df["date"] = df["date"].apply(lambda x: datetime.fromtimestamp(x/1000).strftime("%Y-%m-%d"))
        df["date"] = pd.to_datetime(df["date"])

    indices = Indices(df)
    df_bi = indices.get_vola_index()
    df_bi.drop("price", axis=1, inplace=True)
    df_rsi = indices.get_rsi()
    df_rsi.drop(["price", "RS_Smooth", "RSI_1"], axis=1, inplace=True)
    df_sma = indices.get_simple_moving_average()
    df_sma.drop(["price"], axis=1, inplace=True)
    df_bb = indices.get_bollinger_bands()
    df_bb.drop(["price"], axis=1, inplace=True)
    df_ema = indices.get_exponential_moving_average([20, 50])
    df_ema.drop(["price"], axis=1, inplace=True)
    df_macd = indices.get_moving_average_convergence_divergence()
    df_macd.drop(["price"], axis=1, inplace=True)

    df = pd.merge(df, df_macd, on="date", how="left")
    df = pd.merge(df, df_rsi, on="date", how="left")
    df = pd.merge(df, df_bi, on="date", how="left")
    df = pd.merge(df, df_bb, on="date", how="left")
    df = pd.merge(df, df_ema, on="date", how="left")
    df = pd.merge(df, df_sma, on="date", how="left")
    del df_rsi, df_macd, df_sma, df_bb, df_bi
    df.rename(columns={"RSI_2": "RSI"}, inplace=True)
    df.fillna(0)
    for col in df.columns[1:]:
        df[col] = np.round(df[col], 2)
    df.sort_values("date", ascending=False, inplace=True)
    while save_data:
        df.to_csv("data.csv", index=False)
        break
    return df


def get_coin_price(coin="bitcoin"):
    price = cg.get_price(ids=coin, vs_currencies="usd")[coin]["usd"]
    return price

