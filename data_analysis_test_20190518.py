#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : data_analysis_test_20190518.py
@Author: flyhawk
@Date  : 2019/5/18 17:44
@Desc  : 
'''

import requests
from lxml import etree
import logging  # log相关功能，不能总是用print那么low
import threading  # 导入线程包
import queue  # 多线程传递验证通过的IP, 保证线程安全
import os
import time
from Crawl import Crawler
import random
from concurrent.futures import ThreadPoolExecutor


class Model(object):
    # waittime = 5
    def __init__(self, bitcoinName):
        self.name = bitcoinName
        self.date = ''  #: 返回数据时服务器时间
        self.buy = ''  #: 买一价
        self.high = ''  #: 最高价
        self.last = ''  #: 本币最新成交价
        self.lastUSD = ''  #: 美元最新成交价
        self.low = ''  #: 最低价
        self.sell = ''  #: 卖一价
        self.vol = ''  #: 成交量(最近的24小时)

    def Mod2Dic(self):
        t = {self.name: {'date': self.date, 'buy': self.buy, 'sell': self.sell,
             'high': self.high, 'low': self.low, 'last': self.last, 'lastUSD': self.lastUSD, 'vol': self.vol}}
        return t

    def Mod2Str(self):
        t = '%s, %s, %s, %s, %s, %s, %s, %s' % (self.name, self.date, self.buy, self.sell, self.high, self.low, self.last, self.lastUSD)
        return t


class BitstampModel(Model):
    api_url = ''
    
    def __init__(self, bitcoinName):
        if bitcoinName == 'BTC':
            # self.api_url = 'https://www.bitstamp.net/api/ticker/'
            self.api_url = 'https://www.bitstamp.net/api/v2/ticker/btcusd'
        elif bitcoinName == 'LTC':
            self.api_url = 'https://www.bitstamp.net/api/v2/ticker/ltcusd'
        elif bitcoinName == 'ETH':
            self.api_url = 'https://www.bitstamp.net/api/v2/ticker/ethusd'
        else:
            pass
        
        super(BitstampModel, self).__init__('Bitstamp_' + bitcoinName)
    
    def GetTicker(self):
        # t_data = Ult.getURLData(self.api_url)
        t_data = self.get_response(self.api_url, self.http_headers)
        # print("Threading %d crawl %s" % thread_id, url)
        # charset的编码检测
        t_data.encoding = t_data.apparent_encoding
        self.date = t_data['timestamp']
        self.buy = t_data.get('bid')
        self.sell = t_data.get('ask')
        self.lastUSD = float(t_data.get('last'))
        # print('self.lastUSD : %s - %s' % (self.lastUSD, type(self.lastUSD)))
        self.last = float(t_data.get('last'))
        self.high = t_data.get('high')
        self.low = t_data.get('low')
        self.vol = t_data.get('volume')


#
#         # t_data = GetData(t_url)
#         # t_last = t_data['last']
#         # print("%s : %s" %(targeName,t_last))
#         time.sleep(waitTime)
'''
GET 	https://www.bitstamp.net/api/v2/ticker/{currency_pair}
  	Supported values for currency_pair: btcusd, btceur, eurusd, xrpusd, xrpeur, xrpbtc, ltcusd, ltceur, ltcbtc, ethusd, etheur, ethbtc

Response (JSON)
last 	Last BTC price.
high 	Last 24 hours price high.
low 	Last 24 hours price low.
vwap 	Last 24 hours volume weighted average price.
volume 	Last 24 hours volume.
bid 	Highest buy order.
ask 	Lowest sell order.
timestamp 	Unix timestamp date and time.
open 	First price of the day.

high	"4365.96"
last	"4305.53"
timestamp	"1503932683"
bid	"4305.54"
vwap	"4277.41"
volume	"6567.14892154"
low	"4169.01"
ask	"4312.94"
open	"4329.91"
'''


class BitfinexModel(Model):
    api_url = ''
    
    def __init__(self, bitcoinName):
        if bitcoinName == 'BTC':
            self.api_url = 'https://api.bitfinex.com/v1/pubticker/btcusd'
        elif bitcoinName == 'LTC':
            self.api_url = 'https://api.bitfinex.com/v1/pubticker/ltcusd'
        elif bitcoinName == 'ETH':
            self.api_url = 'https://api.bitfinex.com/v1/pubticker/ethusd'
        else:
            pass
        
        super(BitfinexModel, self).__init__('Bitfinex_' + bitcoinName)
    
    def GetTicker(self):
        t_data = self.get_response(self.api_url)
        t_data.encoding = t_data.apparent_encoding
        self.date = t_data['timestamp']  # .split('.')[0]
        self.buy = t_data.get('ask')
        self.sell = t_data.get('bid')
        self.lastUSD = float(t_data.get('last_price'))
        # print('self.lastUSD : %s - %s' % (self.lastUSD, type(self.lastUSD)))
        self.last = float(t_data.get('last_price'))
        self.high = t_data.get('high')
        self.low = t_data.get('low')
        self.vol = t_data.get('volume')
        
        # t_last = t_data['last_price']
        # print("%s : %s" % (self.name, self.last))
        # time.sleep(waitTime)


#     '''
#     https://api.bitfinex.com/v1/pubticker/btcusd
#     '''

