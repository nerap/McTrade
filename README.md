<div id="top"></div>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![GNU License][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">McTrade</h3>

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



<!-- TABLE OF CONTENTS -->
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
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
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

<!-- GETTING STARTED -->
## Getting Started

Do not panic everything will be alright, really simple!

### Prerequisites

You need of course python 3.6+ to launch everything, and pip3 to install package
* apt-get
  ```sh
  $ sudo apt-get update
  $ sudo apt-get install python3.6
  $ sudo apt install python3-pip
  ```

### Installation

1. First get your account at [Binance](https://www.binance.com/fr)
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



<!-- USAGE EXAMPLES -->
## Usage

McTrade works like any other script.
The main argument that McTrade need is a configuration file

 ```sh
   python3 McTrady.py -f path/to/config/file
   ```

Default config files are in config_file/ directory

 ```sh
   python3 McTrady.py -f config_files/basic_config
   ```

The "tricky" part comes now, the configuration file. No extension needed but a really strict format is expected but unusual.
The format is a json object, it's a json file.
 
 ```json
    {
        "symbols": [
            {
                "symbol": "ETHUSDT"
            },
            {
                "symbol": "BTCUSDT",
                "quantity": 20,
                "risk": 7
            },
            {
                "symbol": "XRPUSDT",
                "quantity": 50
            }
        ]
    }
```

You have to respect that symbols is the key to yours symbols array, so whatever you are trying to do keep "symbols" as the main key to your array.

Like this 

    
```json
    {
        "symbols": [
            {
                "symbol": "ETHUSDT"
            }
        ]
    }
```

or like this

```json
    {
        "symbols": [
            {
                "symbol": "ETHUSDT"
            },
            {
                "symbol": "BTCUSDT"
            },
            {
                "symbol": "DOGEUSDT"
            },
            {
                "symbol": "COMPUSDT"
            }
        ]
    }
```
Each element of symbols array in the configuration file, can take 3 parameters (5 in reality but I don't recommend to touch them unless you really know what you are doing).

```json
    {
        "symbols": [
            {
                "symbol": "ETHUSDT",
                "quantity": 20,
                "risk": 4
            }
        ]
    }
```
<!-- MANDATORY -->

## Mandatory parameters

### **-The "symbol"**

*The only this to worry about is each element in your "symbols" array.
You have to got at least 1 symbol (pair of coin and quote -> BTC + USDT , ETH + USDT, etc..)
You can only trade crypto that end with USDT, because USDT is the only currency that McTrade can mange for now.*

*So if you want to trade, you need to make sure to have your wallet converted to USDT, because this is how McTrade will place his order.
Each transaction is a minimum of 10 USDT (10 dollars), so you need at least 20 USDT to trade without being worried about the minimum about.*

<!-- OPTIONNAL -->

## Optionnal parameters:

### **-The "quantity"**

How many MAX % of your USDT wallet this McTrade will trade with, if you specify 20, 20 percent of your MAX % so if you 100 USDT, 20 will be dedicated to trade, (not more not less).
McTrade won't run if the sum of your quantity is above 100 %

### "quantity" must be between 10 and 100.

*(If not quantity is present, the default value will be ( 100 / numbers of symbols)) so for instance if you want to trade 4 crypto simultaneously and none of them has precise their quantity each of them will use 25 % of your maximum wallet)*

### **-The "risk"**

Represent how greedy your bot will be, I don't recommend using this parameters neither, because the greater he is the more unpredictable the McTrade will be if you really want to use it, I suggest to put him between 3 and 7 MAXIMUM.

### "risk" must be between 3 and 25

*(Default value is 5)*

## WARNING THOSE 2 PARAMETERS ARE NOT RECOMMEND TO MODIFY

Nevertheless you still can, see this doc https://python-binance.readthedocs.io/en/latest/constants.html

### **-The "interval"**

McTrade is fetching data from Binance API and the data have an interval for example, 1 minutes between each price of the BTC, or 30 minutes even 1 day between each data.
That doesn't mean that when you fetch a data with 1 day interval that you won't have the actual current price of the BTC, you will have the each price from now with an "interval" with a certain "lookback".

*(Default value is "30m")*

### **-The "lookback"**

Like interval, lookback has special format that you will need to stick to.
Reprensent how far you will look for you data, example 100 minutes, 1 week, 1 year. McTrade will use data 1 year old with a certain "interval" between each of them.

*(Default value is "14 day ago UTC")*


<!-- ROADMAP -->
## Roadmap

- [] Add another currency than USDT
- [] Add Docker file
- [] Make a prettier ReadMe

See the [open issues](https://github.com/othneildrew/Best-README-Template/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request




<!-- LICENSE -->
## License

Distributed under the GNU License. See `LICENSE.txt` for more information.


<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

Use this space to list resources you find helpful and would like to give credit to. I've included a few of my favorites to kick things off!

* [Binance Python-API](https://binance-docs.github.io/apidocs/spot/en/)
* [Stochastic](https://www.investopedia.com/terms/s/stochasticoscillator.asp)
* [MACD](https://www.investopedia.com/terms/m/macd.asp)
* [AlgoVibes](https://www.youtube.com/c/Algovibes)
* [%K & %D](https://www.investopedia.com/articles/technical/073001.asp)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/nerap/McTrade/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/nerap/McTrade/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/nerap/McTrade/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/nerap/McTrade/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/nerap/McTrade/LICENSE.txt
[product-screenshot]: images/screenshot.png
