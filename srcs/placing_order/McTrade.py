import os
import sys
from time import sleep
import threading
from .Symbol import Symbol
from binance.client import Client
from binance.exceptions import BinanceAPIException


# Global Dictionnary used by all symbol to be able to retrieve the exact amount aviable on the account

usdt_wallet = {}

# Global Mutex to make sure that threads won't modify usdt_wallet at the same time during an order

mutex = threading.Lock()


class McTrade:

    # We just need the config object as arguements because it hold everything we need to know about symbols
    # and how we will trade them


    def __init__(self, config):

        self.config = config

        # Storing each symbols to keep track of every single thread
        
        self.threads = []

        # Retrieving the Binance Client API with api_key environnement variable
        
        self.client = self.connect_binance_client(os.environ.get('api_key'), os.environ.get('secret_api_key'))
        

    def connect_binance_client(self, api_key, secret_api_key):

        # @Return Bincance Client object

        try:

            return Client(api_key, secret_api_key)
        
        except BinanceAPIException as e:
        
            print(e)
            print("Error: cannot create a connection to Binance with those api_key")
            sys.exit(1)


    # The function address that we will be used for each thread when
    # they will be setup, this is their entry point

    def main_loop_thread(self, symbol, client):

        # Making sure that mutex is available in all threads

        global mutex

        # Instantiate Symbol object to init attributes

        symbol = Symbol(symbol, client, mutex)

        symbol.main_loop()

    # Revieve a single thread based on the index

    def revieve_thread(self, index):
    
        try:

            # Rebuilding the thread

            self.threads[index] = threading.Thread(target=self.main_loop_thread, args=(self.config[index], self.client, ), daemon=True)
        
            # Restarsting the thread

            self.threads[index].start()

        except ValueError as e:
            print(e)
            print("Error: Unable to start the thread in starting_symbol_order function")
            sys.exit(1)

    # Confiurating each thread

    def starting_symbol_order(self):

        try:

            # Creating a thread for each symbol in self.config object

            for symbol_config in self.config:
                self.threads.append(threading.Thread(target=self.main_loop_thread, args=(symbol_config, self.client, ), daemon=True))
        
            # Starting each thread created previously

            for index in range(len(self.threads)):
                self.threads[index].start()

        except ValueError as e:
            print(e)
            print("Error: Unable to start the thread in starting_symbol_order function")
            sys.exit(1)


    # Keep alive of McTrade to keep trade of each thread

    def main_loop(self):
        try:

            while True:

                # Iterate on each threads

                for index in range(len(self.threads)):

                    # Making sure they are still alive

                    if self.threads[index].is_alive() == False:
                    
                        print("Restarting the thread in 5 seconds")

                        sleep(5)

                        # Revieve the thead that just die

                        self.revieve_thread(index)
                    
                
        except KeyboardInterrupt:

            # Catching ctrl + c to exit all threads at the same time

            print("Successfully exited from all threads, (need to implements conclusion) ")
            sys.exit(1)     
