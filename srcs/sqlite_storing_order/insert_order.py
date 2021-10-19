#!/usr/bin/python3

import os
import sys
import sqlalchemy
import pandas as pd

SQLite_dir = 'SQLiteDB/'

# Create Frame to insert order in SQL format

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