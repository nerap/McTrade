#!/usr/bin/python3

import os
import time
import json
import math
import sqlalchemy
import sys, getopt
import requests as rq
from nginxparser_eb import load
from pyparsing import ParseException
from dotenv import load_dotenv

symbols = []

default_values = ['MIN_QUANTITY', 'MAX_QUANTITY', 'DEFAULT_INTERVAL', 'DEFAULT_LOOKBACK', 'DEFAULT_INTERVAL_VALIDATE', 'DEFAULT_LOOKBACK_VALIDATE']
default_attributes = ['SYMBOL', 'QUANTITY', 'INTERVAL', 'LOOKBACK', 'INTERVAL_VALIDATE', 'LOOKBACK_VALIDATE']

default_values_dic = {
    'MAX_QUANTITY' : '100',
    'MIN_QUANTITY' : '5',
    'DEFAULT_INTERVAL' : '1d',
    'DEFAULT_LOOKBACK' : '180 day ago UTC',
    'DEFAULT_INTERVAL_VALIDATE' : '6h',
    'DEFAULT_LOOKBACK_VALIDATE' : '5 day ago UTC'
}

MAX_QUANTITY = 100
MIN_QUANTITY = 5
DEFAULT_INTERVAL = "1d"
DEFAULT_LOOKBACK = "180 day ago UTC"
DEFAULT_INTERVAL_VALIDATE = "6h"
DEFAULT_LOOKBACK_VALIDATE = "7 day ago UTC"
bot = sys.argv[0]
url_binance_ticker_price = "https://api.binance.com/api/v3/ticker/price?symbol="

def default_symbol():
    return  {   'SYMBOL' : 'NOSYMBOL',
                'QUANTITY' : default_values_dic['MIN_QUANTITY'],
                'INTERVAL' : default_values_dic['DEFAULT_INTERVAL'],
                'LOOKBACK' : default_values_dic['DEFAULT_LOOKBACK'],
                'INTERVAL_VALIDATE' : default_values_dic['DEFAULT_INTERVAL_VALIDATE'],
                'LOOKBACK_VALIDATE' : default_values_dic['DEFAULT_LOOKBACK_VALIDATE'] }

# Making sure that the symbol in the configuration file is valid for Binance

def parse_quantity(symbols):
    quantity = 0
    try:
        for i in range(len(symbols)):
            if int(symbols[i]['QUANTITY']) < int(default_values_dic['MIN_QUANTITY']) or int(symbols[i]['QUANTITY']) > int(default_values_dic['MAX_QUANTITY']):
                print('Invalid quantity ' + symbols[i]['QUANTITY'] + ' for symbol ' + symbols[i]['SYMBOL'])
                print('Quantity should be between >= ' + default_values_dic['MIN_QUANTITY']  + ' and <= ' + default_values_dic['MAX_QUANTITY'] + '!')
                print('Quantity default value is the MIN_QUANTITY such as ' +  default_values_dic['MIN_QUANTITY'])
                sys.exit(1)
            else:
                quantity += math.floor(int(symbols[i]['QUANTITY']))
        if quantity > int(default_values_dic['MAX_QUANTITY']):
            print('Invalid quantity the total quantity of your symbols is above 100% which is impossible check your configuration file')
            print('Quantity default value is the MIN_QUANTITY such as ' +  default_values_dic['MIN_QUANTITY'])
            sys.exit(1)
    except ValueError as e:
        print(e)
        print("Error: Quantity has to be an int")
        sys.exit(1)
    return symbols

# Making sure that the symbol in the configuration file is valid for Binance

def parse_symbol(symbol):
    if symbol[-4:] != 'USDT':
        print('Error: ' + symbol + ' is not valid for BinanceBot check your configuration file')
        print('BinanceBot can only hold USDT currency as pair with another crypto like -> BTCUSDT, XRPUSDT, ETHUSDT, etc..')
        print('Note that you cannot trade USDT currency such as -> USDTBIDR, USDTRUB, USDTUAH, etc..')
        sys.exit(1)
    res = rq.get(url_binance_ticker_price + symbol).json()
    if 'msg' in res:
        print(symbol + ' is not valid for BinanceBot check your configuration file')
        print(res["msg"])
        print("Return Code : " + str(res["code"]))
        sys.exit(1)
    elif symbol == "":
        print(symbol + ' is not valid for BinanceBot check your configuration file')
        sys.exit(1)
    return symbol

# Parsing all symbols in the configuration file with JSON format

def parse_config_file(config_file):
    if config_file == '':
        print("Error: configuration file missing")
        sys.exit(1)
    try:
        conf_fd = open(config_file,)
    except IOError as io:
        print("Error: can't open " + config_file)
        sys.exit(1)
    try:
        conf_parsed = load(conf_fd)
        if len(conf_parsed) == 0:
            print("Error: your configuration file is empty")
            sys.exit(1)
    except ParseException as pe:
        print("Error: can't parse " + config_file)
        sys.exit(1)
    try:
        for conf in conf_parsed:
            key, val = [conf[i] for i in (0, 1)]
            if key in default_values:
                val = val.replace('"', '')
                default_values_dic[key] = val
                if (key == 'MIN_QUANTITY' or key == 'MAX_QUANTITY') and (int(val) < 0 or int(val) > 100):
                    raise ('Error: ' + key + ' has to be > 0 and < 100')
            elif isinstance(key, list) and key[0] == 'SYMBOL':
                symbol = default_symbol()
                if len(conf_parsed) == 0:
                    print("Error: your configuration file is empty")
                    sys.exit(1)
                for attr in val:
                    key_attr, val_attr = [attr[i] for i in (0, 1)]
                    val_attr = val_attr.replace('"', '')
                    if key_attr in default_attributes:
                        symbol[key_attr] = val_attr
                parse_symbol(symbol['SYMBOL'])
                symbols.append(symbol)
            else:
                print(str(key) + ' is not valid for BinanceBot check your configuration file')
                sys.exit(1)
    except ValueError as e:
        print(e)
        print("Error: can't parse the configuration file")
        sys.exit(1)
    parse_quantity(symbols)
    for i in range(len(symbols)):
        for j in range(len(symbols)):
            if i != j and symbols[i]['SYMBOL'] == symbols[j]['SYMBOL']:
                print('Error: duplicated symbol ' + symbols[i]['SYMBOL'] + ' in configuration file')
                sys.exit(1)
    return symbols

# Taking all arguments of the program to parse -h and -f options.
# Making sure that the use is sending valid input and valid symbol.

def parse_entry(argv):
    config_file = ""
    try:
        opts, args = getopt.getopt(argv, "hf:", ["help", "file="])
    except getopt.GetoptError:
        print ('python3 ' + bot + ' -f <file> or --file=<file>')
        print ('python3 ' + bot + ' -h or --help')
        sys.exit(1)
    if len(opts) <= 0:
        print ('python3 ' + bot + ' -f <file> or --file=<file>')
        print ('python3 ' + bot + ' -h or --help')
        sys.exit(1)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print ('python3 ' + bot + ' -f <file> or --file=<file>')
            sys.exit(0)
        elif opt in ('-f', '--file'):
            config_file = arg
    return parse_config_file(config_file)

if __name__ == "__main__":
    parse_entry(sys.argv[1:])
    #print(symbols)
