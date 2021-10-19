from binance.client import Client
import pandas as pd
import time
import numpy as np

# Need to explain this

class Signals:
        def __init__(self, data_frame, steps):
            self.data_frame = data_frame
            self.steps = steps
        
        def get_trigger(self, buy=True):
            data_frame_trigger = pd.DataFrame()
            for i in range (self.steps + 1):
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
