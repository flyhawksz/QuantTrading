# -*- coding: utf-8 -*-
# @Time    : 2019-5-23 15:29
# @Author  : flyhawk
# @Email   : flyhawksz@163.com
# @File    : get_ticker.py
# @Software: PyCharm

# -*- coding: utf-8 -*-

import asyncio
import os
import sys
from pprint import pprint

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root + '/python')

import ccxt.async_support as ccxt  # noqa: E402

pprint(asyncio.get_event_loop().run_until_complete(ccxt.binance().fetch_ticker('ETH/BTC')))