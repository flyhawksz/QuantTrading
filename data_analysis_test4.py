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


class HuobiModel(Model):
    api_url = ''
    def __init__(self, bitcoinName):
        if bitcoinName == 'BTC':
            self.api_url = 'http://api.huobi.com/staticmarket/ticker_btc_json.js'
        elif bitcoinName == 'LTC':
            self.api_url ='http://api.huobi.com/staticmarket/ticker_ltc_json.js'
        # elif bitcoinName == 'ETH':
        #     self.api_url ='https://be.huobi.com/market/detail?symbol=ethcny'
        else:
            pass

        super(HuobiModel, self).__init__('Huobi_' + bitcoinName)

    def GetTicker(self):
        t_data = ultility.getURLData(self.api_url)
        self.date = t_data['time']
        self.buy = t_data.get('ticker')['buy']
        self.sell = t_data.get('ticker')['sell']
        self.last = t_data.get('ticker')['last']
        self.lastUSD = self.last * cny_usd
        self.high = t_data.get('ticker')['high']
        self.low = t_data.get('ticker')['low']
        self.vol = t_data.get('ticker')['vol']

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


class OkcoinModel(Model):
    api_url = ''
    def __init__(self, bitcoinName):
        if bitcoinName == 'BTC':
            self.api_url = 'https://www.okcoin.cn/api/v1/ticker.do?symbol=btc_cny'
        elif bitcoinName == 'LTC':
            self.api_url = 'https://www.okcoin.cn/api/v1/ticker.do?symbol=ltc_cny'
        elif bitcoinName == 'ETH':
            self.api_url = 'https://www.okcoin.cn/api/v1/ticker.do?symbol=eth_cny'
        else:
            pass

        super(OkcoinModel, self).__init__('Okcoin_' + bitcoinName)

    def GetTicker(self):
        t_data = ultility.getURLData(self.api_url)
        self.date = t_data['date']
        self.buy = t_data.get('ticker')['buy']
        self.sell = t_data.get('ticker')['sell']
        self.last = t_data.get('ticker')['last']
        self.lastUSD = float(self.last) * cny_usd
        self.high = t_data.get('ticker')['high']
        self.low = t_data.get('ticker')['low']
        self.vol = t_data.get('ticker')['vol']


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
        t_data = ultility.getURLData(self.api_url)
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
        t_data = ultility.getURLData(self.api_url)
        self.date = t_data['timestamp'] # .split('.')[0]
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
        t_data = ultility.getURLData(self.api_url)
        self.date = t_data['timestamp'] # .split('.')[0]
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
        t_data = ultility.getURLData(self.api_url)['data']
        self.date = t_data['date']
        self.buy = t_data.get('buy_price')
        self.sell = t_data.get('sell_price')
        self.last = float(t_data.get('closing_price'))
        self.lastUSD = self.last * krw_usd
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
        t_data = ultility.getURLData(self.api_url)
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

