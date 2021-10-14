import pandas as pd
import requests as rq
from datetime import datetime
import ast
import asyncio
from binance.client import Client
from binance import AsyncClient
from binance.exceptions import BinanceAPIException
import time
from binance import BinanceSocketManager
import sqlalchemy

symbol = "LINKBTC"

api_key = "1Phr1soDo5RtsyLzcVLt7rHa1UsBEpcEhVCZ9ddllmCtUK9BR74r9PZPoFiEJdoy"
secret_key = "he2Rj1dhBjbYsSynsUvSySVE5UZg5NzP00ORJ0LxaCarlLt3oWethlDlC7slcbfj"



#client = Client(api_key, secret_key)


async def main():
    client = await AsyncClient.create()
    bsm = BinanceSocketManager(client, user_timeout=10)
    socket = bsm.trade_socket(symbol)
    while True:
        try:
            await socket.__aenter__()
            msg = await socket.recv()
            if msg['e'] == "error":
                continue
            frame = create_frame(msg)
            frame.to_sql(symbol, engine, if_exists='append', index=False)
            print(frame)
        except BinanceAPIException as e:
            print(e)
            await disconnect_callback(client=client)
            await socket.__aexit__(None, None, None)
            break


async def disconnect_callback(client):
    await client.close_connection()  # close connection
    time.sleep(10)  # wait a minute before restarting
    await main()  # restart client and kline socket


def create_frame(msg):
    df = pd.DataFrame([msg])
    df = df.loc[:, ['s', 'E', 'p']]
    df.columns = ['symbol', 'Time', 'Price']
    df.Price = df.Price.astype(float)
    df.Time = pd.to_datetime(df.Time, unit='ms')
    return df


if __name__ == "__main__":
    engine = sqlalchemy.create_engine('sqlite:///' + symbol + 'stream.db')
    while True:
        res = rq.get("https://api.binance.com/api/v3/ticker/price?symbol=" + symbol).json()
        df = pd.DataFrame([{
                "symbol": res["symbol"],
                "datetime": int(time.time()),
                "price": float(res["price"])

        }])
        df.columns = ['Symbol', 'Time', 'Price']
        df.Price = df.Price.astype(float)
        df.Time = pd.to_datetime(int(time.time() * 1000), unit="ms")
        df.to_sql(symbol, engine, if_exists='append', index=False)
        print(df)
