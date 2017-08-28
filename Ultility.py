# coding=utf-8

import urllib2
import json
import re
import requests

class ultility:
    def __init__(self):
        pass

    @staticmethod
    def getUSDexchange():
        url = "http://www.boc.cn/sourcedb/whpj/"
        html = requests.get(url).content.decode('utf-8')
        # print(html)
        result = re.findall('(?<=<td>).+?(?=</td>)', html)
        # print(result)
        # print(type(result))
        # for i in range(len(result)):
        #    print("%d : %s" % (i, result[i]))

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
