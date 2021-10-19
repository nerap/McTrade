import os
import sys
import threading
from .Symbol import Symbol
from binance.client import Client
from binance.exceptions import BinanceAPIException

usdt_wallet = {}
mutex = threading.Lock()

class McTrade:
    def __init__(self, config):
        self.config = config

        self.threads = []
        
        self.client = self.connect_binance_client(os.environ.get('api_key'), os.environ.get('secret_api_key'))
        

    def connect_binance_client(self, api_key, secret_api_key):
        try:
            return Client(api_key, secret_api_key)
        except BinanceAPIException as e:
            print(e)
            print("Error: cannot create a connection to Binance with those api_key")
            sys.exit(1)

    def main_loop_thread(self, symbol, client):
        global usdt_wallet

        mutex.acquire()

        symbol = Symbol(symbol, client)
        usdt_wallet[symbol.symbol] = str(symbol.open_position_price)
        mutex.release()

        symbol.main_loop() 

    # Connecting to the client then starting each thread/symbol

    def starting_symbol_order(self):
        global mutex

        try:

            for symbol_config in self.config:
                self.threads.append(threading.Thread(target=self.main_loop_thread, args=(symbol_config, self.client, ), daemon=True))
        
            for index in range(len(self.threads)):
                self.threads[index].start()

        except ValueError as e:
            print(e)
            print("Error: Unable to start the thread in starting_symbol_order function")
            sys.exit(1)


    def main_loop(self):
        try:
            while True:
                for index in range(len(self.threads)):
                    if self.threads[index].is_alive() == False:
                        print("Thread Died")
                        sys.exit(1)
        except KeyboardInterrupt:
            print("Successfully exited from all threads, (need to implements conclusion) ")
            sys.exit(1)     
