# coding=utf-8
#python
import json
import urllib
from urllib import urlencode

url = 'http://api.k780.com'
params = {
  'app' : 'finance.rate',
  'scur' : 'USD',
  'tcur' : 'CNY',
  'appkey' : '27849',
  'sign' : '7fd967ecc9c404c5d3e295804edfb2ce',
  'format' : 'json',
}
params = urlencode(params)

f = urllib.urlopen('%s?%s' % (url, params))
nowapi_call = f.read()
#print content
a_result = json.loads(nowapi_call)
if a_result:
  if a_result['success'] != '0':
    print a_result['result'];
  else:
    print a_result['msgid']+' '+a_result['msg']
else:
  print 'Request nowapi fail.'