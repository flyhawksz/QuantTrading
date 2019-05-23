# -*- coding: utf-8 -*-
# @Time    : 2019-5-20 11:55
# @Author  : flyhawk
# @Email   : flyhawksz@163.com
# @File    : ccxt_test.py
# @Software: PyCharm

import ccxt
import pprint
import pandas as pd
from datetime import datetime
import numpy as np


# good_markets = ['_1btcxe', 'bequant', 'binanceje', 'bit2c', 'bitbank', 'bitbay', 'bitflyer', 'bitibu', 'bitkk',
# 'bitmarket', 'bitso', 'bitstamp', 'bitstamp1', 'bittrex', 'bl3p', 'bleutrade', 'btcbox', 'btcchina', 'btcexchange',
# 'btctradeua', 'chbtc', 'chilebit', 'coinbase', 'coinbaseprime', 'coincheck', 'coinex', 'coinfalcon', 'coinfloor',
# 'coinmarketcap', 'coinmate', 'coinnest', 'coinone', 'coinspot', 'crypton', 'dsx', 'fcoinjp', 'foxbit', 'fybse',
# 'fybsg', 'gdax', 'gemini', 'getbtc', 'hadax', 'huobipro', 'huobiru', 'ice3x', 'independentreserve', 'indodax',
# 'itbit', 'jubi', 'kraken', 'kuna', 'lakebtc', 'liquid', 'mercado', 'mixcoins', 'negociecoins', 'nova', 'okcoincny',
# 'paymium', 'poloniex', 'quadrigacx', 'southxchange', 'surbitcoin', 'therock', 'upbit', 'urdubit', 'vbtc', 'virwox',
# 'zaif', 'zb']

good_exchanges = ['bitbay', 'bitflyer', 'bitstamp']


def create_exchange(exchange_name):
    exchange = getattr(ccxt, exchange_name)()
    # exchange.proxies = {
    #     'http': 'socks5://127.0.0.1:1080',
    #     'https': 'socks5h://127.0.0.1:1080'
    # }
    # if isMac():
    #     exchange.proxies = {
    #         'http': 'http://127.0.0.1:1080',
    #         'https': 'https://127.0.0.1:1080'
    #     }

    print(exchange.id, exchange.name, exchange)
    # print(exchange.load_markets())
    
    markets = exchange.load_markets()
    
    etheur1 = exchange.markets['ETH/EUR']  # get market structure by symbol
    print(etheur1)
    print('etheur1 = %s' % etheur1)
    etheur2 = exchange.market('ETH/EUR')  # same result in a slightly different way
    print(etheur2)
    print('etheur2 = %s' % etheur2)
    etheurId = exchange.market_id('BTC/USD')  # get market id by symbol
    print(etheurId)
    print('etheurId = %s' % etheurId)
    symbols = exchange.symbols  # get a list of symbols
    print('symbols = %s' % symbols)
    symbols2 = list(exchange.markets.keys())  # same as previous line
    print('symbols2 = %s' % symbols2)
    print(exchange.id, symbols)  # print all symbols

    currencies = exchange.currencies  # a list of currencies
    print('currencies = %s' % currencies)


    # kraken = ccxt.kraken()
    # kraken.load_markets()

    # kraken.markets['BTC/USD']  # symbol → market (get market by symbol)
    # kraken.markets_by_id['XXRPZUSD']  # id → market (get market by id)
    #
    # kraken.markets['BTC/USD']['id']  # symbol → id (get id by symbol)
    # kraken.markets_by_id['XXRPZUSD']['symbol']  # id → symbol (get symbol by id)
    return exchange


def get_symbol(exchange_name):
    exchange = create_exchange(exchange_name)
    return exchange.symbols


if __name__ == '__main__':
    # good_exchanges = []
    # for i in ccxt.exchanges:
    
    for i in good_exchanges:
        try:
            # print(create_exchange(i))
            create_exchange(i)
            # print(get_symbol(i))
            # exchange = getattr(ccxt, i)()
            # task = simple_test(exchange)
            # # task = getData(exchanges[i], symbols[i])
            # tasks.append(asyncio.ensure_future(task))
            # good_exchanges.append(i)
        except Exception:
            print('exchange error! name is %s' % i)
        
    # print(good_exchanges)
        