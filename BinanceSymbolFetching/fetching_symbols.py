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

# Get last open position price reading the SQLite file with the associated symbol

def get_last_open_position_price(symbol):
    try:
        if not os.path.exists(SQLite_dir):
            os.makedirs(SQLite_dir)
        if not os.path.exists(SQLite_dir + symbol + 'stream.db'):
            return 0
        engine = sqlalchemy.create_engine('sqlite:///' + SQLite_dir + symbol + 'stream.db')
        data_frame = pd.read_sql(symbol, engine)
        if data_frame.empty or data_frame[-1:]['Side'].values[0] == 'SELL':
            return 0
        else:
            return data_frame[-1:]['CummulativeQuoteQty'].values[0]
    except ValueError as e:
        print(e)
        print('Error : SQLachlchemy couldn\'t create engine when getting last price on open position')
        raise e

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

def create_frame(order):
    data_frame = pd.DataFrame([{"symbol": order['symbol'],
                                "orderId": order['orderId'],
                                "time": order['transactTime'],
                                'price': float(order['fills'][0]['price']),
                                'qty': float(order['fills'][0]['qty']),
                                'cummulativeQuoteQty': float(order['cummulativeQuoteQty']),
                                'type': order['type'],
                                'side': order['side'],
                                'commission': float(order['fills'][0]['commission']) }])
    data_frame.columns = ['Symbol', 'OrderId', 'Time', 'Price', 'Qty', 'CummulativeQuoteQty', 'Type', 'Side', 'Commission']
    data_frame.Price = data_frame.Price.astype(float)
    data_frame.Qty = data_frame.Qty.astype(float)
    data_frame.CummulativeQuoteQty = data_frame.CummulativeQuoteQty.astype(float)
    data_frame.Commission = data_frame.Commission.astype(float)
    data_frame.Time = pd.to_datetime(data_frame.Time, unit="ms")
    return (data_frame)

# Transforming DataFrame into SQLite data

def storing_order(order):
    try:
        engine = sqlalchemy.create_engine('sqlite:///' + SQLite_dir + order['symbol'] + 'stream.db')
        data_frame = create_frame(order)
        data_frame.to_sql(order['symbol'], engine, if_exists='append', index=False)
        print(data_frame)
    except ValueError as e:
        print(e)
        print('Error : SQLachlchemy couldn\'t create engine when storing order')
        raise e

# Starting a Thread for each symbol in the configuration file

def insert_sql_data(order):
    if not os.path.exists(SQLite_dir):
        os.makedirs(SQLite_dir)
    try:
        storing_order(order)
    except ValueError as e:
        print('Error: SQLite couldn\'t store data')
        sys.exit(1)