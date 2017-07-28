#coding=utf-8
import urllib.request
import json
import threading
import time
import requests
import re

waitTime = 10
USD_RMB = 0

def GetUSDExchange():
    global USD_RMB
    url = "http://www.boc.cn/sourcedb/whpj/"
    html = requests.get(url).content.decode('utf-8')
    # print(html)
    result = re.findall('(?<=<td>).+?(?=</td>)', html)
    #print(result)
    #print(type(result))
    #for i in range(len(result)):
    #    print("%d : %s" % (i, result[i]))

    USD_RMB = float(result[192])
    print(USD_RMB)


def GetData(t_url):
    #print(t_url)
    response = urllib.request.urlopen(t_url, timeout=5)  # 打开连接，timeout为请求超时时间
    data = response.read().decode('utf-8')  # 返回结果解码
    json_data = json.loads(data)
    #list_all_dict(json_data)
    return json_data

def Huobi_Ticker(targeName):
    global USD_RMB
    global waitTime
    while True:
        t_url = 'http://api.huobi.com/staticmarket/ticker_btc_json.js'
        t_data = GetData(t_url)
        t_last = t_data.get('ticker')['last']
        print("%s CNY: %s USD %s" %(targeName,t_last,t_last*100/USD_RMB))
        time.sleep(waitTime)

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

def Okcoin_Ticker(targeName):
    global USD_RMB
    global waitTime
    while True:
        t_url = 'https://www.okcoin.cN/api/v1/ticker.do?symbol=btc_cny'
        #t_url = 'https://www.okcoin.cn/api/v1/ticker.do?symbol=btc_usd'
        t_data = GetData(t_url)
        t_last = t_data.get('ticker')['last']
        print("%s CNY: %s USD %s" %(targeName,t_last,float(t_last)*100/USD_RMB))
        time.sleep(waitTime)
        '''
        url = 'https://www.okcoin.cn/api/v1/ticker.do?symbol=btc_cny'
    
        :return:
        '''

def Bitstamp_Ticker(targeName):
    global waitTime
    while True:
        t_url = 'https://www.bitstamp.net/api/ticker/'
        t_data = GetData(t_url)
        t_last = t_data['last']
        print("%s : %s" %(targeName,t_last))
        time.sleep(waitTime)
        '''
        TICKERPassing any GET parameters, will result in your request being rejected.
        Request
        GET https://www.bitstamp.net/api/ticker/
            Returns data for the BTC/USD currency pair.
        GET https://www.bitstamp.net/api/v2/ticker/{currency_pair}/API v2
            Supported values for currency_pair: btcusd, btceur, eurusd, xrpusd, xrpeur, xrpbtc, ltcusd, ltceur, ltcbtc
        Response (JSON)
        last    Last BTC price.
        high    Last 24 hours price high.
        low Last 24 hours price low.
        vwap    Last 24 hours volume weighted average price.
        volume  Last 24 hours volume.
        bid Highest buy order.
        ask Lowest sell order.
        timestamp   Unix timestamp date and time.
        open    First price of the day.HOURLY TICKERPassing any GET parameters, will result in your request being rejected.
        Request
        GET https://www.bitstamp.net/api/ticker_hour/
            Returns data for the BTC/USD currency pair.
        GET https://www.bitstamp.net/api/v2/ticker_hour/{currency_pair}/API v2
            Supported values for currency_pair: btcusd, btceur, eurusd, xrpusd, xrpeur, xrpbtc, ltcusd, ltceur, ltcbtc
        Response (JSON)
        Returns a JSON dictionary like the ticker call, with the calculated values being from within an hour.ORDER BOOKPassing any GET parameters, will result in your request being rejected.
        Request
        GET https://www.bitstamp.net/api/order_book/
            Returns data for the BTC/USD currency pair.
        GET https://www.bitstamp.net/api/v2/order_book/{currency_pair}/API v2
            Supported values for currency_pair: btcusd, btceur, eurusd, xrpusd, xrpeur, xrpbtc, ltcusd, ltceur, ltcbtc
        Returns a JSON dictionary like the ticker call, with the calculated values being from within an hour.
        Response (JSON)
        Returns a JSON dictionary with "bids" and "asks". Each is a list of open orders and each order is represented as a list holding the price and the amount.
        '''


def Bitfinex_Ticker(targeName):
    global waitTime
    while True:
        t_url = 'https://api.bitfinex.com/v1/pubticker/btcusd'
        t_data = GetData(t_url)
        t_last = t_data['last_price']
        print("%s : %s" %(targeName,t_last))
        time.sleep(waitTime)
        '''
        https://api.bitfinex.com/v1/pubticker/btcusd
        '''

def PrintResult(t_url):
    print(t_url)
    response = urllib.request.urlopen(t_url, timeout=5)  # 打开连接，timeout为请求超时时间
    data = response.read().decode('utf-8')  # 返回结果解码
    json_data = json.loads(data)
    print(data, type(data))
    print('-'*30)
    print(json_data,type(json_data))

    list_all_dict(json_data)


def list_all_dict(dict_a):
    if isinstance(dict_a,dict) : #使用isinstance检测数据类型
        for x in range(len(dict_a)):
            temp_key = list(dict_a.keys())[x]
            temp_value = dict_a[temp_key]
            print("%s : %s" %(temp_key,temp_value))
            list_all_dict(temp_value) #自我调用实现无限遍历

        print('*'*40)


def startMain():
    GetUSDExchange()
    t_Target = ['Huobi','Okcoin','Bitfinex','Bitstamp']

    for t_targetName in t_Target:
        t_targetName2 = t_targetName + '_Ticker'
        print(t_targetName2)
        t = threading.Thread(target=eval(t_targetName2), args=(t_targetName,))
        t.start()

    #Huobi_Ticker()
    #Okcoin_Ticker()
    #Bitfinex_Ticker()
    #Bitstamp_Ticker()



if __name__=="__main__":
    startMain()

