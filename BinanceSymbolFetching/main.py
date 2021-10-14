#!/usr/bin/python3

import sys, getopt
import pandas as pd
import requests as rq
from datetime import datetime
import time
import sqlalchemy

bot = sys.argv[0]
url_binance_ticker_price = "https://api.binance.com/api/v3/ticker/price?symbol="


def parse_symbol(symbol):
    res = rq.get(url_binance_ticker_price + symbol).json()
    if 'msg' in res:
        print('Symbol is not valid for BinanceBot check your parameters')
        print(res["msg"])
        print("Return Code : " + str(res["code"]))
        sys.exit(1)
    elif symbol == "error" or symbol == "":
        print('Symbol is not valid for BinanceBot check your parameters')
        sys.exit(1)
    return symbol

def parse_entry(argv):
    symbol = "error"
    try:
        opts, args = getopt.getopt(argv, "hs:", ["help", "symbol="])
    except getopt.GetoptError:
        print ('python3 ' + bot + ' -s <symbol> or --symbol=<symbol>')
        print ('python3 ' + bot + ' -h or --help')
        sys.exit(1)
    if len(opts) <= 0:
        print ('python3 ' + bot + ' -s <symbol> or --symbol=<symbol>')
        print ('python3 ' + bot + ' -h or --help')
        sys.exit(1)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print ('python3 ' + bot + ' -s <symbol>')
            sys.exit(0)
        elif opt in ('-s', '--symbol'):
            symbol = arg
    return parse_symbol(symbol)

def create_frame(res):
    data_frame = pd.DataFrame([{"symbol": res["symbol"],
                        "datetime": int(time.time()),
                        "price": float(res["price"]) }])
    data_frame.columns = ['Symbol', 'Time', 'Price']
    data_frame.Price = df.Price.astype(float)
    data_frame.Time = pd.to_datetime(int(time.time() * 1000), unit="ms")
    return (data_frame)


if __name__ == "__main__":
    symbol = parse_entry(sys.argv[1:])
    print(symbol)
    #engine = sqlalchemy.create_engine('sqlite:///SQLiteDB/' + symbol + 'stream.db')
    #while True:
        #res = rq.get("https://api.binance.com/api/v3/ticker/price?symbol=" + symbol).json()
        #data_frame = create_frame(res)
        #data_frame.to_sql(symbol, engine, if_exists='append', index=False)
        #print(data_frame)
