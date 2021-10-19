#!/usr/bin/python3

import pandas as pd

# Getting the historical data of a certain symbol overtime
# @Return : the data in pandas.DataFrame format

def get_data_frame(client, symbol, interval, lookback):

    # Convert all the data from BinanceAPI to DataFrame format
    # Symbol : -> "BTCUSDT", "ETHUSDT", "COMPBUSD", etc..
    # Interval : Time spent between each data such as -> "1m", "30m", "1h", etc..
    # Lookback : How far you want to get the data, "100m", "3 day ago UTC", "1w", etc..

    try:

        data_frame = pd.DataFrame(client.get_historical_klines(symbol, interval, lookback))

    except BinanceAPIException as e:
    
    # After a certain time the client might timeout, so we catch it and restart after 60 seconds

        print(e)
        sleep(60)
        data_frame = pd.DataFrame(client.get_historical_klines(symbol, interval, lookback))

    # Remove the 6 last columns considered useless to McTrade and waste of time to keep them
    
    data_frame = data_frame.iloc[:, :6]

    data_frame.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    
    # Convert timestamp column to datetime format, for readable purpose
    
    data_frame = data_frame.set_index('Time')
    data_frame.index = pd.to_datetime(data_frame.index, unit="ms")

    # Value in the DataFrame should be in float format for obvious reason

    data_frame = data_frame.astype(float)

    return data_frame
