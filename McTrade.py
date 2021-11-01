#!/usr/bin/python3

import os
import sys
from srcs.placing_order.McTrade import McTrade
from dotenv import load_dotenv
from srcs.entry_parsing import configuration_file_parsing as cfp
from binance.client import Client

# Loading environnement variable
# Parsing the configuration file
# Launching McTrade to trade each symbol

if __name__ == "__main__":

    # Loading .env file with all environnement variable

    load_dotenv()
    if os.environ.get('api_key') == None or os.environ.get('secret_api_key') == None:
        print ("Error: no api_key found, pls create .env file at the root of the main direction, with api_key and secret_api_key variable")
        sys.exit(1)

    # Parsing the argument to retrive the configuration file 

    config = cfp.parse_entry(sys.argv[1:])
    
    # Creating McTrade passing the config object as argument

    mctrade = McTrade(config)

    # Starting each thread to trade symbol requested in the config file

    mctrade.starting_symbol_order()
    
    # Main loop checking if all thread are alive
    
    mctrade.main_loop()