#!/usr/bin/python3

import os
import sys
import math
import threading
import ta
import time
import pandas as pd
import numpy as np
from time import sleep
from .Signal import Signals
from binance.client import Client
from binance.exceptions import BinanceAPIException
from BinanceSymbolFetching import fetching_symbols as fetch_symb
from . import utils as ut

usdt_wallet = {}
mutex = threading.Lock()

# Return the sum of each symbol within the mutex sharing the same wallet

def ret_usdt_wallet(usdt_wallet):
    res = 0.0
    for name, values in usdt_wallet.items():
        res += float(values)
    return res

# Buy when Rsi > 50, K and D < 80 && > 20, MACD > 0, Buying Trigger

def buying_order(symbol, client, data_frame, side=Client.SIDE_BUY, order_type=Client.ORDER_TYPE_MARKET):
    mutex.acquire()
    balance = client.get_asset_balance(asset='USDT')
    quantity = (float(balance['free']) + ret_usdt_wallet(usdt_wallet)) * (symbol['quantity'] / 100)
    quantity = ut.get_floor_quantity('USDT', quantity, client)
    usdt_wallet[symbol['symbol']] = str(quantity)
    quantity = quantity / data_frame.Close.iloc[:-1][-1] * 100 / 100
    quantity = ut.get_floor_quantity(symbol['symbol'], quantity, client)
    print(quantity)
    try:
        order = client.create_order(symbol=symbol['symbol'], side=side, type=order_type, quantity=quantity)
    except BinanceAPIException as e:
        print(e)
        mutex.release()
        return False
    mutex.release()
    buy_price = float(order['fills'][0]['price'])
    print(buy_price)
    print(order)
    print("Buying")
    fetch_symb.insert_sql_data(order)
    return True

# Sell when Rsi < 50, K and D < 80 && > 20, MACD < 0, Selling Trigger

def selling_order(symbol, client, data_frame, side=Client.SIDE_SELL, order_type=Client.ORDER_TYPE_MARKET):
    balance = client.get_asset_balance(asset=symbol['symbol'][:-4])
    quantity = ut.get_floor_quantity(symbol['symbol'], float(balance['free']), client)
    print(quantity)
    try:
        order = client.create_order(symbol=symbol['symbol'], side=side, type=order_type, quantity=quantity)
    except BinanceAPIException as e:
        print(e)
        return False
    mutex.acquire()
    usdt_wallet[symbol['symbol']] = '0'
    mutex.release()
    sell_price = float(order['fills'][0]['price'])
    print(sell_price)
    print(order)
    print("Selling")
    fetch_symb.insert_sql_data(order)
    return True

# Only selling when open position, and buying when no open position, 30m interval and 14 day lookback

def strategy(symbol, client, open_position=False):
    data_frame = fetch_symb.get_data_frame(client, symbol['symbol'], "30m", '14 day ago UTC')
    ut.caculate_stoch_rsi_macd(data_frame)
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

# Main loop for each thread using mutex to share the same wallet   

def loop_thread_strat(symbol, client):
    global usdt_wallet

    mutex.acquire()
    usdt_wallet[symbol['symbol']] = '0'
    mutex.release()
    while True:
        if strategy(symbol, client) == False:
            return
        sleep(2)

# Connecting to the client then starting each thread/symbol

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
        threads.append(threading.Thread(target=loop_thread_strat, args=(symbol, client, ), daemon=True))

    # Starting the threads

    for tmp_thread in threads:
        tmp_thread.start()

    # Joining the threads
    try:
        for tmp_thread in threads:
            tmp_thread.join()
    except KeyboardInterrupt:
        print("Successfully exited from all threads, (need to implements conclusion) ")
        sys.exit(1)
    