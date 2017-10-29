# -*- coding: utf-8 -*-
"""

@author: luke
"""

from binanceapi import api as b
import pprint

api_key = ''
api_secret = ''

# Symbol parameter (e.g. 'WTCBTC') is passed in via instance, i.e. you do not put
# symbol in method parameter

# Timestamp parameter required! it's cooked in!
WTC = b.Binance("WTCBTC", api_key, api_secret)
WTC = WTC.account_tradelist()

XVG = b.Binance("NEOTC", api_key, api_secret)
XVG = XVG.account_tradelist()

pprint.pprint(WTC)
pprint.pprint(XVG)

#from here you can multithread many currencies to display and run

