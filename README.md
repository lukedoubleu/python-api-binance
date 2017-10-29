# python-binance-api
BACKGROUND: I originally wanted to do my quick job listings at busstops for those riding bus and encouraging bus use (Inequality/Environment), but lacked the team to pull it all together - definitely bigger than 24 hours for only me. So I wrote what I think might be a possible candidate for Inequality - a cryptoexchange shell. Cryptocurrency is leveling the playing field, allowing those not born into large wealth to understand financial markets and earn assets, yielding upward social mobility. Every generation or so, we experience this phenomena (most previous was dot-com era in late 90s) that allows "commoners" to gain access to a vast world otherwise not accessible due to access to education, birth conditions, and upbringing. The end goal shouldn't be vast wealth however, it's the knowledge gained in understanding how financial and wealth management operate, skills that shouldn't be exclusive to the 1%. The burden not living paycheck to paycheck and the vicious cycle of debt is one of the greatest economic inequality sins of our age, as our middle class shrinks and our extremeties grow. Via coding this hack, I hope the user can understand and grow his/herself and improve the quality of their life and others.

TL;DR? Not seemingly quite as noble as my original endeavor.I could write this in 24 hours, with no teammates, in contrast to my original idea, which I will still complete in near future.

Binance is a cryptoassets exchange based out of Asia. I chose Binance due to my familiarity, they are one of the more well-priced exchanges, and they need a reliable API as well. They also have many contests available for the community. 
Submitting to be considered for best financial hack (see finhack.py), blockchain use.
facebook api use (facebook notification) and zoho api use(alert system for price movement) on next update(s).


### Required 3rd party modules
- pprint
- requests
- asyncio
- websockets

All * are not to be included in actual command, e.g. pip install pprint

# Getting Started
### From cmd line, run

```
pip install *3rd party module listed above*
```

### Run setup.py file:
Clone repository
from CMD line:
```
python *directory of clone*/setup.py
```



## Your first .py file
### In your own created .py file, write:

```python
from binanceapi import api

api_key="put your api key here"
api_secret="put your api secret here"
nameofinstance = Binance("XXXXXX", api_key, api_secret)
```
I recommend writing script to pull API credientials from an external file, to prevent possible loss of control/theft.

## Run Example
```
python *directory*/example.py
```

# ENUM Definitions
## For the types of ENUM in the api file, only the following values are allowed. Put in string format.

### Symbol type:						
- XXXBTC or XXXETH, where XXX is currency, e.g. LINK or XVG

### Order status:
- NEW
- PARTIALLY_FILLED
- FILLED
- CANCELED
- PENDING_CANCEL
- REJECTED
- EXPIRED


### Order side:
- BUY
- SELL

### Time in force:
(GTC = Good Til Cancelled, IOC = Immediately or cancel)
- GTC
- IOC

### Kline intervals:
m: minutes; h: hours; d:  days; w: weeks; M: months
- 1m
- 3m
- 5m
- 15m
- 30m
- 1h
- 2h
- 4h
- 6h
- 8h
- 12h
- 1d
- 3d
- 1w
- 1M	




For more information on Binance and Binance's API, visit 
www.binance.com


