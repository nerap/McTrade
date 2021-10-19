#!/usr/bin/python3

import os
import sys
from srcs.placing_order.McTrade import McTrade
from dotenv import load_dotenv
from srcs.entry_parsing import configuration_file_parsing as cfp
from binance.client import Client


if __name__ == "__main__":
    load_dotenv()
    if os.environ.get('api_key') == None or os.environ.get('secret_api_key') == None:
        print ("Error: no api_key found, pls create .env file at the root of the main direction, with api_key and secret_api_key variable")
        sys.exit(1)
    symbols = cfp.parse_entry(sys.argv[1:])

    mctrade = McTrade(symbols)
    mctrade.starting_symbol_order()
    mctrade.main_loop()
    print(mctrade)
    #s = symb.Symbol(symbols[0], client)
    #print(s.coin_floor_quantity)
    #print(s.quote_floor_quantity)
    #mac.starting_loop_order(symbols)