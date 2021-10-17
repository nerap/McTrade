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


# Reformate the json response "res" to a pandas DataFrame 

def get_data_frame(client, symbol, interval, lookback):
    try:
        df = pd.DataFrame(client.get_historical_klines(symbol, "30m", '14 day ago UTC'))
    except BinanceAPIException as e:
        print(e)
        sleep(60)
        df = pd.DataFrame(client.get_historical_klines(symbol, "30m", '14 day ago UTC'))
    df = df.iloc[:, :6]
    df.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    df = df.set_index('Time')
    df.index = pd.to_datetime(df.index, unit="ms")
    df = df.astype(float)
    return df



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
        
        def gettriger(self, buy=True):
            dfx = pd.DataFrame()
            for i in range (self.lags + 1):
                if buy:
                    mask = (self.df['%K'].shift(i) < 20) & (self.df['%D'].shift(i) < 20)
                else:
                    mask = (self.df['%K'].shift(i) > 80) & (self.df['%D'].shift(i) > 80)
                dfx = dfx.append(mask, ignore_index=True)
            return dfx.sum(axis=0)

        def decide(self):
            self.df['Buytrigger'] = np.where(self.gettriger(), 1, 0)
            self.df['Selltrigger'] = np.where(self.gettriger(buy=False), 1, 0)
            self.df['Buy'] =    np.where((self.df.Buytrigger) &
                                (self.df['%K'].between(20, 80)) & 
                                (self.df['%D'].between(20, 80)) & 
                                (self.df.rsi > 50) & 
                                (self.df.macd > 0), 1, 0)
            self.df['Sell'] =    np.where((self.df.Selltrigger) &
                                (self.df['%K'].between(20, 80)) & 
                                (self.df['%D'].between(20, 80)) & 
                                (self.df.rsi < 50) & 
                                (self.df.macd < 0), 1, 0)



def strategy(symbol, qty, client, open_position=False):
    df = get_data_frame(client, symbol, "1h", '14')
    applytechnicals(df)
    inst = Signals(df, 5)
    inst.decide()
    file_object = open(symbol, 'a')
    print(df.iloc[-1])
    if (df.Buy.iloc[-1]):
        order = client.create_order(symbol=symbol, side="BUY", type="MARKET", quantity=qty)
        buy_price = float(order['fills'][0]['price'])
        print(order)
        open_position = True
    while open_position:
        time.sleep(2)
        df = get_data_frame(client, symbol, "1h", '14')
        print(df.iloc[-1])
        if (df.Buy.iloc[-1]):
            order = client.create_order(symbol=symbol, side="SELL", type="MARKET", quantity=qty)
            sell_price = float(order['fills'][0]['price'])
            print ("HELLO")
            file_object.write(str((sell_price - buy_price) * qty) +  "\n")
            file_object.close()
            break



def thread(symbol, qty, client):
    while True:
        strategy(symbol, qty, client)
        sleep(2)


def main():
    api_key = os.environ.get('api_key')
    secret_api_key = os.environ.get('secret_api_key')
    symbol = "ETHUSDT"
    client = Client(api_key, secret_api_key)
    #df = pd.DataFrame(client.get_historical_klines(symbol, "1h", '14 day ago UTC'))
    #df = get_data_frame(client, symbol, "1m", '100')
    #applytechnicals(df)
    #inst = Signals(df, 5)
    #inst.decide()
    #print(df[df.Buy == 1])
    
    thread(symbol, 0.1, client)
    #_thread.start_new_thread( thread, (symbol, 0.1, client, ))
    #while True:
    #    pass
   # print(df)
    