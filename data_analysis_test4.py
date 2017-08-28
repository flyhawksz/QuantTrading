# coding=utf-8
from Ultility import ultility
import threading
import time
import pandas as pd


class Model(object):
    # waittime = 5
    def __init__(self, bitcoinName):
        self.name = bitcoinName
        self.date = ''  #: 返回数据时服务器时间
        self.buy = ''  #: 买一价
        self.high = ''  #: 最高价
        self.lastCNY = ''  #: 最新成交价
        self.lastUSD = ''  #: 最新成交价
        self.low = ''  #: 最低价
        self.sell = ''  #: 卖一价
        self.vol = ''  #: 成交量(最近的24小时)

    def Mod2Dic(self):
        t = {self.name: {'date': self.date, 'buy': self.buy, 'sell': self.sell,
             'high': self.high, 'low': self.low, 'lastCNY': self.lastCNY, 'lastUSD': self.lastUSD, 'vol': self.vol}}
        return t

    def Mod2Str(self):
        t = '%s, %s, %s, %s, %s, %s, %s, %s, %s' \
            % (self.name, self.date, self.buy, self.sell, self.high, self.low, self.lastCNY, self.lastUSD)
        return t


class HuobiBTC(Model):
    def __init__(self):
        super(HuobiBTC, self).__init__('Huobi_BTC')

    def GetTicker(self):
        t_url = 'http://api.huobi.com/staticmarket/ticker_btc_json.js'
        t_data = ultility.getURLData(t_url)
        self.date = t_data['time']
        self.buy = t_data.get('ticker')['buy']
        self.sell = t_data.get('ticker')['sell']
        self.lastCNY = t_data.get('ticker')['last']
        self.lastUSD = self.lastCNY / USD_RMB
        self.high = t_data.get('ticker')['high']
        self.low = t_data.get('ticker')['low']
        self.vol = t_data.get('ticker')['vol']



class HuobiLTC(Model):
    def __init__(self):
        super(HuobiLTC, self).__init__('Huobi_LTC')

    def GetTicker(self):
        t_url = 'http://api.huobi.com/staticmarket/ticker_ltc_json.js'
        t_data = ultility.getURLData(t_url)
        self.date = t_data['time']
        self.buy = t_data.get('ticker')['buy']
        self.sell = t_data.get('ticker')['sell']
        self.lastCNY = t_data.get('ticker')['last']
        self.lastUSD = self.lastCNY / USD_RMB
        self.high = t_data.get('ticker')['high']
        self.low = t_data.get('ticker')['low']
        self.vol = t_data.get('ticker')['vol']

        # print("%s CNY: %s USD %s" %(targeName,t_last,t_last*100/self.USD_RMB))
        # time.sleep(self.waitTime)
        # time.sleep(super(HuobiLTC, self).waitime)

        '''
        ##实时行情数据接口 目前支持人民币现货、美元现货 ###数据文件： 
        [BTC-CNY] http://api.huobi.com/staticmarket/ticker_btc_json.js
        [LTC-CNY] http://api.huobi.com/staticmarket/ticker_ltc_json.js
        [BTC-USD] http://api.huobi.com/usdmarket/ticker_btc_json.js
        ###数据格式:
        {"time":"1378137600","ticker":{"high":86.48,"low":79.75,"symbol":"btccny","last":83.9,"vol":2239560.1752883,"buy":83.88,"sell":83.9}}
        报价：最高价，最低价，当前价，成交量，买1，卖1 ##深度数据接口（json格式） ###数据文件 [BTC-CNY] http://api.huobi.com/staticmarket/depth_btc_json.js
        [LTC-CNY] http://api.huobi.com/staticmarket/depth_ltc_json.js
        [BTC-USD] http://api.huobi.com/usdmarket/depth_btc_json.js
        指定深度数据条数（1-150条）
        [BTC-CNY] http://api.huobi.com/staticmarket/depth_btc_X.js
        [LTC-CNY] http://api.huobi.com/staticmarket/depth_ltc_X.js
        [BTC-USD] http://api.huobi.com/usdmarket/depth_btc_X.js
        X表示返回多少条深度数据，可取值 1-150
        ###数据格式
        {"asks":[[90.8,0.5],...],"bids":[[86.06,79.243],...]],"symbol":"btccny"}
        卖:价格:累积量,... 买:价格:累积量...
        :return: 
        '''


class OkcoinBTC(Model):
    def __init__(self):
            super(OkcoinBTC, self).__init__('Okcoin_BTC')

    def GetTicker(self):
        t_url = 'https://www.okcoin.cN/api/v1/ticker.do?symbol=btc_cny'
        # t_url = 'https://www.okcoin.cn/api/v1/ticker.do?symbol=btc_usd'
        t_data = ultility.getURLData(t_url)
        self.date = t_data['date']
        self.buy = t_data.get('ticker')['buy']
        self.sell = t_data.get('ticker')['sell']
        self.lastCNY = t_data.get('ticker')['last']
        self.lastUSD = float(self.lastCNY) / USD_RMB
        self.high = t_data.get('ticker')['high']
        self.low = t_data.get('ticker')['low']
        self.vol = t_data.get('ticker')['vol']

            # t_last = t_data.get('ticker')['last']
            # print("%s CNY: %s USD %s" %(targeName,t_last,float(t_last)*100/USD_RMB))
            # time.sleep(waitTime)
#
#     # '''
#     # url = 'https://www.okcoin.cn/api/v1/ticker.do?symbol=btc_cny'
#     #
#     # :return:
#     # '''


