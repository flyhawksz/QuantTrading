#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : ccxt_all_exchanges.py
@Author: flyhawk
@Date  : 2019/5/19 21:00
@Desc  : 
'''
import ccxt
import time
import asyncio

tasks = []

async def simple_test(exchange):
    # 实例化市场
    # exchange = ccxt.bitstamp()
    # 交易对
    symbol = 'BTC/USD'
    try:
        # 获取ticker信息
        ticker = exchange.fetch_ticker(symbol)
        # 获取depth信息
        # depth = exchange.fetch_order_book(symbol)
        
        # print('ticker:%s, depth:%s' % (ticker, depth))
        print('ticker:%s' % ticker)
        print(type(exchange))
        print(exchange.name)
    finally:
        # pass
        print(exchange.name & 'error!')
   
if __name__ == '__main__':
    # pair = 'ETH/BTC'
    # print(ccxt.exchanges)
    for i in ccxt.exchanges:
        exchange = getattr(ccxt, i)()
        task = simple_test(exchange)
        # task = getData(exchanges[i], symbols[i])
        tasks.append(asyncio.ensure_future(task))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))