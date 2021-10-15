import os
from binance.client import Client
import pandas as pd
import time
import pprint
import numpy as np
import matplotlib.pyplot as plt
import requests as rq
import ta
from time import sleep
from binance.exceptions import BinanceAPIException


def get_data_frame(client, symbol, interval, lookback):
    try:
        df = pd.DataFrame(client.get_historical_klines(symbol, interval, lookback + ' min ago UTC'))
    except BinanceAPIException as e:
        print(e)
        sleep(60)
        df = pd.DataFrame(client.get_historical_klines(symbol, interval, starttime))
    df = df.iloc[:, :6]
    df.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    df = df.set_index('Time')
    df.index = pd.to_datetime(df.index, unit="ms")
    return df.astype(float)

def macd(symbol, qty, client, open_position=False):
    while True:
        df = get_data_frame(client, symbol)
        if not open_position:
            if ta.trend.macd_diff(df.Close).iloc[-1] > 0 and ta.trend.macd_diff(df.Close).iloc[-2] < 0:
                buy_price = int(client.get_symbol_ticker(symbol=symbol)) * qty
                print("Buy at : " + str(buy_price))
                open_position = True
                break
    if open_position:
        while True:
            df = get_data_frame(client, symbol)
            if ta.trend.macd_diff(df.Close).iloc[-1] < 0 and ta.trend.macd_diff(df.Close).iloc[-2] > 0:
                sell_price = int(client.get_symbol_ticker(symbol=symbol)) * qty
                print("Selling at : " + str(sell_price))
                open_position = False
                break
    print(f'profit = {(sell_price - buy_price)/buy_price}')
        


def applytechnicals(df):
    df['%K'] = ta.momentum.stoch(df.High, df.Low, df.Close, window=14, smooth_window=3)
    df['%D'] = df['%K'].rolling(3).mean()
    df['rsi'] = ta.momentum.rsi(df.Close, window=14)
    df['macd'] = ta.trend.macd_diff(df.Close)
    df.dropna(inplace=True)



class Signals:
        def __init__(self, df, lags):
            self.df = df
            self.lags = lags
        
        def gettriger(self):
            dfx = pd.DataFrame()
            for i in range (self.lags + 1):
                mask = (self.df['%K'].shift(i) < 20) & (self.df['%D'].shift(i) < 20)
                dfx = dfx.append(mask, ignore_index=True)
            return dfx.sum(axis=0)

        def decide(self):
            self.df['trigger'] = np.where(self.gettriger(), 1, 0)
            self.df['Buy'] = np.where((self.df.trigger) & (self.df['%K'].between(20,80)) & (self.df['%D'].between(20, 80)) & (self.df.rsi > 50) & (self.df.macd > 0), 1, 0)



def strategy(symbol, qty, client, open_position=False):
    df = get_data_frame(client, symbol, "1m", '100')
    applytechnicals(df)
    inst = Signals(df, 25)
    inst.decide()
    file_object = open('sample.txt', 'a')
    print(f'current Close is ' + str(df.Close.iloc[-1]))
    if (df.Buy.iloc[-1]):
        buy_price = float(client.get_symbol_ticker(symbol=symbol)['price']) * qty
        print("Buy at : " + str(buy_price))
        open_position = True
    while open_position:
        time.sleep(0.5)
        df = get_data_frame(client, symbol, "1m", '2')
        print(f'current Close is ' + str(df.Close.iloc[-1]))
        print(f'current Target is ' + str(buy_price * 1.0005))
        print(f'current Stop is ' + str(buy_price * 0.995))
        if df.Close[-1] <= buy_price * 0.995 or df.Close[-1] >= 1.005 * buy_price:
            sell_price = float(client.get_symbol_ticker(symbol=symbol)['price']) * qty
            print("sell at : " + str(sell_price))
            file_object.write(str(df.Time[-1]) + " Profit :" + str((sell_price - buy_price)) * "\n")
            file_object.close()
            break

def main():
    api_key = os.environ.get('api_key')
    secret_api_key = os.environ.get('secret_api_key')
    symbol = "BTCUSDT"
    client = Client(api_key, secret_api_key)
    while True:
        strategy(symbol, 0.1, client)
        #sleep(0.5)
    #print(df)
    