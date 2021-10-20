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

        # Check if SQLite dir and the stored file is here

        if not os.path.exists(SQLite_dir):
            os.makedirs(SQLite_dir)
        if not os.path.exists(SQLite_dir + symbol + 'stream.db'):
            return [0, 0]

        # Creating the engine linking

        engine = sqlalchemy.create_engine('sqlite:///' + SQLite_dir + symbol + 'stream.db')
        data_frame = pd.read_sql(symbol, engine)

        # Check if the last row is a SELL order, if it is, then we have no open position

        if data_frame.empty or data_frame[-1:]['Side'].values[0] == 'SELL':
            return [0, 0]
        else:
            return [data_frame[-1:]['CummulativeQuoteQty'].values[0], data_frame[-1:]['Qty'].values[0]]
    except ValueError as e:
        print(e)
        print('Error : SQLachlchemy couldn\'t create engine when getting last price on open position')
        raise e