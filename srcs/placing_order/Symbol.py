#!/usr/bin/python3

import ta
import sys
import math
import numpy as np
import pandas as pd
from time import sleep
from . import McTrade
from binance.client import Client
from binance.exceptions import BinanceAPIException
from ..fetching_symbols import fetching_symbols as fetch_symb
from ..sqlite_storing_order import insert_order as insert_order
from ..sqlite_storing_order import retrieve_order as retrieve_order

class Symbol:
    def __init__(self, config, client):
        self.symbol = config['symbol']
        self.coin = config['symbol'][:-4]
        self.quote = 'USDT'
        self.risk = config['risk']
        self.quantity = config['quantity']
        self.client = client

        self.coin_floor_quantity = self.get_quantity_precision(self.symbol)
        self.quote_floor_quantity = 2

        self.interval = config['interval']
        self.lookback = config['lookback']

        self.get_last_open_position()

        self.data_frame = fetch_symb.get_data_frame(self.client, self.symbol, self.interval, self.lookback)


    def ret_usdt_wallet():
        res = 0.0
        for name, values in usdt_wallet.items():
            res += float(values)
        return res

    def get_last_open_position(self):
        self.open_position_price = retrieve_order.get_last_open_position_price(self.symbol)
        if self.open_position_price > 0:
            self.open_position = True
        else:
            self.open_position = False

    def get_floor_quantity(self, quantity, precision):
        return (math.floor(quantity * (10 ** precision))) / 10 ** precision
    
    def get_quantity_precision(self, symbol):
        size = 8
        for i in self.client.get_symbol_info(symbol)['filters']:
            if i['filterType'] == 'LOT_SIZE':
                min_quantity = math.floor(float(i['minQty']) * 100000000)
                while min_quantity != 1:
                    min_quantity /= 10
                    size -= 1
                break
        return size

    def update_data_frame(self):
        self.data_frame = fetch_symb.get_data_frame(self.client, self.symbol, self.interval, self.lookback)
        self.caculate_stoch_rsi_macd()
    
    
    def caculate_stoch_rsi_macd(self):
        self.data_frame['K'] = ta.momentum.stoch(self.data_frame.High, self.data_frame.Low, self.data_frame.Close, window=14, smooth_window=3)
        self.data_frame['D'] = self.data_frame['K'].rolling(3).mean()
        self.data_frame['RSI'] = ta.momentum.rsi(self.data_frame.Close, window=14)
        self.data_frame['MACD'] = ta.trend.macd_diff(self.data_frame.Close)
        self.data_frame.dropna(inplace=True)

    def get_trigger(self, buy=True):
        data_frame_trigger = pd.DataFrame()
        for i in range (self.risk + 1):
            if buy:
                mask = (self.data_frame['K'].shift(i) < 20) & (self.data_frame['D'].shift(i) < 20)
            else:
                mask = (self.data_frame['K'].shift(i) > 80) & (self.data_frame['D'].shift(i) > 80)
            data_frame_trigger = data_frame_trigger.append(mask, ignore_index=True)
        return data_frame_trigger.sum(axis=0)

    def buy_sell_trigger(self):
        self.data_frame['Buy_trigger'] = np.where(self.get_trigger(), 1, 0)
        self.data_frame['Sell_trigger'] = np.where(self.get_trigger(buy=False), 1, 0)

    def decide(self):
        self.buy_sell_trigger()
        self.data_frame['Buy'] =    np.where((self.data_frame.Buy_trigger) &
                                    (self.data_frame['K'].between(20, 80)) & 
                                    (self.data_frame['D'].between(20, 80)) & 
                                    (self.data_frame.RSI > 50) & 
                                    (self.data_frame.MACD > 0), 1, 0)
        self.data_frame['Sell'] =   np.where((self.data_frame.Sell_trigger) &
                                    (self.data_frame['K'].between(20, 80)) & 
                                    (self.data_frame['D'].between(20, 80)) & 
                                    (self.data_frame.RSI < 50) & 
                                    (self.data_frame.MACD < 0), 1, 0)

    def get_possible_quantity():
        balance = self.client.get_asset_balance(asset=self.quote)
        quantity = (float(balance['free']) + self.ret_usdt_wallet()) * (self.quantity / 100)
        quantity = self.get_floor_quantity(self.quote, self.quote_floor_quantity)
        usdt_wallet[self.symbol] = str(quantity)
        quantity = quantity / self.data_frame.Close.iloc[:-1][-1] * 100 / 100
        return self.get_floor_quantity(self.coin, self.coin_floor_quantity)

    def place_order(self, side, order_type=Client.ORDER_TYPE_MARKET):
        mutex.acquire()
        if side == 'SELL':
            quantity = self.open_position_price
            self.open_position_price = 0
            usdt_wallet[self.symbol] = '0'
        else:
            quantity = self.get_possible_quantity()
            self.open_position_price = quantity
        try :
            order = self.client.create_order(symbol=self.symbol, side=side, type=order_type, quantity=quantity)
        except BinanceAPIException as e:
            mutex.release()
            print(e)
            print("Error: couldn't place order for symbol " + self.symbol + " side " + side + " for " + quantity)
            return False
        mutex.release()
        sell_price = float(order['fills'][0]['price'])
        insert_sql_order.insert_sql_data(order)

    def strategy(self):
        self.update_data_frame()
        self.decide()
        print(self.data_frame.iloc[-1])
        if self.open_position == False and self.data_frame.Buy.iloc[-1]:
            self.open_position = True
            return self.buying_order(Client.SIDE_BUY)
        elif self.open_position == True and self.data_frame.Sell.iloc[-1]:
            self.open_position = False
            return self.selling_order(Client.SIDE_SELL)
        return True
    
    def main_loop(self):
        while True:
            if self.strategy() == False:
                return
            sleep(2)
