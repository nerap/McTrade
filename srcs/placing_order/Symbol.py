#!/usr/bin/python3

import ta
import os
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

usdt_wallet = {}

# An Symbol is created for each symbol configurated in the config file

class Symbol:

    # Symbol is define with certain attribute such as :
    # symbol    -> "BTCUSCT", "ETHUSDT", "COMPUSDT", etc...
    # coin      -> "BTC", "ETH", "COMP", "DOGE", etc...
    # quote     -> "USDT" and only "USDT" for now
    # quantity  -> 5 >= quantity <= 100 (Max percentage of the wallet (quote currency))
    # coin_floor_precision -> the precision of the coin, must have to perform a transaction
    # quote_floor_precision -> the precision of the quote, must have to perform a transaction
    # interval  -> String representing the interval between each data we will fork, the quicker the interval is, the more reactive the bot will be, check https://python-binance.readthedocs.io/en/latest/constants.html
    # lookback  -> String representing how old your data will be, like interval, check https://python-binance.readthedocs.io/en/latest/constants.html, for more information
    # data_frame-> pandas.DataFrame current data used by the bot to know if we want to buy/sell or not with certain financial indicator
    # client    -> Binance Client
    #
    # Each of those attributes are mandatary for the bot to perform well

    def __init__(self, config, client, mutex):

        # Making sure that usdt_wallet is a global variable
        global usdt_wallet

        self.mutex = mutex
        self.client = client
        self.symbol = config['symbol']
        self.coin = config['symbol'][:-4]
        self.quote = 'USDT'
        self.quantity = config['quantity']
        self.get_last_open_position()
        self.mutex.acquire()

        # Instantiate Symbol object to init attributes

        # Retrieving open_position_price in Symbol object to make sure that
        # every symbol know how much quote is available
        usdt_wallet[self.symbol] = str(self.open_position_price)
        self.mutex.release()
        self.coin_floor_precision = self.get_quantity_precision(self.symbol)

        # For know the quote value is USDT so we know the exact precision
        self.quote_floor_precision = 2
        self.interval = config['interval']
        self.lookback = config['lookback']
        self.interval_validate = config['interval_validate']
        self.lookback_validate = config['lookback_validate']
    
    # Connect to Binance API with a Client

    def connect_binance_client(api_key, secret_api_key):

    # @Return Bincance Client object
        try:
            return Client(api_key, secret_api_key)
        except BinanceAPIException as e:
            print(e)
            print("Error: cannot create a connection to Binance with those api_key")
            sys.exit(1)

    # Sum up the USDT wallet
    # @Return the total wallet values as float 

    def ret_usdt_wallet(self):

        res = 0.0
        for name, values in usdt_wallet.items():
            res += float(values)
        return res

    # When we first execute we need to make sure that we have no open position from last time

    def get_last_open_position(self):
        
        # Retriveing the last price and the quantity of the last sell order 
        price_quantity = retrieve_order.get_last_open_position_price(self.symbol)
        self.open_position_price = price_quantity[0]
        self.open_position_quantity = price_quantity[1]
        if self.open_position_price > 0:
            self.open_position = True
        else:
            self.open_position = False
    
    # @Return as float the exact amount we have to put in the order

    def get_floor_quantity(self, quantity, precision):
        return (math.floor(quantity * (10 ** precision))) / 10 ** precision

    # @Return an int between 1 and 8 representing the precision of the coin or quote
    
    def get_quantity_precision(self, symbol):

        # Precision can't go higher than 8
        size = 8

        # Making GET request to get symbol info such as precision, minQty, etc..
        for filt in self.client.get_symbol_info(symbol)['filters']:

            # For some reason we need to loop to get minQty key
            if filt['filterType'] == 'LOT_SIZE':
                min_quantity = math.floor(float(filt['minQty']) * 100000000)
                while min_quantity != 1:
                    min_quantity /= 10
                    size -= 1
                break
        return size

    # Fetching all data we need and apply each finicial indicators we need
    
    def update_data_frame(self):
        try :
            self.data_frame = fetch_symb.get_data_frame(self.client, self.symbol, self.interval, self.lookback)
            self.data_frame_validate = fetch_symb.get_data_frame(self.client, self.symbol, self.interval_validate, self.lookback_validate)

        # After a while the client might reset or timeout, we are making sure to reconnect
        except BinanceAPIException as e:

            # Create a new client to make sure that everything is alright
            print(self.symbol + " is reconnecting to the client in 10 seconds")
            sleep(10)
            try :
                self.client = Symbol.connect_binance_client(os.environ.get('api_key'), os.environ.get('secret_api_key'))
                return self.update_data_frame()
            except BinanceAPIException as e:
                print(e)
                print("Error: the client can't connect to binance with those API Keys")
        self.caculate_macd()

    # Applying MACD algorithm 

    def caculate_macd(self):

        # Moving average convergence divergence (MACD) is a trend-following momentum
        # indicator that shows the relationship between two moving averages of a security’s price.
        # The MACD is calculated by subtracting the 26-period exponential 
        # moving average (EMA) from the 12-period EMA.

        # Formula :
        #
        #          MACD = N-Period EMA − N2-Period EMA
        #
        # Where N = 12 and N2 = 26 for example
        # MACD is calculated by subtracting the long-term EMA (26 periods) from the short-term EMA (12 periods).
        # An exponential moving average (EMA) is a type of moving average (MA)
        # that places a greater weight and significance on the most recent data point


        shortEMA = self.data_frame.Close.ewm(span=12, adjust=False).mean()
        longEMA = self.data_frame.Close.ewm(span=26, adjust=False).mean()

        self.data_frame['Macd'] = shortEMA - longEMA
        self.data_frame['Signal'] = self.data_frame.Macd.ewm(span=9, adjust=False).mean()

        shortEMA_validate = self.data_frame_validate.Close.ewm(span=12, adjust=False).mean()
        longEMA_validate = self.data_frame_validate.Close.ewm(span=26, adjust=False).mean()

        self.data_frame_validate['Macd'] = shortEMA_validate - longEMA_validate
        self.data_frame_validate['Signal'] = self.data_frame_validate.Macd.ewm(span=9, adjust=False).mean()

        # Since we are playing with days, we need to remove data that can't be counted, those with NA
        self.data_frame.dropna(inplace=True)

    # @Return a float with the correct quantity amount to place when creating order

    def get_possible_quantity(self):

        # Getting the current balance with quote currency
        balance = self.client.get_asset_balance(asset=self.quote)

        # Retrieving the total quote amount with usdt_wallet variable
        quantity = (float(balance['free']) + self.ret_usdt_wallet()) * (self.quantity / 100)
        
        # Storing the exact quote amount format when placing order
        quantity = self.get_floor_quantity(quantity, self.quote_floor_precision)
        
        # Keeping tradk of the correct MAX quote amount between symbols
        usdt_wallet[self.symbol] = str(quantity)
        self.open_position_price = quantity

        # Converting quote amount to coint amount
        quantity = quantity / self.data_frame.Close.iloc[:-1][-1] * 100 / 100
        
        # Return the exact coin amount with the right format for Binance
        return self.get_floor_quantity(quantity, self.coin_floor_precision)


    # Side will define if we are BUYING or SELLING, the order type will always be MARKET type for now
    # @Return Boolean wether or not things went well

    def place_order(self, side, order_type=Client.ORDER_TYPE_MARKET):

        # Locking the mutex to make sure that no thread will interfer
        self.mutex.acquire()
        if side == 'SELL':
            quantity = self.open_position_quantity
            self.open_position_quantity = 0
            self.open_position_price = 0
            usdt_wallet[self.symbol] = '0'
        else:
            quantity = self.get_possible_quantity()
            self.open_position_quantity = quantity
        try:
            # Placing an order with Binance API return a json object
            order = self.client.create_order(symbol=self.symbol, side=side, type=order_type, quantity=quantity)    
        except BinanceAPIException as e:
            self.mutex.release()
            print(e)
            print("Error: couldn't place order for symbol " + self.symbol + " side " + side + " for " + str(quantity))
            return False

        # Release the mutex to free all thread that was blocked
        self.mutex.release()

        # Storing order in sql format to manipulate it after
        insert_order.insert_sql_data(order)

    def check_price(self, side):
        if side == Client.SIDE_BUY: 
            if self.data_frame_validate.Macd.iloc[-1] > self.data_frame_validate.Signal.iloc[-1] and self.data_frame_validate.Macd.iloc[-2] > self.data_frame_validate.Signal.iloc[-2]:
               return True
        elif side == Client.SIDE_SELL:
            if self.data_frame_validate.Macd.iloc[-1] < self.data_frame_validate.Signal.iloc[-1] and self.data_frame_validate.Macd.iloc[-2] < self.data_frame_validate.Signal.iloc[-2]:
                return True
        return False

    def buy_sell(self):
        self.data_frame['Buy'] = 0
        self.data_frame['Sell'] = 0
        flag = -1
        
        for i in range(26, len(self.data_frame)):
            if self.data_frame.Macd[i] > self.data_frame.Signal[i]:
                if flag != 1:
                    self.data_frame.Buy.iloc._setitem_with_indexer(i, 1)
                    flag = 1
            if self.data_frame.Macd[i] < self.data_frame.Signal[i]:
                if flag != 0:
                    self.data_frame.Sell.iloc._setitem_with_indexer(i, 1)
                    flag = 0

    # @Return Boolean, False will stop the thread because something went wrong

    def strategy(self):

        # Updating the current data_frame with financial indicators

        self.update_data_frame()
        # Applying Buy and Sell columns to decide wether or not we should place an order

        self.buy_sell()
        # Printing last row of the data frame

        print("\t\t" + self.symbol)
        print("Close -> " + str(self.data_frame.Close.iloc[-1]))
        print("Open Position -> " + str(self.open_position))
        print("Macd " + self.interval + " -> " + str(round(self.data_frame.Macd.iloc[-1], 3)) + " Signal " + self.interval + " -> " + str(round(self.data_frame.Signal.iloc[-1], 3)))
        print("Macd " + self.interval_validate + " -> " + str(round(self.data_frame_validate.Macd.iloc[-1], 3)) + " Signal " + self.interval_validate + " -> " + str(round(self.data_frame_validate.Signal.iloc[-1], 3)))

        # Making sure if we are not in open_position and we want to place an order with .Buy or .Sell
        if self.open_position == False and (self.data_frame.Buy.iloc[-1] or self.data_frame.Buy.iloc[-2]) and self.check_price(Client.SIDE_BUY):
            self.open_position = True
            return self.place_order(Client.SIDE_BUY)
        elif self.open_position == True and (self.data_frame.Sell.iloc[-1] or self.data_frame.Sell.iloc[-2]) and self.check_price(Client.SIDE_SELL):
            self.open_position = False
            return self.place_order(Client.SIDE_SELL)
        return True
    
    # Main loop of the thread Symbol, sleep each time we try to trade

    def main_loop(self):
        while True:
            if self.strategy() == False:
                return
            sleep(10)
