from PriceIndices import Indices, MarketHistory
import pandas as pd
import numpy as np
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()
history = MarketHistory()


def get_coin_data(crypto='bitcoin', start_date='20130428', end_date='20200501', save_data=None):
    df = history.get_price(crypto, start_date, end_date)
    df_bi = Indices.get_bvol_index(df)
    df_bi.drop('price', axis=1, inplace=True)
    df_rsi = Indices.get_rsi(df)
    df_rsi.drop(['price', 'RS_Smooth', 'RSI_1'], axis=1, inplace=True)
    df_sma = Indices.get_simple_moving_average(df)
    df_sma.drop(['price'], axis=1, inplace=True)
    df_bb = Indices.get_bollinger_bands(df)
    df_bb.drop(['price'], axis=1, inplace=True)
    df_ema = Indices.get_exponential_moving_average(df, [20, 50])
    df_ema.drop(['price'], axis=1, inplace=True)
    df_macd = Indices.get_moving_average_convergence_divergence(df)
    df_macd.drop(['price',], axis=1, inplace=True)

    df = pd.merge(df, df_macd, on='date', how='left')
    df = pd.merge(df, df_rsi, on='date', how='left')
    df = pd.merge(df, df_bi, on='date', how='left')
    df = pd.merge(df, df_bb, on='date', how='left')
    df = pd.merge(df, df_ema, on='date', how='left')
    df = pd.merge(df, df_sma, on='date', how='left')
    del df_rsi, df_macd, df_sma, df_bb, df_bi
    df.rename(columns={'RSI_2': 'RSI'}, inplace=True)
    df.fillna(0)
    for col in df.columns[1:]:
        df[col] = np.round(df[col], 2)
    while save_data:
        df.to_csv('data.csv', index=False)
        break
    return df


def get_coin_price(coin='bitcoin'):
    price = cg.get_price(ids=coin, vs_currencies='usd')[coin]['usd']
    return price

