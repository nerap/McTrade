import os
from binance.client import Client
import pandas as pd
import time
import pprint
import numpy as np
import matplotlib.pyplot as plt
import requests as rq
import _thread
import ta
from time import sleep
from binance.exceptions import BinanceAPIException
from BinanceSymbolFetching import fetching_symbols as fs


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
            self.df['Buy'] =    np.where((self.df.trigger) &
                                (self.df['%K'].between(20,80)) & 
                                (self.df['%D'].between(20, 80)) & 
                                (self.df.rsi > 50) & 
                                (self.df.macd > 0), 1, 0)



def strategy(symbol, qty, client, open_position=False):
    df = fs.get_data_frame(client, symbol, "1m", '100')
    applytechnicals(df)
    inst = Signals(df, 5)
    inst.decide()
    file_object = open(symbol, 'a')
    print(f'current Close is ' + str(df.Close.iloc[-1]))
    if (df.Buy.iloc[-1]):
        order = client.create_order(symbol=symbol, side="BUY", type="MARKET", quantity=qty)
        buy_price = float(order['fills'][0]['price'])
        print(order)
        open_position = True
    while open_position:
        time.sleep(0.5)
        df = fs.get_data_frame(client, symbol, "1m", '2')
        print(f'current Close is ' + str(df.Close.iloc[-1]))
        print(f'current Target is ' + str(buy_price * 1.005))
        print(f'current Stop is ' + str(buy_price * 0.995))
        if df.Close[-1] <= (buy_price * 0.995) or df.Close[-1] >= (buy_price * 1.005):
            order = client.create_order(symbol=symbol, side="SELL", type="MARKET", quantity=qty)
            sell_price = float(order['fills'][0]['price'])
            file_object.write(str((sell_price - buy_price) * qty) +  "\n")
            file_object.close()
            break



def thread(symbol, qty, client):
    while True:
        strategy(symbol, qty, client)
        sleep(0.5)


def main():
    api_key = os.environ.get('api_key')
    secret_api_key = os.environ.get('secret_api_key')
    symbol = "ETHUSDT"
    client = Client(api_key, secret_api_key)
    #df = get_data_frame(client, symbol, "1m", '100')
    #applytechnicals(df)
    #inst = Signals(df, 5)
    #inst.decide()
    #print(df[df.Buy == 1])
    
    _thread.start_new_thread( thread, (symbol, 0.0080, client, ))
    while True:
        pass
    #print(df)
    