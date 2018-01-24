# python-binance-api
BACKGROUND:


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


