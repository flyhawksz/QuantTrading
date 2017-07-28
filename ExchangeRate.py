#coding=utf-8
import urllib
import requests
import re
import sys

url="http://www.boc.cn/sourcedb/whpj/"
html=requests.get(url).content.decode('utf-8')
#print(html)
result = re.findall('(?<=<td>).+?(?=</td>)',html)
print(result)
print(type(result))
for i in range(len(result)):
    print("%d : %s" %(i,result[i]))
print(result[192]+"\n")