class CoincheckModel(Model):
    api_url = ''
    
    def __init__(self, bitcoinName):
        if bitcoinName == 'BTC':
            self.api_url = 'https://coincheck.com/api/ticker'
        # elif bitcoinName == 'LTC':
        #     self.api_url = ''
        else:
            pass
        
        super(CoincheckModel, self).__init__('Coincheck_' + bitcoinName)
    
    def GetTicker(self):
        # t_data = Ult.getURLData(self.api_url)
        t_data = self.get_response(self.api_url)
        t_data.encoding = t_data.apparent_encoding
        self.date = t_data['timestamp']  # .split('.')[0]
        self.buy = t_data.get('ask')
        self.sell = t_data.get('bid')
        self.last = float(t_data.get('last'))
        self.lastUSD = self.last * jpy_usd
        # print('self.lastUSD : %s - %s' % (self.lastUSD, type(self.lastUSD)))
        self.high = t_data.get('high')
        self.low = t_data.get('low')
        self.vol = t_data.get('volume')
        
        # t_last = t_data['last_price']
        # print("%s : %s" % (self.name, self.last))
        # time.sleep(waitTime)


'''
https://coincheck.com/api/ticker

last	473400
bid	473400
ask	473404
high	480200
low	461017
volume	21855.48989698
timestamp	1503927864

'''


class BithumbModel(Model):
    api_url = ''
    
    def __init__(self, bitcoinName):
        if bitcoinName == 'BTC':
            self.api_url = 'https://api.bithumb.com/public/ticker/BTC'
        elif bitcoinName == 'LTC':
            self.api_url = 'https://api.bithumb.com/public/ticker/LTC'
        elif bitcoinName == 'ETH':
            self.api_url = 'https://api.bithumb.com/public/ticker/ETH'
        else:
            pass
        
        super(BithumbModel, self).__init__('Bithumb_' + bitcoinName)
    
    def GetTicker(self):
        # t_data = Ult.getURLData(self.api_url)['data']
        t_data = self.get_response(self.api_url)
        t_data.encoding = t_data.apparent_encoding
        self.date = t_data['date']
        self.buy = t_data.get('buy_price')
        self.sell = t_data.get('sell_price')
        self.last = float(t_data.get('closing_price'))
        # self.lastUSD = self.last * krw_usd
        # print('self.lastUSD : %s - %s' % (self.lastUSD, type(self.lastUSD)))
        self.high = t_data.get('max_price')
        self.low = t_data.get('min_price')
        self.vol = t_data.get('volume_1day')


'''

https://api.bithumb.com/public/ticker/{currency}更多
bithumb交易所最后交易信息
* {currency} = BTC, ETH, DASH, LTC, ETC, XRP, BCH (基本值: BTC), ALL(全部)
[Returned Example]
{
    "status": "0000",
    "data": {
        "opening_price" : "504000",
        "closing_price" : "505000",
        "min_price"     : "504000",
        "max_price"     : "516000",
        "average_price" : "509533.3333",
        "units_traded"  : "14.71960286",
        "volume_1day"   : "14.71960286",
        "volume_7day"   : "15.81960286",
        "buy_price"     : "505000",
        "sell_price"    : "504000",
        "date"          : 1417141032622
    }
}
Key Name 	Description
status	结果状态代码(正常 : 0000，正常外代码请参考错误代码)
opening_price	最近24小时内开始交易金额
closing_price	最近24小时内最后交易金额
min_price	最近24小时内最低交易金额
max_price	最近24小时内最高交易金额
average_price	最近24小时内平均交易金额
units_traded	最近24小时内Currency交易量
volume_1day	最近1天内Currency交易量
volume_7day	最近1天内Currency交易量
buy_price	交易等待件最高购买价
sell_price	交易等待件最小销售价
date	目前时间Timestamp

'''


