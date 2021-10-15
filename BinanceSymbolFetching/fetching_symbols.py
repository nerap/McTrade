#!/usr/bin/python3

import os
import time
import json
import _thread
import sqlalchemy
import sys
import pandas as pd
import requests as rq

SQLite_dir = 'SQLiteDB/'
url_binance_ticker_price = "https://api.binance.com/api/v3/ticker/price?symbol="

# Reformate the json response "res" to a pandas DataFrame 

def create_frame(res):
    df = pd.DataFrame([{"symbol": res["symbol"],
                        "datetime": int(time.time()),
                        "price": float(res["price"]) }])
    df.columns = ['Symbol', 'Time', 'Price']
    df.Price = df.Price.astype(float)
    df.Time = pd.to_datetime(int(time.time() * 1000), unit="ms")
    return (df)

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