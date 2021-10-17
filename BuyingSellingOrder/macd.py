#!/usr/bin/python3

import os
import sys
from binance.client import Client
import pandas as pd
import time
import pprint
import numpy as np
import matplotlib.pyplot as plt
import requests as rq
import math
import threading
import ta
from time import sleep
from binance.exceptions import BinanceAPIException
from BinanceSymbolFetching import fetching_symbols as fetch_symb

class Signals:
        def __init__(self, data_frame, steps):
            self.data_frame = data_frame
            self.steps = steps
        
        def get_trigger(self, buy=True):
            data_frame_trigger = pd.DataFrame()
            for i in range (self.steps + 1):
                if buy:
                    mask = (self.data_frame['K'].shift(i) < 20) & (self.data_frame['D'].shift(i) < 20)
                else:
                    mask = (self.data_frame['K'].shift(i) > 80) & (self.data_frame['D'].shift(i) > 80)
                data_frame_trigger = data_frame_trigger.append(mask, ignore_index=True)
            return data_frame_trigger.sum(axis=0)

        def buy_sell_trigger(self):
            self.data_frame['Buy_trigger'] = np.where(self.get_trigger(), 1, 0)
            self.data_frame['Sell_trigger'] = np.where(self.get_trigger(buy=False), 1, 0)

        def decide(self):
            self.buy_sell_trigger()
            self.data_frame['Buy'] =    np.where((self.data_frame.Buy_trigger) &
                                        (self.data_frame['K'].between(20, 80)) & 
                                        (self.data_frame['D'].between(20, 80)) & 
                                        (self.data_frame.RSI > 50) & 
                                        (self.data_frame.MACD > 0), 1, 0)
            self.data_frame['Sell'] =   np.where((self.data_frame.Sell_trigger) &
                                        (self.data_frame['K'].between(20, 80)) & 
                                        (self.data_frame['D'].between(20, 80)) & 
                                        (self.data_frame.RSI < 50) & 
                                        (self.data_frame.MACD < 0), 1, 0)


def applytechnicals(df):
    df['K'] = ta.momentum.stoch(df.High, df.Low, df.Close, window=14, smooth_window=3)
    df['D'] = df['K'].rolling(3).mean()
    df['RSI'] = ta.momentum.rsi(df.Close, window=14)
    df['MACD'] = ta.trend.macd_diff(df.Close)
    df.dropna(inplace=True)


def get_floor_quantity(symbol, quantity, client):
    res = client.get_symbol_info(symbol)
    size = 8
    if symbol == 'USDT':
        return (math.floor(quantity * (10 ** 2))) / 10 ** 2 
    for i in res['filters']:
        if i['filterType'] == 'LOT_SIZE':
            temp = float(i['minQty']) * 100000000
            while temp != 1:
                temp /= 10
                size -= 1
            quantity = (math.floor(quantity * (10 ** size))) / 10 ** size
            break
    return quantity

def buying_order(symbol, client, data_frame, side=Client.SIDE_BUY, order_type=Client.ORDER_TYPE_MARKET):
    balance = client.get_asset_balance(asset='USDT')
    quantity = float(balance['free']) * (symbol['quantity'] / 100)
    quantity = get_floor_quantity('USDT', quantity, client) 
    quantity = quantity / data_frame.Close.iloc[:-1][-1] * 100 / 100
    quantity = get_floor_quantity(symbol['symbol'], quantity, client)
    print(quantity)
    try:
        order = client.create_order(symbol=symbol['symbol'], side=side, type=order_type, quantity=quantity)
    except BinanceAPIException as e:
        print(e)
        return False
    buy_price = float(order['fills'][0]['price'])
    print(buy_price)
    print(order)
    print("Buying")
    return True

def selling_order(symbol, client, data_frame, side=Client.SIDE_SELL, order_type=Client.ORDER_TYPE_MARKET):
    balance = client.get_asset_balance(asset=symbol['symbol'][:-4])
    quantity = get_floor_quantity(symbol['symbol'], float(balance['free']), client)
    print(quantity)
    try:
        order = client.create_order(symbol=symbol['symbol'], side=side, type=order_type, quantity=quantity)
    except BinanceAPIException as e:
        print(e)
        return False
    sell_price = float(order['fills'][0]['price'])
    print(sell_price)
    print(order)
    print("Selling")
    return True

def strategy(symbol, client, open_position=False):
    data_frame = fetch_symb.get_data_frame(client, symbol['symbol'], "30m", '14 day ago UTC')
    applytechnicals(data_frame)
    inst = Signals(data_frame, symbol['risk'])
    inst.decide()
    print(data_frame.iloc[-1])
    if (data_frame.Buy.iloc[-1]):
        if buying_order(symbol, client, data_frame) == False:
            return False
        open_position = True
    while open_position:
        time.sleep(2)
        data_frame = fetch_symb.get_data_frame(client, symbol['symbol'], "30m", '14 day ago UTC')
        print(data_frame.iloc[-1])
        if (data_frame.Sell.iloc[-1]):
            return selling_order(symbol, client, data_frame)
            

def loop_thread_strat(symbol, client):
    while True:
        if strategy(symbol, client) == False:
            return
        sleep(2)

def starting_loop_order(symbols):
    api_key = os.environ.get('api_key')
    secret_api_key = os.environ.get('secret_api_key')

    try:
        client = Client(api_key, secret_api_key)
    except BinanceAPIException as e:
        print(e)
        print("Error: cannot create a connection to Binance with those api_key")
        sys.exit(1)

    # Creating the threads
    
    threads = []
    for symbol in symbols:
        threads.append(threading.Thread(target=loop_thread_strat, args=(symbol, client, )))

    # Starting the threads

    for tmp_thread in threads:
        tmp_thread.start()

    # Joining the threads

    for tmp_thread in threads:
        tmp_thread.join()
    