# coding=utf-8
import requests
import re

def rmbusb():
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

def rmbusb2():
    import urllib2
    import re
    import json
    fp = urllib2.urlopen(
        'http://webforex.hermes.hexun.com/forex/quotelist?code=FOREXUSDCNY,&column=code,price,UpdownRate&callback=ongetjsonpforex&_=1451543515359')
    html = fp.read().decode("utf-8")
    fp.close()
    s = re.findall("(.∗)", str(html))[0]
    sjson = json.loads(s)
    print sjson
    USDCNY = sjson["Data"][0][0][1] / 10000
    print(USDCNY)

rmbusb2()