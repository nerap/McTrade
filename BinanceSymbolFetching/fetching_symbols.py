#!/usr/bin/python3

import os
import time
import json
import _thread
import sqlalchemy
import sys
import pandas as pd
import requests as rq

# Reformate the json response "res" to a pandas DataFrame 

def get_data_frame(client, symbol, interval, lookback):
    try:
        data_frame = pd.DataFrame(client.get_historical_klines(symbol, interval, lookback))
    except BinanceAPIException as e:
        print(e)
        sleep(60)
        data_frame = pd.DataFrame(client.get_historical_klines(symbol, interval, lookback))
    data_frame = data_frame.iloc[:, :6]
    data_frame.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    data_frame = data_frame.set_index('Time')
    data_frame.index = pd.to_datetime(data_frame.index, unit="ms")
    data_frame = data_frame.astype(float)
    return data_frame

# Transforming DataFrame into SQLite data

def storing_price_symbol(symbol):
    engine = sqlalchemy.create_engine('sqlite:///' + SQLite_dir + symbol + 'stream.db')
    while True:
        res = rq.get(url_binance_ticker_price + symbol).json()
        data_frame = create_frame(res)
        data_frame.to_sql(symbol, engine, if_exists='append', index=False)
        print(data_frame)

# Starting a Thread for each symbol in the configuration file

def fetching_symbols(symbols):
    if not os.path.exists(SQLite_dir):
        os.makedirs(SQLite_dir)
    else:
        for f in os.listdir(SQLite_dir):
            os.remove(os.path.join(SQLite_dir, f))
    for symbol in symbols:
        try:
            _thread.start_new_thread( storing_price_symbol, (symbol , ))
        except ValueError as e:
            print('Error: Thread unable to start')
            sys.exit(1)
    while True:
        time.sleep(0.100)
        pass
    print('Every thread is working')