'''

waitTime = 5
bitcoinList = []
strBitcoinList = []

# cny_usd = ultility.GetExchange('CNY')
# jpy_usd = ultility.GetExchange('JPY')
# krw_usd = ultility.GetExchange('KRW')

exchange2 = ultility.GetExchange2()
cny_usd = round(1/exchange2['CNY'], 6)
jpy_usd = round(1/exchange2['JPY'], 6)
krw_usd = round(1/exchange2['KRW'], 6)


print ('cny_usd : %s' % cny_usd)
print ('jpy_usd : %s' % jpy_usd)
print ('krw_usd : %s' % krw_usd)
print ('-'*80)
# print ('cny_usd : %s' % cny_usd2)
# print ('jpy_usd : %s' % jpy_usd2)
# print ('krw_usd : %s' % krw_usd2)

BTCHuobi = HuobiModel('BTC')
BTCOkcoin = OkcoinModel('BTC')
BTCBitfinex = BitfinexModel('BTC')
BTCBitstamp = BitstampModel('BTC')
BTCCoincheck = CoincheckModel('BTC')
BTCBithumb = BithumbModel('BTC')
# BTCBitflyer = BitflyerModel('BTC')

strBitcoinList = ['BTCHuobi', 'BTCOkcoin', 'BTCBitfinex', 'BTCBitstamp', 'BTCCoincheck', 'BTCBithumb']
bitcoinList = [BTCHuobi, BTCOkcoin, BTCBitfinex, BTCBitstamp, BTCCoincheck, BTCBithumb]


def getBTCHuobiTicker():
    BTCHuobi.GetTicker()
    # print BTCHuobi.Mod2Dic()

def getBTCOkcoinTicker():
    BTCOkcoin.GetTicker()

def getBTCBitfinexTicker():
    BTCBitfinex.GetTicker()

def getBTCBitstampTicker():
    BTCBitstamp.GetTicker()

def getBTCCoincheckTicker():
    BTCCoincheck.GetTicker()

def getBTCBithumbTicker():
    BTCBithumb.GetTicker()

def getBTCCoincheckTicker():
    BTCCoincheck.GetTicker()

# def getBTCBitflyerTicker():
#     BTCBitflyer.GetTicker()


LTCHuobi = HuobiModel('LTC')
LTCOkcoin = OkcoinModel('LTC')
LTCBitfinex = BitfinexModel('LTC')
LTCBitstamp = BitstampModel('LTC')
# LTCCoincheck = CoincheckModel('LTC')
LTCBithumb = BithumbModel('LTC')

strBitcoinList2 = ['LTCHuobi', 'LTCOkcoin', 'LTCBitfinex', 'LTCBitstamp', 'LTCBithumb']
bitcoinList2 = [LTCHuobi, LTCOkcoin, LTCBitfinex, LTCBitstamp, LTCBithumb]

def getLTCHuobiTicker():
    LTCHuobi.GetTicker()
    # print LTCHuobi.Mod2Dic()

def getLTCOkcoinTicker():
    LTCOkcoin.GetTicker()

def getLTCBitfinexTicker():
    LTCBitfinex.GetTicker()

def getLTCBitstampTicker():
    LTCBitstamp.GetTicker()

# def getLTCCoincheckTicker():
#     LTCCoincheck.GetTicker()

def getLTCBithumbTicker():
    LTCBithumb.GetTicker()

# def getLTCBitflyerTicker():
#     LTCBitflyer.GetTicker()


# ETHHuobi = HuobiModel('ETH')
ETHOkcoin = OkcoinModel('ETH')
ETHBitfinex = BitfinexModel('ETH')
ETHBitstamp = BitstampModel('ETH')
# ETHCoincheck = CoincheckModel('ETH')
ETHBithumb = BithumbModel('ETH')

strBitcoinList3 = ['ETHOkcoin', 'ETHBitfinex', 'ETHBitstamp', 'ETHBithumb']
bitcoinList3 = [ETHOkcoin, ETHBitfinex, ETHBitstamp, ETHBithumb]

# def getETHHuobiTicker():
#     ETHHuobi.GetTicker()
    # print ETHHuobi.Mod2Dic()

def getETHOkcoinTicker():
    ETHOkcoin.GetTicker()

def getETHBitfinexTicker():
    ETHBitfinex.GetTicker()

def getETHBitstampTicker():
    ETHBitstamp.GetTicker()

# def getETHCoincheckTicker():
#     ETHCoincheck.GetTicker()

def getETHBithumbTicker():
    ETHBithumb.GetTicker()


def startMain():
    BTCDic = {}
    LTCDic = {}
    ETHDic = {}

    for strBitcoin in strBitcoinList:
        BTCTicker = threading.Thread(target=eval('get' + strBitcoin + 'Ticker'))
        BTCTicker.start()

    for strBitcoin in strBitcoinList2:
        LTCTicker = threading.Thread(target=eval('get' + strBitcoin + 'Ticker'))
        LTCTicker.start()

    for strBitcoin in strBitcoinList3:
        ETHTicker = threading.Thread(target=eval('get' + strBitcoin + 'Ticker'))
        ETHTicker.start()

    while 1:
        # --------------------for BTC -------------------------
        for bitcoin in bitcoinList:
            bitcoin.GetTicker()
            # print bitcoin.Mod2Dic()
            BTCDic.update(bitcoin.Mod2Dic())

        frameBTC = pd.DataFrame(BTCDic).T
        frameBTC = frameBTC.sort_values(by=['lastUSD'])
        serierBTC = frameBTC['lastUSD']
        # print(serierBTC)
        serierBTC = serierBTC / serierBTC[0] - 1
        # print (serierBTC)
        frameBTC['Dif'] = serierBTC
        print(frameBTC.loc[:, ['lastUSD', 'Dif']])
        print ('-' * 80)
        ultility.DataFrame2Excel(frameBTC.loc[:, ['lastUSD', 'Dif']], 'frameBTC')
        # time.sleep(waitTime)
        # --------------------for LTC -------------------------
        for bitcoin in bitcoinList2:
            bitcoin.GetTicker()
            # print bitcoin.Mod2Dic()
            LTCDic.update(bitcoin.Mod2Dic())

        frameLTC = pd.DataFrame(LTCDic).T
        frameLTC = frameLTC.sort_values(by=['lastUSD'])
        serierLTC = frameLTC['lastUSD']
        # print(serierBTC)
        serierLTC = serierLTC / serierLTC[0] - 1
        # print (serierBTC)
        frameLTC['Dif'] = serierLTC
        print(frameLTC.loc[:, ['lastUSD', 'Dif']])
        print ('-' * 80)
        ultility.DataFrame2Excel(frameLTC.loc[:, ['lastUSD', 'Dif']], 'frameLTC')
        # --------------------for ETH -------------------------
        for bitcoin in bitcoinList3:
            bitcoin.GetTicker()
            # print bitcoin.Mod2Dic()
            ETHDic.update(bitcoin.Mod2Dic())

        frameETH = pd.DataFrame(ETHDic).T
        frameETH = frameETH.sort_values(by=['lastUSD'])
        serierETH = frameETH['lastUSD']
        # print(serierBTC)
        serierETH = serierETH / serierETH[0] - 1
        # print (serierBTC)
        frameETH['Dif'] = serierETH
        print(frameETH.loc[:, ['lastUSD', 'Dif']])
        print ('*' * 80)
        ultility.DataFrame2Excel(frameETH.loc[:, ['lastUSD', 'Dif']], 'frameETH')
        time.sleep(waitTime)

if __name__ == "__main__":
    startMain()


