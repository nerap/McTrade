import os
import sys
import math
import ta
import pandas as pd
from binance.client import Client

#Calculate all signals K momentum
#RSI 14D
#MACD 14D

def caculate_stoch_rsi_macd(data_frame):
    data_frame['K'] = ta.momentum.stoch(data_frame.High, data_frame.Low, data_frame.Close, window=14, smooth_window=3)
    data_frame['D'] = data_frame['K'].rolling(3).mean()
    data_frame['RSI'] = ta.momentum.rsi(data_frame.Close, window=14)
    data_frame['MACD'] = ta.trend.macd_diff(data_frame.Close)
    data_frame.dropna(inplace=True)

#Return the right quantity for Binance API, with the right precision of the symbol

def get_floor_quantity(symbol, quantity, client):
    res = client.get_symbol_info(symbol)
    size = 8
    if symbol == 'USDT':
        return (math.floor(quantity * (10 ** 2))) / 10 ** 2 
    for i in res['filters']:
        if i['filterType'] == 'LOT_SIZE':
            temp = math.floor(float(i['minQty']) * 100000000)
            while temp != 1:
                temp /= 10
                size -= 1
            quantity = (math.floor(quantity * (10 ** size))) / 10 ** size
            break
    return quantity