class BitflyerModel(Model):
    api_url = ''
    
    def __init__(self, bitcoinName):
        if bitcoinName == 'BTC':
            self.api_url = 'https://api.bitflyer.jp/v1/ticker'
        # elif bitcoinName == 'LTC':
        #     self.api_url = 'https://api.bithumb.com/public/ticker/LTC'
        else:
            pass
        
        super(BitflyerModel, self).__init__('Bitflyer' + bitcoinName)
    
    def GetTicker(self):
        # t_data = Ult.getURLData(self.api_url)
        t_data = self.get_response(self.api_url)
        t_data.encoding = t_data.apparent_encoding
        self.date = t_data['timestamp']
        self.buy = t_data.get('buy_price')
        self.sell = t_data.get('sell_price')
        self.lastUSD = self.last * jpy_usd
        # print('self.lastUSD : %s - %s' % (self.lastUSD, type(self.lastUSD)))
        self.last = float(t_data.get('closing_price'))
        self.high = t_data.get('max_price')
        self.low = t_data.get('min_price')
        self.vol = t_data.get('volume_1day')


'''
https://api.bitflyer.jp/v1/ticker/BTC_JPY

  { "product_code": "BTC_JPY" },
  { "product_code": "FX_BTC_JPY" },
  { "product_code": "ETH_BTC" },

Response

{
  "product_code": "BTC_JPY",
  "timestamp": "2015-07-08T02:50:59.97",
  "tick_id": 3579,
  "best_bid": 30000,
  "best_ask": 36640,
  "best_bid_size": 0.1,
  "best_ask_size": 5,
  "total_bid_depth": 15.13,
  "total_ask_depth": 20,
  "ltp": 31690,
  "volume": 16819.26,
  "volume_by_product": 6819.26
}

'''

'''
curno: "KRW",curnm: "韩国元"
curno: "HKD",curnm: "港币"
curno: "EUR",curnm: "欧元"
curno: "CNY",curnm: "人民币"
curno: "JPY",curnm: "日元"



class GetTickerAndAnalysis(Crawler):
    def __init__(self):  # 类的初始化函数，在类中的函数都有个self参数，其实可以理解为这个类的对象
        Crawler.__init__(self)
        self.database_name = 'bitcoin'
        
        self.threading_number = 5  # 验证IP线程数量
        self.threading_pool_size = 5

        self.connargs['db'] = self.database_name
        # 初始化数据库连接
        try:
            if self.mysql is None:
                self.create_mysql(self.connargs)
        except Exception as e:
            print(e)
        
        # 生成数据库   create database if not exists ' + name
        self.mysql.insert("create database if not exists " + self.database_name)
        
        if not self.mysql.hasThisTable(self.file_proxy_all_list_table):
            self.mysql.insert(
                "create table if not exists " + self.file_proxy_all_list_table + "(id int not null AUTO_INCREMENT PRIMARY KEY ,ip char(30))")  # 自增长
        
        if not self.mysql.hasThisTable(self.file_proxy_valid_list_table):
            self.mysql.insert(
                "create table if not exists " + self.file_proxy_valid_list_table + "(id int not null AUTO_INCREMENT PRIMARY KEY ,ip char(30))")  # 自增长
        
'''

if __name__ == '__main__':
    waitTime = 5
    bitcoinList = []
    strBitcoinList = []
    
    # cny_usd = Ult.GetExchange('CNY')
    # jpy_usd = Ult.GetExchange('JPY')
    # krw_usd = Ult.GetExchange('KRW')
    
    exchange2 = Crawler.GetExchange()
    cny_usd = round(1/exchange2['CNY'], 6)
    jpy_usd = round(1/exchange2['JPY'], 6)
    # krw_usd = round(1/exchange2['KRW'], 6)
    
    print('cny_usd : %s' % cny_usd)
    print('jpy_usd : %s' % jpy_usd)
    # print('krw_usd : %s' % krw_usd)
    print('-'*80)
    # print ('cny_usd : %s' % cny_usd2)
    # print ('jpy_usd : %s' % jpy_usd2)
    # print ('krw_usd : %s' % krw_usd2)
    
    # BTCHuobi = HuobiModel('BTC')
    # BTCOkcoin = OkcoinModel('BTC')
    BTCBitfinex = BitfinexModel('BTC')
    BTCBitstamp = BitstampModel('BTC')
    BTCCoincheck = CoincheckModel('BTC')
    BTCBithumb = BithumbModel('BTC')
    # BTCBitflyer = BitflyerModel('BTC')
    
    strBitcoinList = ['BTCHuobi', 'BTCOkcoin', 'BTCBitfinex', 'BTCBitstamp', 'BTCCoincheck', 'BTCBithumb']
    bitcoinList = [BTCBitfinex, BTCBitstamp, BTCCoincheck, BTCBithumb]