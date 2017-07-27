#coding=utf-8
import urllib.request
import json

def startMain():
    url = 'https://www.okcoin.cn/api/v1/ticker.do?symbol=btc_cny'
    response = urllib.request.urlopen(url, timeout=3)  # 打开连接，timeout为请求超时时间
    data = response.read().decode('utf-8')  # 返回结果解码
    json_data = json.loads(data)
    print(data, type(data))
    print(json_data)
    print(json_data['ticker']['buy'])


    url = 'https://www.bitstamp.net/api/ticker/'
    response = urllib.request.urlopen(url)
    data = response.read().decode('utf-8')  # 返回结果解码
    json_data = json.loads(data)

    exchange_name = 'Bitstamp'
    btc_in_usd = float(resp['last'])
    print(data, type(data))
    print(json_data)
    print(json_data['last'])

if __name__=="__main__":
    startMain()

