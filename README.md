<div id="top"></div>

[![Size][size-shield]][repo-url]
[![Linex][line-shield]][repo-url]
[![Contributor][contributor-shield]][contributor-url]
[![Downloads][downloads-shield]][repo-url]
[![Issues][issues-shield]][issues-url]
[![License][lic-shield]][repo-url]
[![Stars][stars-shield]][repo-url]


<br />
<div align="center">
  <a href="https://github.com/nerap/McTrade">
    <img src="image/logo.png" alt="Logo" width="200" height="200">
  </a>
  <p align="center">
    Open Source Crypto Trading Bot using Binance API
    <br />
    <br />
    ·
    <a href="https://github.com/othneildrew/Best-README-Template/issues">Report Bug</a>
    ·
    <a href="https://github.com/othneildrew/Best-README-Template/issues">Request Feature</a>
  </p>
</div>

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#output">Output</a></li>
    <li><a href="#configuration">Configuration</a></li>
    <li><a href="#strategy">Strategy</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>


## About The Project

McTrade can run 24/7 on a server, laptop, anywhere.. his main purpose is to make smart trade.
This Bot is not built for making 20 order/sec, McTrade will only trade when many parameters are combined. In fact, he is using 3 main financial indicators used by almost everyone trader on the market.

Here's why:
* You will only need to give a configuration file to the bot, and that's it he won't need you anymore.
* McTrade is free, so there is no fee, EXCEPT from Binance (0.1 %).
* You can trade almost any crypto you want and at the same time !

Of course, we are in the real world, don't expect McTrade to make you billionaire in 2 weeks, the main idea of this bot is to give "passiv" revenue to anyone who wants to.
Trading is not like roulette or black jack, so McTrade won't bet your money randomly and pray to gain money. Every decision he will make is mathematically correct.

<p align="right">(<a href="#top">back to top</a>)</p>


## Built With

The techs are really simple that's why he is really portable and has not a high memory usage !

