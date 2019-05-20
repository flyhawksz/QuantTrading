#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : GetMarketsInfo.py
@Author: flyhawk
@Date  : 2019/5/19 0:35
@Desc  : 
'''

# 引入库
import ccxt
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor

now = lambda: time.time()
start = now()


async def getData(exchange, symbol):
    data = {}  # 用于存储ticker和depth信息
    # 获取ticker信息
    tickerInfo = await exchange.fetch_ticker(symbol)
    # # 获取depth信息
    # depth = {}
    # # 获取深度信息
    # exchange_depth = await exchange.fetch_order_book(symbol)
    # # 获取asks,bids 最低5个，最高5个信息
    # asks = exchange_depth.get('asks')[:5]
    # bids = exchange_depth.get('bids')[:5]
    # depth['asks'] = asks
    # depth['bids'] = bids
    
    data['ticker'] = tickerInfo
    # data['depth'] = depth
    
    return data


def main():
    # 实例化市场
    exchanges = [ccxt.bitstamp(), ccxt.bitflyer()]
    # 交易对
    symbols = ['BTC/USD']
    
    tasks = []
    i = 0
    j = 0
    for i in range(len(exchanges)):
        for j in range(len(symbols)):
            # tasks.append(self.proxy_resource_Url + str(i))
            task = getData(exchanges[i], symbols[j])
            tasks.append(asyncio.ensure_future(task))
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))


if __name__ == '__main__':
    main()
    print('Run Time: %s' % (now() - start))