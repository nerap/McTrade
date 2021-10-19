#!/usr/bin/python3

import os
import sys
import sqlalchemy
import pandas as pd

# Which directory all the SQLite data will be stored

SQLite_dir = 'SQLiteDB/'

# Create Frame to insert order in SQL format
# into SQLite_dir variable
# @Return : the data in pandas.DataFrame format

def create_frame(order):

    # Converting order json response to DataFrame taking all columns that we need for futher usage

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

    # Converting data_frame values to float for obvious reason

    data_frame.Price = data_frame.Price.astype(float)
    data_frame.Qty = data_frame.Qty.astype(float)
    data_frame.CummulativeQuoteQty = data_frame.CummulativeQuoteQty.astype(float)
    data_frame.Commission = data_frame.Commission.astype(float)

    # Converting timestamp to datetime for more readable purpose

    data_frame.Time = pd.to_datetime(data_frame.Time, unit="ms")

    return (data_frame)

# Transforming DataFrame into SQLite data
# and store it into SQLite_folder

def storing_order(order):

    try:
        # Creating SQLite engine int SQLite_dir with "symbol" + "stream.db" as filename

        engine = sqlalchemy.create_engine('sqlite:///' + SQLite_dir + order['symbol'] + 'stream.db')
        
        # Formating the json response order in pandas.DataFrame format

        data_frame = create_frame(order)

        # Converting the DataFrame to SQL format

        data_frame.to_sql(order['symbol'], engine, if_exists='append', index=False)

    except ValueError as e:
        print(e)
        print('Error : SQLachlchemy couldn\'t create engine when storing order')
        raise e

# Insert order into SQL format in SQLite_dir 

def insert_sql_data(order):

    # Creating SQLite_dir is deleting or not created

    if not os.path.exists(SQLite_dir):
        os.makedirs(SQLite_dir)
    try:

        # Converting order (JSON) to SQL format

        storing_order(order)
        
    except ValueError as e:
        print('Error: SQLite couldn\'t store data')
        sys.exit(1)