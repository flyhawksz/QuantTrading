import os
import time
import tushare as ts
import pandas as pd


def check(code, low, high):
    df = ts.get_realtime_quotes(code)
    e = df[['code', 'name', 'price', 'time']]
    p = df[u'price']
    print e
    if float(p[0]) > low and float(p[0]) < high:
        return True
    else:
        return False


while True:
    if check('sh', 3200, 10000) or check('601318', 0, 49):
        os.system('play bell.wav')
        exit()
    time.sleep(5)