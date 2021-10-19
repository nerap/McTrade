#!/usr/bin/python3

import pandas as pd

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
