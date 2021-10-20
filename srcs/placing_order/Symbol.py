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

usdt_wallet = {}

# An Symbol is created for each symbol configurated in the config file

class Symbol:

    # Symbol is define with certain attribute such as :
    # symbol    -> "BTCUSCT", "ETHUSDT", "COMPUSDT", etc...
    # coin      -> "BTC", "ETH", "COMP", "DOGE", etc...
    # quote     -> "USDT" and only "USDT" for now
    # risk      -> 3 >= risk <= 25 (the higher this value is the more risky the bot will be)
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

        self.risk = config['risk']
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
       
        # Storing the first fetch as DataFrame, not affected by financial indicators

        self.data_frame = fetch_symb.get_data_frame(self.client, self.symbol, self.interval, self.lookback)

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

        # Precision can't go higher than 6

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
        self.data_frame = fetch_symb.get_data_frame(self.client, self.symbol, self.interval, self.lookback)
        self.caculate_stoch_rsi_macd()

    # Applying STOCH + RSI + MACD algorithm 

    def caculate_stoch_rsi_macd(self):

        # A stochastic oscillator is a momentum indicator comparing a particular closing price of a security
        # to a range of its prices over a certain period of time. The sensitivity of the oscillator to market
        # movements is reducible by adjusting that time period or by taking a moving average of the result.
        # It is used to generate overbought and oversold trading signals, utilizing a 0–100 bounded range of values. 

        # Formula :
        # 
        #           K = ((H14 - L14) / (C - L14)​) * 100
        # 
        # C = The most recent closing price
        # L14 = The lowest price traded of the 14 previoustrading sessions
        # H14 = The highest price traded during the same 14-day period
        # K = The current value of the stochastic indicator​

        self.data_frame['K'] = ta.momentum.stoch(self.data_frame.High, self.data_frame.Low, self.data_frame.Close, window=14, smooth_window=3)

        # Notably, K is referred to sometimes as the fast stochastic indicator.
        # The "slow" stochastic indicator is taken as
        # D = 3-period moving average of K
        
        self.data_frame['D'] = self.data_frame['K'].rolling(3).mean()

        # The relative strength index (RSI) is a momentum indicator used in technical analysis
        # that measures the magnitude of recent price changes to evaluate overbought or oversold
        # conditions in the price of a stock or other asset. The RSI is displayed as an oscillator
        # (a line graph that moves between two extremes) and can have a reading from 0 to 100.

        # Formula :
        #
        #          RSI = 100 - (100 / (1 + (Average loss / Average gain)​)
        #
        # The average gain or loss used in the calculation is the average percentage
        # gain or loss during a look-back period. The formula uses a positive value
        # for the average loss. Periods with price losses are counted as 0 in the
        # calculations of average gain, and periods when the price increases are
        # counted as 0 for the calculation of average losses.

        self.data_frame['RSI'] = ta.momentum.rsi(self.data_frame.Close, window=14)

        # Moving average convergence divergence (MACD) is a trend-following momentum
        # indicator that shows the relationship between two moving averages of a security’s price.
        # The MACD is calculated by subtracting the 26-period exponential 
        # moving average (EMA) from the 12-period EMA.

        # Formula :
        #
        #          MACD= N-Period EMA − N2-Period EMA
        #
        # Where N = 12 and N2 = 26 for example
        # MACD is calculated by subtracting the long-term EMA (26 periods) from the short-term EMA (12 periods).
        # An exponential moving average (EMA) is a type of moving average (MA)
        # that places a greater weight and significance on the most recent data point


        self.data_frame['MACD'] = ta.trend.macd_diff(self.data_frame.Close)

        # Since we are playing with days, we need to remove data that can't be counted, those with NA

        self.data_frame.dropna(inplace=True)

    # Storing one of the four signal to know if we are in good posture to buy/sell
    # K < 20 and D < 20 means that the market is oversold (time to buy)
    # K > 80 and D > 80 means that the market is overbought (time to sell)
    # @Return data_frame with all the buy and sell trigger

    def get_trigger(self, buy=True):
        
        # Easier to store it in DataFrame

        data_frame_trigger = pd.DataFrame()

        # Risk means how far we are going to step back the DataFrame,
        # the less we do the more secure the call is

        for i in range (self.risk + 1):

            # Market Oversold

            if buy:

                mask = (self.data_frame['K'].shift(i) < 20) & (self.data_frame['D'].shift(i) < 20)
            
            # Market Overbought
             
            else:

                mask = (self.data_frame['K'].shift(i) > 80) & (self.data_frame['D'].shift(i) > 80)
            
            # Storing each mask

            data_frame_trigger = data_frame_trigger.append(mask, ignore_index=True)

        return data_frame_trigger.sum(axis=0)

    # Retrieving buy and sell trigger putting 1 if it's a good time to buy, 0 if it's not

    def buy_sell_trigger(self):

        self.data_frame['Buy_trigger'] = np.where(self.get_trigger(), 1, 0)
        self.data_frame['Sell_trigger'] = np.where(self.get_trigger(buy=False), 1, 0)

   
    # The decision making of McTrade, wether or not he will place an order
   
    def decide(self):

        # Retrieving buy and sell trigger

        self.buy_sell_trigger()

        # If the market is Oversold, K is between 20 and 80, D is between 20 and 80, RSI > 50
        # and MAC > 0 we buy

        self.data_frame['Buy'] =    np.where((self.data_frame.Buy_trigger) &
                                    (self.data_frame['K'].between(20, 80)) & 
                                    (self.data_frame['D'].between(20, 80)) & 
                                    (self.data_frame.RSI > 50) & 
                                    (self.data_frame.MACD > 0), 1, 0)

        # If the market is Overbought, K is between 20 and 80, D is between 20 and 80, RSI < 50
        # and MAC < 0 we sell

        self.data_frame['Sell'] =   np.where((self.data_frame.Sell_trigger) &
                                    (self.data_frame['K'].between(20, 80)) & 
                                    (self.data_frame['D'].between(20, 80)) & 
                                    (self.data_frame.RSI < 50) & 
                                    (self.data_frame.MACD < 0), 1, 0)


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
        try :

            # Placing an order with Binance API return a json object
        
            order = self.client.create_order(symbol=self.symbol, side=side, type=order_type, quantity=quantity)
        
        except BinanceAPIException as e:
            self.mutex.release()
            print(e)
            print("Error: couldn't place order for symbol " + self.symbol + " side " + side + " for " + quantity)
            return False

        # Release the mutex to free all thread that was blocked

        self.mutex.release()

        # Storing order in sql format to manipulate it after

        insert_order.insert_sql_data(order)


    # @Return Boolean, False will stop the thread because something went wrong

    def strategy(self):

        # Updating the current data_frame with financial indicators

        self.update_data_frame()

        # Applying Buy and Sell columns to decide wether or not we should place an order

        self.decide()

        # Printing last row of the data frame

        print(self.data_frame.iloc[-1])

        # Making sure if we are not in open_position and we want to place an order with .Buy or .Sell

        if self.open_position == False and self.data_frame.Buy.iloc[-1]:

            self.open_position = True
            return self.place_order(Client.SIDE_BUY)
        elif self.open_position == True and self.data_frame.Sell.iloc[-1]:

            self.open_position = False
            return self.place_order(Client.SIDE_SELL)

        return True
    
    # Main loop of the thread Symbol, sleep each time we try to trade

    def main_loop(self):
        while True:
            if self.strategy() == False:
                return
            sleep(2)