class BitstampBTC(Model):
    def __init__(self):
        super(BitstampBTC, self).__init__('Bitstamp_BTC')
        
    def GetTicker(self):
        t_url = 'https://www.bitstamp.net/api/ticker/'
        t_data = ultility.getURLData(t_url)
        self.date = t_data['timestamp']
        self.buy = t_data.get('bid')
        self.sell = t_data.get('ask')
        self.lastUSD = float(t_data.get('last'))
        # print('self.lastUSD : %s - %s' % (self.lastUSD, type(self.lastUSD)))
        self.lastCNY = self.lastUSD * USD_RMB
        self.high = t_data.get('high')
        self.low = t_data.get('low')
        self.vol = t_data.get('volume')
#
#         # t_data = GetData(t_url)
#         # t_last = t_data['last']
#         # print("%s : %s" %(targeName,t_last))
#         time.sleep(waitTime)
#     '''
#     TICKERPassing any GET parameters, will result in your request being rejected.
#     Request
#     GET https://www.bitstamp.net/api/ticker/
#         Returns data for the BTC/USD currency pair.
#     GET https://www.bitstamp.net/api/v2/ticker/{currency_pair}/API v2
#         Supported values for currency_pair: btcusd, btceur, eurusd, xrpusd, xrpeur, xrpbtc, ltcusd, ltceur, ltcbtc
#     Response (JSON)
#     last    Last BTC price.
#     high    Last 24 hours price high.
#     low Last 24 hours price low.
#     vwap    Last 24 hours volume weighted average price.
#     volume  Last 24 hours volume.
#     bid Highest buy order.
#     ask Lowest sell order.
#     timestamp   Unix timestamp date and time.
#     open    First price of the day.HOURLY TICKERPassing any GET parameters, will result in your request being rejected.
#     Request
#     GET https://www.bitstamp.net/api/ticker_hour/
#         Returns data for the BTC/USD currency pair.
#     GET https://www.bitstamp.net/api/v2/ticker_hour/{currency_pair}/API v2
#         Supported values for currency_pair: btcusd, btceur, eurusd, xrpusd, xrpeur, xrpbtc, ltcusd, ltceur, ltcbtc
#     Response (JSON)
#     Returns a JSON dictionary like the ticker call, with the calculated values being from within an hour.ORDER BOOKPassing any GET parameters, will result in your request being rejected.
#     Request
#     GET https://www.bitstamp.net/api/order_book/
#         Returns data for the BTC/USD currency pair.
#     GET https://www.bitstamp.net/api/v2/order_book/{currency_pair}/API v2
#         Supported values for currency_pair: btcusd, btceur, eurusd, xrpusd, xrpeur, xrpbtc, ltcusd, ltceur, ltcbtc
#     Returns a JSON dictionary like the ticker call, with the calculated values being from within an hour.
#     Response (JSON)
#     Returns a JSON dictionary with "bids" and "asks". Each is a list of open orders and each order is represented as a list holding the price and the amount.
#     '''


class BitfinexBTC(Model):
    def __init__(self):
        super(BitfinexBTC, self).__init__('Bitfinex_BTC')

    def GetTicker(self):
        t_url = 'https://api.bitfinex.com/v1/pubticker/btcusd'
        t_data = ultility.getURLData(t_url)
        self.date = t_data['timestamp'].split('.')[0]
        self.buy = t_data.get('ask')
        self.sell = t_data.get('bid')
        self.lastUSD = float(t_data.get('last_price'))
        # print('self.lastUSD : %s - %s' % (self.lastUSD, type(self.lastUSD)))
        self.lastCNY = self.lastUSD * USD_RMB
        self.high = t_data.get('high')
        self.low = t_data.get('low')
        self.vol = t_data.get('volume')

        # t_last = t_data['last_price']
        # print("%s : %s" % (self.name, self.last))
        # time.sleep(waitTime)
#     '''
#     https://api.bitfinex.com/v1/pubticker/btcusd
#     '''


waitTime = 5
USD_RMB = ultility.getUSDexchange()
print(USD_RMB)

BTCHuobi = HuobiBTC()
BTCOkcoin = OkcoinBTC()
BTCBitfinex = BitfinexBTC()
BTCBitstamp = BitstampBTC()



def getHuobiTicker():
    BTCHuobi.GetTicker()
    # print BTCHuobi.Mod2Dic()

def getHuobiTicker():
    BTCHuobi.GetTicker()

def getHuobiTicker():
    BTCHuobi.GetTicker()

def getHuobiTicker():
    BTCHuobi.GetTicker()

def getHuobiTicker():
    BTCHuobi.GetTicker()

def startMain():
    HuobiBTCTicker = threading.Thread(target=getHuobiTicker)
    HuobiBTCTicker.start()

    while 1:
        BTCHuobi.GetTicker()
        print BTCHuobi.Mod2Dic()
        time.sleep(waitTime)

        # Huobi_BTC.GetTicker()
        # BTCDic.update(Huobi_BTC.Mod2Dic())
        # # BTCDic.update(Okcoin_BTC.Mod2Dic())
        # # BTCDic.update(Bitfinex_BTC.Mod2Dic())
        # # BTCDic.update(Bitstamp_BTC.Mod2Dic())
        #
        # frameBTC = pd.DataFrame(BTCDic).T
        # frameBTC = frameBTC.sort_values(by=['lastUSD'])
        # serierBTC = frameBTC['lastUSD']
        # # print(serierBTC)
        # serierBTC = serierBTC/serierBTC[0]-1
        # # print (serierBTC)
        # frameBTC['Dif'] = serierBTC
        # print(frameBTC.loc[:, ['lastCNY', 'lastUSD', 'Dif']])
        # print ('-' * 80)

        # time.sleep(waitTime)





if __name__ == "__main__":
    startMain()
