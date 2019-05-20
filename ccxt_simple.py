#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : ccxt_simple.py
@Author: flyhawk
@Date  : 2019/5/18 15:53
@Desc  : 
'''

# 引入pandas框架
import pandas as pd
import time
import pprint

#  引入ccxt框架， 通过pip install ccxt 可以进行安装
# ccxt 的github地址为： https://github.com/ccxt/ccxt
import ccxt


def bitstamp_test():
    
    #  初始化bitme交易所对象
    bitmex = ccxt.bitstamp()
    
    # 请求的candles个数
    limit = 500
    
    #  当前时间
    current_time = int(time.time() // 60 * 60 * 1000)  # 毫秒
    print(current_time)
    
    # 获取请求开始的时间
    since_time = current_time - limit * 60 * 1000
    
    #  'BTC/USD' 比特币对美元的交易对，或者ETH/USD 以太坊对美元的交易对.
    data = bitmex.fetch_ohlcv(symbol='BTC/USD', limit=500, since=since_time)
    df = pd.DataFrame(data)
    df = df.rename(columns={0: 'open_time', 1: 'open', 2: 'high', 3: 'low', 4: 'close', 5: 'volume'})
    
    # 时间转换成北京时间
    df['open_time'] = pd.to_datetime(df['open_time'], unit='ms') + pd.Timedelta(hours=8)
    
    # 设置index
    df = df.set_index('open_time', drop=True)
    
    # 保存成csv文件
    df.to_csv('bitmex_data.csv')  # comma seperate Value
    print(df)


def simple_test(exchange):
    # 实例化市场
    # exchange = ccxt.bitstamp()
    # 交易对
    symbol = 'BTC/USD'
    
    # 获取ticker信息
    ticker = exchange.fetch_ticker(symbol)
    # 获取depth信息
    depth = exchange.fetch_order_book(symbol)
    
    print('ticker:%s, depth:%s' % (ticker, depth))
    
    
if __name__ == '__main__':
    simple_test()
    # bitstamp_test()
    