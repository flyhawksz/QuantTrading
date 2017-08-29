# coding=utf-8

import urllib2
import json
import re
import requests
import json
import urllib
from urllib import urlencode


class ultility:
    def __init__(self):
        pass

    @staticmethod
    def GetExchange(source, target='USD'):
        # use k789 api data
        exchange_rate = 0
        url = 'http://api.k780.com'
        params = {
            'app': 'finance.rate',
            'scur': source,
            'tcur': target,
            'appkey': '27849',
            'sign': '7fd967ecc9c404c5d3e295804edfb2ce',
            'format': 'json',
        }
        params = urlencode(params)

        f = urllib.urlopen('%s?%s' % (url, params))
        nowapi_call = f.read()
        # print content
        a_result = json.loads(nowapi_call)
        if a_result:
            if a_result['success'] != '0':
                # print a_result['result'];
                exchange_rate = float(a_result['result']['rate'])
            else:
                print a_result['msgid'] + ' ' + a_result['msg']
        else:
            print 'Request nowapi fail.'

        return exchange_rate

    @staticmethod
    def GetExchange2():
        # use openexchangerates api data
        appID = '13090c130b794ccb99e1805586f96c66'
        symbols = 'JPY,CNY,KRW'
        turl = 'https://openexchangerates.org/api/latest.json'
        print ('%s?app_id=%s&symbols=%s' %(turl, appID, symbols))
        fp = urllib2.urlopen('%s?app_id=%s&symbols=%s' %(turl, appID, symbols))
        resp = fp.read() #.decode("utf-8")
        fp.close()
        a_result = json.loads(resp)
        if a_result:
            print (a_result)
            return a_result['rates']
    '''
    curno: "KRW",curnm: "韩国元"
    curno: "HKD",curnm: "港币"
    curno: "EUR",curnm: "欧元"
    curno: "CNY",curnm: "人民币"
    curno: "JPY",curnm: "日元"
    '''




    @staticmethod
    def getUSDexchange():
        url = "http://www.boc.cn/sourcedb/whpj/"
        html = requests.get(url).content.decode('utf-8')
        # print(html)
        result = re.findall('(?<=<td>).+?(?=</td>)', html)
        # print(result)
        # print(type(result))
        for i in range(len(result)):
           print("%d : %s" % (i, result[i]))

        USD_RMB = float(result[192]) / 100
        # print('USD-RMB : %s' % USD_RMB)
        return  USD_RMB

    @staticmethod
    def getURLData(t_url):
        # print(t_url)
        req = urllib2.Request(t_url)  # 打开连接，timeout为请求超时时间
        res = urllib2.urlopen(req, None, 5)
        data = res.read().decode('utf-8')  # 返回结果解码
        json_data = json.loads(data)
        # list_all_dict(json_data)
        return json_data

    @staticmethod
    def PrintResult(t_url):
        print(t_url)
        response = urllib2.request.urlopen(t_url, timeout=5)  # 打开连接，timeout为请求超时时间
        data = response.read().decode('utf-8')  # 返回结果解码
        json_data = json.loads(data)
        print(data, type(data))
        print('-' * 30)
        print(json_data, type(json_data))

        ultility.list_all_dict(json_data)

    @staticmethod
    def list_all_dict(objdict):
        tempstring = ''
        if isinstance(objdict, dict):  # 使用isinstance检测数据类型
            for x in range(len(objdict)):
                temp_key = list(objdict.keys())[x]
                temp_value = objdict[temp_key]
                tempstring = tempstring + "%s : %s" % (temp_key, temp_value) + '\n'
                ultility.list_all_dict(temp_value)  # 自我调用实现无限遍历

            print('*' * 40)