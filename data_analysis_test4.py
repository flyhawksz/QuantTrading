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
             'high': self.high, 'low': self.low, 'lastCNY': self.lastCNY, 'lastUSD': self.lastUSD, 'vol': self.vol}}
        return t

    def Mod2Str(self):
        t = '%s, %s, %s, %s, %s, %s, %s, %s, %s' \
            % (self.name, self.date, self.buy, self.sell, self.high, self.low, self.lastCNY, self.lastUSD)
        return t


class HuobiModel(Model):
    api_url = ''
    def __init__(self, bitcoinName):
        if bitcoinName == 'BTC':
            self.api_url = 'http://api.huobi.com/staticmarket/ticker_btc_json.js'
        elif bitcoinName == 'LTC':
            self.api_url ='http://api.huobi.com/staticmarket/ticker_ltc_json.js'
        else:
            pass

        super(HuobiModel, self).__init__('Huobi_' + bitcoinName)

    def GetTicker(self):
        t_data = ultility.getURLData(t_url)
        self.date = t_data['time']
        self.buy = t_data.get('ticker')['buy']
        self.sell = t_data.get('ticker')['sell']
        self.last = t_data.get('ticker')['last']
        self.lastUSD = self.last/USD_RMB
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
        else:
            pass

        super(OkcoinModel, self).__init__('Okcoin_' + bitcoinName)

    def GetTicker(self):
        t_data = ultility.getURLData(self.api_url)
        self.date = t_data['date']
        self.buy = t_data.get('ticker')['buy']
        self.sell = t_data.get('ticker')['sell']
        self.last = t_data.get('ticker')['last']
        self.lastUSD = float(self.last)/USD_RMB
        self.high = t_data.get('ticker')['high']
        self.low = t_data.get('ticker')['low']
        self.vol = t_data.get('ticker')['vol']

            # t_last = t_data.get('ticker')['last']
            # print("%s CNY: %s USD %s" %(targeName,t_last,float(t_last)*100/USD_RMB))
            # time.sleep(waitTime)


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
class BitstampModel(Model):
    api_url = ''
    def __init__(self, bitcoinName):
        if bitcoinName == 'BTC':
            # self.api_url = 'https://www.bitstamp.net/api/ticker/'
            self.api_url = 'https://www.bitstamp.net/api/v2/ticker/btcusd'
        elif bitcoinName == 'LTC':
            self.api_url = 'https://www.bitstamp.net/api/v2/ticker/ltcusd'
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



class BitfinexModel(Model):
    api_url = ''

    def __init__(self, bitcoinName):
        if bitcoinName == 'BTC':
            self.api_url = 'https://api.bitfinex.com/v1/pubticker/btcusd'
        elif bitcoinName == 'LTC':
            self.api_url = 'https://api.bitfinex.com/v1/pubticker/ltcusd'
        else:
            pass

        super(BitfinexModel, self).__init__('Bitfinex' + bitcoinName)

    def GetTicker(self):
        t_data = ultility.getURLData(self.api_url)
        self.date = t_data['timestamp'].split('.')[0]
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
        else:
            pass

        super(BithumbModel, self).__init__('Bithumb' + bitcoinName)

    def GetTicker(self):
        t_data = ultility.getURLData(self.api_url)
        self.date = t_data['date']
        self.buy = t_data.get('buy_price')
        self.sell = t_data.get('sell_price')
        self.lastUSD = self.last*
        # print('self.lastUSD : %s - %s' % (self.lastUSD, type(self.lastUSD)))
        self.last = float(t_data.get('closing_price'))
        self.high = t_data.get('high')
        self.low = t_data.get('low')
        self.vol = t_data.get('volume')
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