* [Python3](https://www.python.org/download/releases/3.0/)
* [SQLite](https://www.sqlite.org/index.html)
* [Docker](https://www.docker.com/) (Not implemted yet)

## Getting Started

Do not panic everything will be alright, really simple!

### Prerequisites

You need of course python 3.6+ to launch everything, and pip3 to install package
* apt-get
  ```sh
  $ sudo apt update
  $ sudo apt install python3.6
  $ sudo apt install python3-pip
  ```

### Installation

1. First get your account at [Binance](https://www.binance.com/en)
2. Put money on your wallet (50 USD or EUR ) is recommended but not mandatory you will see why. 
3. Clone the repo
   ```sh
   git clone https://github.com/nerap/McTrade.git
   ```
4. Installing dependencies
   ```sh
   make setup
   ```
5. Enter your API keys in `.env`
   ```sh
   api_key=SOME_API_KEY
   secret_api_key=SECRET_API_KEY
   ```
6. Here we go you successfully installed McTrade !


## Usage

McTrade works like any other script.
The main argument that McTrade need is a configuration file

 ```sh
   python3 McTrady.py -f path/to/config/file
   ```

Default config files are in config_file/ directory

 ```sh
   python3 McTrady.py -f config_files/basic_config.conf
   ```

### Output

If you set up your configuration file correctly you will this an output like this: 

 ```sh
                    XRPUSDT

    Close -> 1.1913
    Open Position -> False
    Macd 1d -> 0.036 Signal 1d -> 0.029
    Macd 6h -> 0.012 Signal 6h -> 0.018
 ```

**Every 10 seconds, you will see those informations on each crypto meaning that McTrade is working and currently looking to place an order.**

Those value will depends on the crypto you want to trade of course !
Open Position variable will tell you if your bot want to buy or want to sell, (False means he wants to buy, True means he wants to sell).

I didn't implement a trade history, but you have already have a beautiful one on Binance App.

**You really want to him to be working 24/7 so I recommend you to have a server, or letting your PC always on. If you want to use it on a server take a look a [this](https://askubuntu.com/questions/8653/how-to-keep-processes-running-after-ending-ssh-session).**

I will soon add a Docker File making things a bit easier.


### Configuration

The configuration is inspired by nginx configuration file format. The parser can be found [there](https://pypi.org/project/nginxparser_eb/)
This is really nginx but in caps lock, don't try to break the parser or add useless things, the configuration file is really straight foward.
 
 ```nginx
    MAX_QUANTITY 100;
    MIN_QUANTITY 5;
    DEFAULT_INTERVAL 1d;
    DEFAULT_LOOKBACK 180 day ago UTC;
    DEFAULT_INTERVAL_VALIDATE 6h;
    DEFAULT_LOOKBACK_VALIDATE 7 day ago UTC;
   
    SYMBOL {
       SYMBOL ETHUSDT;
       QUANTITY 33;
    }

    SYMBOL {
       SYMBOL XRPUSDT;
       QUANTITY 33;
    }
    
    SYMBOL {
       SYMBOL BTCUSDT;
       QUANTITY 34;
    }
```

Those first variable are basically constant and will be used when this file you will be parsed.
I don't recommend you to touch then useless you know what is happening in the code and how the value will affect the entire programm.

Now the part that you will modify as your will is SYMBOL field, there is only 2 paramters that I recommend you to modify :

SYMBOL :
  The symbol that will be trade, so a pair of two crypto 'BTCUSDT', 'ETHUSDT', etc.. 
  McTrade IS ONLY WORKING WITH USDT CRYPTO SO YOU CAN'T PUT ANY OTHER CRYPTO RATHER THAN USDT.

QUANTITY : 
  The amount is percentage of your maximum wallet you will give to this Symbol

An example :

```nginx
   SYMBOL {
       SYMBOL ETHUSDT;
       QUANTITY 25;
    }
```

McTrade will trade ETH with USDT currency, with 25 % of your maximum wallet.
You can remove QUANTITY field if you want, but the quantity will be replace by the MIN_QUANTITY defined earlier.
For instance, you can remove eveyrthing in SYMBOL {} field like this.

```nginx
   SYMBOL {
       SYMBOL BTCUSDT;
    }
```

So here the QUANTITY will be 5 because the field is empty.

This is the bare minimum to launch McTrade, the other fields will be replace by the default value, defined above.
You can add as much as Symbol you want, but you need to take in mind that each transaction has to be at least 10 USD equivalent, so if you have 100 USD, you can trade 10 symbols maximum (in therory)
I don't recommend, and even if you do it it won't work well, to trade with only 10 USD (equivalent), because, the moment you trade, you won't be able to sell back what you bought, for 3 reason:
### **First**
Each transaction comes  with a Binance Tax (0.1% the highest possible), so if you bought ETH for example, your will have 9.99 USD of ETH right after your Buying order, so you won't be able to sell 9.99 USD of ETH because the transaction has to be above 10 USD.
### **Second**
Crypto price is moving really fast, so if you buy, let's say for 10.02 USD of ETH, you will have enough to sell your ETH right after, unless, the price change and the ETH you bought doesn't worth 10 USD anymore, so you won't be able to sell it.
### **Third**
Some crypto doesn't let you buy the amount you want, like you can't buy 1.5 DOGE, you can only buy 1 or 2 DOGE, so, when you will buy 3 DOGE for example, you will have 2.997 right after your buying order, so if you want to sell your DOGE you will be able to only sell 2 DOGE not 2.997.
So for me the BARE BARE minimum will be 15 USD for me per symbol, and with symbol that let you buy with a certain precision.
And even trader with only 15 USD is really not worth it, keep it and buy yourself a Big Mac honestly.

## Mandatory parameters

### **-The "SYMBOL"**

*The only this to worry about is each element in your "symbols" array.
You have to got at least 1 symbol (pair of coin and quote -> BTC + USDT , ETH + USDT, etc..)
You can only trade crypto that end with USDT, because USDT is the only currency that McTrade can mange for now.*

*So if you want to trade, you need to make sure to have your wallet converted to USDT, because this is how McTrade will place his order.
Each transaction is a minimum of 10 USDT (10 dollars), so you need at least 20 USDT to trade without being worried about the minimum about.*

## Optionnal parameters:

### **-The "QUANTITY"**

How many MAX % of your USDT wallet this McTrade will trade with, if you specify 20, 20 percent of your MAX % so if you 100 USDT, 20 will be dedicated to trade, (not more not less).
McTrade won't run if the sum of your quantity is above 100 %
The MAX_QUANTITY defined is the configuration file is the maximum quantity of your wallet you let McTrade use for all Symbol combined.

### "QUANTITY" must be between 1 and 100.

*(If not quantity is present, the default value will be the MIN_QUANTITY defined in the configuration file)*

## WARNING THOSE 4 PARAMETERS ARE NOT RECOMMEND TO MODIFY, IF YOU DON'T UNDERSTAND WHAT MACD AND SIGNAL ARE, SKIP

Nevertheless you still can, see this doc https://python-binance.readthedocs.io/en/latest/constants.html
This is how much you can modify SYMBOL field. You can specify each symbol on wich period you want McTrade to trade with, lower value will mean faster trade.

```nginx
   SYMBOL {
       SYMBOL BTCUSDT;
       QUANTITY 20;
       INTERVAL 1d;
       LOOKBACK 60 day ago UTC;
       INTERVAL_VALIDATE 6h;
       LOOKBACK_VALIDATE 5 day ago UTC;
    }
```

### **-The "INTERVAL"**

McTrade is fetching data from Binance API and the data have an interval for example, 1 minutes between each price of the BTC, or 30 minutes even 1 day between each data.
That doesn't mean that when you fetch a data with 1 day interval that you won't have the actual current price of the BTC, you will have the each price from now with an "interval" with a certain "lookback".

*(Default value is "1d")*

### **-The "LOOKBACK"**

Like interval, lookback has special format that you will need to stick to.
Reprensent how far you will look for you data, example 100 minutes, 1 week, 1 year. McTrade will use data 1 year old with a certain "interval" between each of them.

*(Default value is "180 day ago UTC")*

### **-The "INTERVAL_VALIDATE"**

Same as INTERVAL but with a period inferior as INTERVAL, it will be a MACD and SIGNAL line like the previous one and will validate if you really want to buy now.
For example, McTrade is using MACD algorithm, but if you just buy or sell when the line cross you will sometimes have way more bad trade without the other MACD with a shorter perdiod.
If the MACD and SIGNAL with d1 period are crossing and MACD and SIGNAL with h6 period crossed N-2, you BUY/SELL
This will make sure that the line in d1 period crossed just for 1 hour then cross again and giving a useless buying and selling order, that will be a loss. 

*(Default value is "6h")*

### **-The "LOOKBACK_VALIDATE"**

Same as LOOKBACK but it will work with INTERVAL_VALIDATE

*(Default value is "5 day ago UTC")*

## Strategy

McTrade is really simple and using a simple trading algorithm.
MACD with a 12 and 26 period with a 1 day interval (can be modified)

        Moving average convergence divergence (MACD) is a trend-following momentum
        indicator that shows the relationship between two moving averages of a security’s price.
        The MACD is calculated by subtracting the 26-period exponential 
        moving average (EMA) from the 12-period EMA.

        Formula :
        
                  MACD = N-Period EMA − N2-Period EMA
        
        Where N = 12 and N2 = 26 for example
        MACD is calculated by subtracting the long-term EMA (26 periods) from the short-term EMA (12 periods).
        An exponential moving average (EMA) is a type of moving average(MA)
        that places a greater weight and significance on the most recent data point

You can't change the shortEMA and longEMA (unless you change the code directly) but you can change the period (INTERVAL variable), the default value is 1 day, but you can put 1 minute, 1 hour, 2 day, but don't do it unless you know what you are doing.
Default value are the best I found, so stick to it.

## Roadmap

- [] Add another currency than USDT
- [] Add Docker file
- [] Make a prettier ReadMe

See the [open issues](https://github.com/othneildrew/Best-README-Template/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the GNU License. See `LICENSE.txt` for more information.


## Acknowledgments

Use this space to list resources you find helpful and would like to give credit to. I've included a few of my favorites to kick things off!

* [Binance Python-API](https://binance-docs.github.io/apidocs/spot/en/)
* [Stochastic](https://www.investopedia.com/terms/s/stochasticoscillator.asp)
* [MACD](https://www.investopedia.com/terms/m/macd.asp)
* [AlgoVibes](https://www.youtube.com/c/Algovibes)
* [%K & %D](https://www.investopedia.com/articles/technical/073001.asp)

<p align="right">(<a href="#top">back to top</a>)</p>


[size-shield]: https://img.shields.io/github/languages/code-size/nerap/McTrade
[repo-url]: https://github.com/nerap/McTrade/
[line-shield]: https://img.shields.io/tokei/lines/github/nerap/McTrade
[contributor-shield]: https://img.shields.io/github/contributors/nerap/McTrade?color=Bri
[contributor-url]: https://github.com/nerap/McTrade/graphs/contributors
[downloads-shield]: https://img.shields.io/github/downloads/nerap/McTrade/total?color=bri
[issues-shield]: https://img.shields.io/github/issues/nerap/McTrade
[issues-url]: https://github.com/nerap/McTrade/issues
[lic-shield]: https://img.shields.io/github/license/nerap/McTrade?color=red
[stars-shield]: https://img.shields.io/github/stars/nerap/McTrade
