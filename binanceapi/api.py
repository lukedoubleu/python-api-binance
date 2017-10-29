# -*- coding: utf-8 -*-
'''
Created on Sun Oct 29 08:38:01 2017

@author: lukedoulbeu
'''

import hmac
import hashlib
import time
import urllib.parse as up
import json
import pprint as p
import requests as r
import asyncio
import websockets as ws

		
# Main Class to interact with Binance API, to include ability to buy and sell assets
# 'Responses' listed after instance methods refer to the output of the respectively 
# used _public_qry, _signed_qry, or _userstream_qry
# For 'timestamp', use time.time(). Binance API requires milliseconds - functions listed here
# convert time.time() from seconds into milliseconds
		
class Binance:
	
	def __init__(self, symbol, api_key, api_secret):
		self.symbol = symbol
		self.__api_key = api_key
		self.__api_secret = api_secret.encode('utf-8')
		self.api_url_public = 'https://www.binance.com/api/v1/'
		self.api_url_withdrl = 'https://www.binance.com/wapi/v1/'
		self.api_url_acct = 'https://www.binance.com/api/v3/'
		self.api_wss = 'wss://stream.binance.com:9443/ws/'		
	

	# Generic Methods to make HTTP Request. Value returned is JSON instance of data, not displayed
	# _signed_qry is for SIGNED requests, _userstream_qry only uses API key
	def _public_qry(self, request_params, action):
		try:
				return (r.get(self.api_url_public + action,params=request_params)).json()
		except KeyboardInterrupt:
				print("Operation cancelled via 'Ctrl-C'")
		except (TypeError, AttributeError):
				print("Invalid input used, check parameter input")		
		
		
	def _signed_qry(self, params, action):
		try:
			request_params = {}
			for k,v in params.items():
				if v is not None:
					request_params.setdefault(k,v)
			request_body = up.urlencode(request_params).encode('utf-8')
			signature = hmac.new(self.__api_secret, msg=request_body, 
										digestmod=hashlib.sha256).hexdigest()
			headers = {'X-MBX-APIKEY': self.__api_key,
					   'Content-type': 'application/x-www-form-urlencoded'}		
			request_params['signature'] = signature
			if action == ('order' or 'order/test') :
				return r.post(self.api_url_acct + action, data=request_params, headers=headers).json()
			elif action == 'cancel' :
				return r.delete(self.api_url_acct + action, data=request_params, headers=headers).json()
			else:
				return r.get(self.api_url_acct + action, params=request_params, headers=headers).json()
		except KeyboardInterrupt:
			print("Operation cancelled via 'Ctrl-C'")
		except (TypeError, AttributeError):
			print("Invalid input used, check parameter input")
			
	def _withdraw_qry(self, params, action):
		try:
			request_params = {}
			for k,v in params.items():
				if v is not None:
					request_params.setdefault(k,v)
			request_body = up.urlencode(request_params).encode('utf-8')
			signature = hmac.new(self.__api_secret, msg=request_body, 
										digestmod=hashlib.sha256).hexdigest()
			headers = {'X-MBX-APIKEY': self.__api_key,
					   'Content-type': 'application/x-www-form-urlencoded'}		
			request_params['signature'] = signature
			return r.post(self.api_url_withdrl + action, data=request_params, headers=headers).json()
		except KeyboardInterrupt:
			print("Operation cancelled via 'Ctrl-C'")
		except (TypeError, AttributeError):
			print("Invalid input used, check parameter input")
			
	def _userstream_qry(self, request_params, action, _type):
		headers = {'X-MBX-APIKEY': self.__api_key,
			       'Content-type': 'application/x-www-form-urlencoded'}	
		try:
			if _type == 'startstream':
				return r.post(self.api_url_public + action, data=request_params, headers=headers).json()
			elif _type == 'keepstream':
				return r.put(self.api_url_public + action, data=request_params, headers=headers).json()
			elif _type == 'closestream':
				return r.delete(self.api_url_public + action, data=request_params, headers=headers).json()
			else:
				print ('Invalid stream type')
				return None
		except KeyboardInterrupt:
			print("Operation cancelled via 'Ctrl-C'")
		except (TypeError, AttributeError):
			print("Invalid input used, check parameter input")
	
	
	
#########################
## Public API Enpoints ##
#########################
# ENUM Definitions and requirements at bottom of this page



	# Test connectivity to Binance API server
	def test_connectivity(self):
		if (r.get(self.api_url_public+'ping')) is not None:
			return print('Ping successful')
		else:
			return print('Ping failed')

			
	# Returns server time in Unix epoch format
	def server_time(self):
		params = None
		return self._public_qry(params,'time')
	# Response: { 'serverTime': 1499827319559 }
	
	
	# Returns order book 
	def get_order_book(self, limit=100):
		params = {'symbol':self.symbol,
				  'limit': limit}
		return self._public_qry(params,'depth')
	# Response: {
		  # 'lastUpdateId': 1027024,
		  # 'bids': [
		    # [
		      # '4.00000000',     // PRICE
		      # '431.00000000',   // QTY
		      # []                // Can be ignored
		    # ]
		  # ],
		  # 'asks': [
		    # [
		      # '4.00000200',
		      # '12.00000000',
		      # []
		    # ]
		  # ]}
	
	
	# Get compressed, aggregate trades. Trades that fill at the time, from the same order, with the same price will have the quantity aggregated.
	# Parameters:
	# Name       Type    Mandatory  Description
	# symbol     STRING  YES	
	# fromId     LONG    NO	        ID to get aggregate trades from INCLUSIVE.
	# startTime  LONG    NO	        Timestamp in ms to get aggregate trades from INCLUSIVE.
	# endTime    LONG    NO	        Timestamp in ms to get aggregate trades until INCLUSIVE.
	# limit      INT     NO	        Default 500; max 500.
	# If both startTime and endTime are sent, limit should not be sent AND the distance between startTime and endTime must be less than 24 hours.
	# If frondId, startTime, and endTime are not sent, the most recent aggregate trades will be returned.
	def get_aggregate_trades(self, fromId=None, startTime=None, endTime=None, limit=500):
		params = {'symbol':self.symbol,
				  'fromId': fromId,
				  'startTime':startTime,
				  'endTime':endTime,
				  'limit':limit}
		return self._public_qry(params,'aggTrades')
	# Response: [{
		     # 'a': 26129,         // Aggregate tradeId
		     # 'p': '0.01633102',  // Price
		     # 'q': '4.70443515',  // Quantity
		     # 'f': 27781,         // First tradeId
		     # 'l': 27781,         // Last tradeId
		     # 'T': 1498793709153, // Timestamp
		     # 'm': true,          // Was the buyer the maker?
		     # 'M': true           // Was the trade the best price match?
		   # }]
	
	
	# Kline/candlestick bars for a symbol. Klines are uniquely identified by their open time.
	# Parameters:
	# Name       Type     Mandatory  Description
	# symbol	 STRING   YES	
	# interval   ENUM	  YES	
	# limit      INT	  NO	      Default 500; max 500.
	# startTime  LONG	  NO	
	# endTime	 LONG	  NO		
	# If startTime and endTime are not sent, the most recent klines are returned.
	def kline_candlesticks(self, interval=None, limit=None, startTime=None, endTime=100):
		params = {'symbol':self.symbol,
				  'interval': interval,
				  'limit':limit,
				  'startTime':startTime,
				  'endTime':endTime}
		return self._public_qry(params,'klines')
	# Response: [
		  # [
		    # 1499040000000,      // Open time
		    # '0.01634790',       // Open
		    # '0.80000000',       // High
		    # '0.01575800',       // Low
		    # '0.01577100',       // Close
		    # '148976.11427815',  // Volume
		    # 1499644799999,      // Close time
		    # '2434.19055334',    // Quote asset volume
		    # 308,                // Number of trades
		    # '1756.87402397',    // Taker buy base asset volume
		    # '28.46694368',      // Taker buy quote asset volume
		    # '17928899.62484339' // Can be ignored
		  # ] ]	
	

	# 24 hr ticker price change statistics
	# Parameters:
	# Name     Type     Mandatory
	# symbol   String   Yes
	def price_change_24hours(self):
		params = {'symbol':self.symbol}
		return self._public_qry(params,'ticker/24hr')
	# Response: {
		  # 'priceChange': '-94.99999800',
		  # 'priceChangePercent': '-95.960',
		  # 'weightedAvgPrice': '0.29628482',
		  # 'prevClosePrice': '0.10002000',
		  # 'lastPrice': '4.00000200',
		  # 'bidPrice': '4.00000000',
		  # 'askPrice': '4.00000200',
		  # 'openPrice': '99.00000000',
		  # 'highPrice': '100.00000000',
		  # 'lowPrice': '0.10000000',
		  # 'volume': '8913.30000000',
		  # 'openTime': 1499783499040,
		  # 'closeTime': 1499869899040,
		  # 'firstId': 28385,   // First tradeId
		  # 'lastId': 28460,    // Last tradeId
		  # 'count': 76         // Trade count
		# }	
		
	
	# Lists all price tickers
	# Parameters: None
	def symbol_price_ticker(self):
		params = None
		return self._public_qry(params,'ticker/allPrices')	
	# Response:[ {
				    # 'symbol': 'LTCBTC',
				    # 'price': '4.00000200'
				  # },
				  # {
				    # 'symbol': 'ETHBTC',
				    # 'price': '0.07946600'
				  # } ]	
	
	
	# Symbols order book ticker
	# Best price/qty on the order book for all symbols
	# Parameters: None
	def order_book_ticker(self):
		params = None
		return self._public_qry(params,'ticker/allBookTickers')
	# Response: [{
				    # 'symbol': 'LTCBTC',
				    # 'bidPrice': '4.00000000',
				    # 'bidQty': '431.00000000',
				    # 'askPrice': '4.00000200',
				    # 'askQty': '9.00000000'
				  # },
				  # {
				    # 'symbol': 'ETHBTC',
				    # 'bidPrice': '0.07946700',
				    # 'bidQty': '9.00000000',
				    # 'askPrice': '100000.00000000',
				    # 'askQty': '1000.00000000'
				  # } ]


				  
#################################################################
## Account-specific Endpoints. Requires API Key and API Secret ##
## user_data_stream method only requires API KEY               ##
#################################################################

	# Send in a new order (POST)
	# Parameters:
	# Name	            Type	 Mandatory	Description
	# symbol	        STRING	 YES	
	# side	            ENUM	 YES	
	# type	            ENUM	 YES	
	# timeInForce	    ENUM	 YES	
	# quantity	        DECIMAL  YES	
	# price	            DECIMAL  YES	
	# newClientOrderId	STRING	 NO	         A unique id for the order. Automatically generated if not sent.
	# stopPrice	        DECIMAL	 NO	         Used with stop orders
	# icebergQty	    DECIMAL	 NO	         Used with iceberg orders
	# timestamp	        LONG	 YES	
	def new_order(self, side=None, otype=None, timeInForce=None,
				  quantity=None, price=None, newClientOrderId=None, stopPrice=None,
				  icebergQty=None, timestamp=time.time()):
		params = {'symbol':self.symbol,
				  'side':side,
				  'type':otype,
				  'timeInForce':timeinForce,
				  'quantity':quantity,
				  'price':price,
				  'newClientOrderId':newClientOrderId,
				  'stopPrice':stopPrice,
				  'icebergQty':icebergQty, 
				  'timestamp':int(timestamp)*1000}
		return self._signed_qry(params, 'order')
	# Response: {
	  # 'symbol':'LTCBTC',
	  # 'orderId': 1,
	  # 'clientOrderId': 'myOrder1' // Will be newClientOrderId
	  # 'transactTime': 1499827319559
	# }
		
		
	# Test new order creation and signature/recvWindow long. 
	# Creates and validates a new order but does not send it into the matching engine. (POST)
	# Parameters:
	# Name	            Type	 Mandatory	Description
	# symbol	        STRING	 YES	
	# side	            ENUM	 YES	
	# type	            ENUM	 YES	
	# timeInForce	    ENUM	 YES	
	# quantity	        DECIMAL  YES	
	# price	            DECIMAL  YES	
	# newClientOrderId	STRING	 NO	         A unique id for the order. Automatically generated if not sent.
	# stopPrice	        DECIMAL	 NO	         Used with stop orders
	# icebergQty	    DECIMAL	 NO	         Used with iceberg orders
	# timestamp	        LONG	 YES			
	def test_new_order(self, side=None, otype=None, timeInForce=None,
					   quantity=None, price=None, newClientOrderId=None, stopPrice=None,
				       icebergQty=None, timestamp=time.time()):
		params = {'symbol':self.symbol,
				  'side':side,
				  'type':otype,
				  'timeInForce':timeInForce,
				  'quantity':quantity,
				  'price':price,
				  'newClientOrderId':newClientOrderId,
				  'stopPrice':stopPrice,
				  'icebergQty':icebergQty, 
				  'timestamp':int(timestamp)*1000}
		return self._signed_qry(params, 'order/test')
	# Response: {}
	
	
	# Check an order's status. (GET)
	# Parameters:
	# Name	            Type	Mandatory	Description
	# symbol	        STRING	YES	
	# orderId	        LONG	NO	
	# origClientOrderId	STRING	NO	
	# recvWindow	    LONG	NO	
	# timestamp	        LONG	YES	
	# Either orderId or origClientOrderId must be sent.		
	def query_order(self, orderId=None, origClientOrderId=None, recvWindow=None,
					timestamp=time.time()):
		params = {'symbol':self.symbol,
				  'orderId':orderId,
				  'origClientOrderId':origClientOrderId,
				  'recvWindow':recvWindow,
				  'timestamp':int(timestamp)*1000}
		return self._signed_qry(params, 'order')
	# Response: {
			  # 'symbol': 'LTCBTC',
			  # 'orderId': 1,
			  # 'clientOrderId': 'myOrder1',
			  # 'price': '0.1',
			  # 'origQty': '1.0',
			  # 'executedQty': '0.0',
			  # 'status': 'NEW',
			  # 'timeInForce': 'GTC',
			  # 'type': 'LIMIT',
			  # 'side': 'BUY',
			  # 'stopPrice': '0.0',
			  # 'icebergQty': '0.0',
			  # 'time': 1499827319559
			# }		
			
				
	# Cancel an active order. (DELETE)
	# Parameters:
	# Name	            Type	Mandatory  Description
	# symbol	        STRING	YES	
	# orderId	        LONG	NO	
	# origClientOrderId	STRING	NO	
	# newClientOrderId	STRING	NO	       Used to uniquely identify this cancel. Automatically generated by default.
	# recvWindow	    LONG	NO	
	# timestamp	        LONG	YES			
	def cancel_order(self, orderId=None, origClientOrderId=None, newClientOrderId=None, recvWindow=None,
					 timestamp=time.time()):
		params = {'symbol':self.symbol,
				  'orderId':orderId,
				  'origClientOrderId':origClientOrderId,
				  'newClientOrderId':newClientOrderId,
				  'recvWindow':recvWindow,
				  'timestamp':int(timestamp)*1000}
		return self._signed_qry(params, 'order')
	# Response: {
		  # 'symbol': 'LTCBTC',
		  # 'origClientOrderId': 'myOrder1',
		  # 'orderId': 1,
		  # 'clientOrderId': 'cancelMyOrder1'
		# }
			
			
	# Get all open orders on a symbol. (GET)
	# Parameters:
	# Name	     Type	Mandatory	Description
	# symbol	 STRING	YES	
	# recvWindow LONG	NO	
	# timestamp	 LONG   YES
	def current_open_orders(self, recvWindow=None, timestamp=time.time()):
		params = {'symbol':self.symbol,
				  'recvWindow':recvWindow,
				  'timestamp':int(timestamp)*1000}
		return self._signed_qry(params, 'openOrders')
	# Response:[ {
		# 'symbol': 'LTCBTC',
		# 'orderId': 1,
		# 'clientOrderId': 'myOrder1',
		# 'price': '0.1',
		# 'origQty': '1.0',
		# 'executedQty': '0.0',
		# 'status': 'NEW',
		# 'timeInForce': 'GTC',
		# 'type': 'LIMIT',
		# 'side': 'BUY',
		# 'stopPrice': '0.0',
		# 'icebergQty': '0.0',
		# 'time': 1499827319559
	  # } ]
	  
			  
	# Get all account orders; active, canceled, or filled. (GET)
	# Parameters:
	# Name	     Type	Mandatory  Description
	# symbol	 STRING	YES	
	# orderId	 LONG	NO	
	# limit	     INT	NO	       Default 500; max 500.
	# recvWindow LONG	NO	
	# timestamp	 LONG	YES	
	# If orderId is set, it will get orders >= that orderId. Otherwise most recent orders are returned.	
	def all_orders(self, orderId=None, limit=None, recvWindow=None, timestamp=time.time()):
		params = {'symbol':self.symbol,
				  'orderId':orderId,
				  'limit':limit,
				  'recvWindow':recvWindow,
				  'timestamp':int(timestamp)*1000}
		return self._signed_qry(params, 'allOrders')
	# Response:[ {
				# 'symbol': 'LTCBTC',
				# 'orderId': 1,
				# 'clientOrderId': 'myOrder1',
				# 'price': '0.1',
				# 'origQty': '1.0',
				# 'executedQty': '0.0',
				# 'status': 'NEW',
				# 'timeInForce': 'GTC',
				# 'type': 'LIMIT',
				# 'side': 'BUY',
				# 'stopPrice': '0.0',
				# 'icebergQty': '0.0',
				# 'time': 1499827319559
			  # } ]	
			  
			  
	# Get current account information. (GET)
	# Parameters:
	# Name	     Type	Mandatory	Description
	# recvWindow LONG	NO	
	# timestamp  LONG   YES
	def account_info(self, recvWindow=None, timestamp=time.time()):
		params = {'recvWindow':recvWindow,
				  'timestamp':int(timestamp)*1000}
		return self._signed_qry(params, 'account')
	# Response:{
		  # 'makerCommission': 15,
		  # 'takerCommission': 15,
		  # 'buyerCommission': 0,
		  # 'sellerCommission': 0,
		  # 'canTrade': true,
		  # 'canWithdraw': true,
		  # 'canDeposit': true,
		  # 'balances': [
		    # {
		      # 'asset': 'BTC',
		      # 'free': '4723846.89208129',
		      # 'locked': '0.00000000'
		    # },
		    # {
		      # 'asset': 'LTC',
		      # 'free': '4763368.68006011',
		      # 'locked': '0.00000000'
		    # }
		  # ] }
	
		
	# Get trades for a specific account and symbol. (GET)
	# Parameters:
	# Name	     Type	Mandatory	Description
	# symbol	 STRING	YES	
	# limit	     INT	NO	        Default 500; max 500.
	# fromId	 LONG	NO	       TradeId to fetch from. Default gets most recent trades.
	# recvWindow LONG	NO	
	# timestamp	 LONG	YES		
	def account_tradelist(self, limit=None, fromId=None, recvWindow=None, timestamp=time.time()):
		params = {'symbol':self.symbol,
				  'limit':limit,
				  'fromId':fromId,
				  'recvWindow':recvWindow,
				  'timestamp':int(timestamp)*1000}
		return self._signed_qry(params, 'myTrades')
	# Response:[ {
		# 'id': 28457,
		# 'price': '4.00000100',
		# 'qty': '12.00000000',
		# 'commission': '10.10000000',
		# 'commissionAsset': 'BNB',
		# 'time': 1499865549590,
		# 'isBuyer': true,
		# 'isMaker': false,
		# 'isBestMatch': true
	  # } ]
	  

	# Submit a withdraw request. (POST)
	# Parameters:
	# Name		 Type	 Mandatory	 Description
	# asset		 STRING	 YES	
	# address	 STRING	 YES	
	# amount	 LONG	 YES	
	# name		 STRING	 NO	          Description of the address
	# recvWindow LONG	 NO	
	# timestamp	 LONG	 YES		  
	def withdrawal(self, address=None, amount=None, name=None, recvWindow=None, timestamp=time.time()):
		params = {'asset':self.symbol,
				  'address':address,
				  'amount':amount,
				  'name':name,
				  'recvWindow':recvWindow,
				  'timestamp':int(timestamp)*1000}
		return self._withdraw_qry(params, 'withdraw')
				
				
	# Fetch deposit history. (POST)
	# Parameters:
	# Name		 Type	 Mandatory	 Description
	# asset		 STRING	 YES	
	# status	 INT	 NO	  		 0(0:pending,1:success)
	# startTime	 LONG	 NO	
	# endTime	 LONG	 NO	
	# recvWindow LONG	 NO	
	# timestamp	 LONG	 YES					
	def get_deposit_history(self, status=None, address=None, startTime=None, endTime=None, recvWindow=None, timestamp=time.time()):
		params = {'asset':self.symbol,
				  'status':status,
				  'address':address,
				  'startTime':startTime,
				  'endTime':endTime,
				  'recvWindow':recvWindow,
				  'timestamp':int(timestamp)*1000}
		return self._withdraw_qry(params, 'getDepositHistory')
				
	# Fetch withdraw history. (POST)
	# Parameters:
	# Name		 Type	 Mandatory	 Description
	# asset		 STRING	 YES
	# status	 INT	 NO	  		 0(0:Email Sent,1:Cancelled 2:Awaiting Approval 3:Rejected 4:Processing 5:Failure 6:Completed)
	# startTime	 LONG	 NO	
	# endTime	 LONG	 NO	
	# recvWindow LONG	 NO	
	# timestamp	 LONG	 YES					
	def get_withdraw_history(self, status= None, address=None, startTime=None, endTime=None, recvWindow=None, timestamp=time.time()):
		params = {'asset':self.symbol,
				  'status': status,
				  'address':address,
				  'startTime':startTime,
				  'endTime':endTime,
				  'recvWindow':recvWindow,
				  'timestamp':int(timestamp)*1000}
		return self._withdraw_qry(params, 'getWithdrawHistory')
				
 
	  
	  
	  
	  
		
	# Get user stream data. Requires API Key
	# 3 types of data streams, must specify with 'type' parameter. Default type='startstream'
	# Start user data stream starts stream, Keep alive user data stream pings to prevent time out,
	# Close user data stream closes out stream. 
	# Action denoted by type of HTTP request: POST, PUT, or DELETE
	# Parameters
	# Start user data stream (POST)
	# Name       Type      Mandatory   Description
	# type	     STRING	   Yes         Default setting, type='startstream'
	#
	# Keep alive user data stream (PUT)
	# listenKey  STRING    YES
	# type 		 STRING    NO		   type='keepstream'
	#
	# Close User Data Stream (DELETE)
	# listenKey  STRING    YES
	# type 		 STRING    NO		   type='closestream'	
	def user_data_stream(self, listenKey=None, type='startstream'):
		params = {'listenKey':listenKey}
		return self._userstream_qry(params, 'userDataStream', type)
		

	
########################
## Websocket Endpoint ##
########################	


	# Depth Websocket Endpoint
	async def ws_depth(self):
	#wss://stream.binance.com:9443/ws/[symbol in lowercase]@depth
		symbol_lower = self.symbol.lower()
		uri = 'wss://stream.binance.com:9443/ws/{}@depth'.format(symbol_lower)
		async with ws.client.connect(uri) as opensocket:
			while(True):
				result = await opensocket.recv()
				result = json.loads(result)
				p.pprint(result)
				print("\n")
	# Event Data: {
				# "e": "depthUpdate",						// event type
				# "E": 1499404630606, 					// event time
				# "s": "ETHBTC", 							// symbol
				# "u": 7913455, 							// updateId to sync up with updateid in /api/v1/depth
				# "b": [									// bid depth delta
					# [
						# "0.10376590", 					// price (need to upate the quantity on this price)
						# "59.15767010", 					// quantity
						# []								// can be ignored
					# ],
				# ],
				# "a": [									// ask depth delta
					# [
						# "0.10376586", 					// price (need to upate the quantity on this price)
						# "159.15767010", 				// quantity
						# []								// can be ignored
					# ],
					# [
						# "0.10383109",
						# "345.86845230",
						# []
					# ],
					# [
						# "0.10490700",
						# "0.00000000", 					//quantitiy=0 means remove this level
						# []
					# ]
				# ]
			# }			
		
		
	# Kline Websocket Endpoint	
	async def ws_kline(self, kline_i='5m'):
		#wss://stream.binance.com:9443/ws/[symbol in lowercase]@kline
		symbol_lower = self.symbol.lower()
		uri = 'wss://stream.binance.com:9443/ws/{}@kline_{}'.format(symbol_lower, kline_i)
		async with ws.client.connect(uri) as opensocket:
			while(True):
				result = await opensocket.recv()
				result = json.loads(result)
				p.pprint(result)
				print("\n")
	# Event Data: {
				# "e": "kline",				// event type
				# "E": 1499404907056,			// event time
				# "s": "ETHBTC",			// symbol
				# "k": {
					# "t": 1499404860000, 		// start time of this bar
					# "T": 1499404919999, 		// end time of this bar
					# "s": "ETHBTC",		// symbol
					# "i": "1m",			// interval
					# "f": 77462,			// first trade id
					# "L": 77465,			// last trade id
					# "o": "0.10278577",		// open
					# "c": "0.10278645",		// close
					# "h": "0.10278712",		// high
					# "l": "0.10278518",		// low
					# "v": "17.47929838",		// volume
					# "n": 4,			// number of trades
					# "x": false,			// whether this bar is final
					# "q": "1.79662878",		// quote volume
					# "V": "2.34879839",		// volume of active buy
					# "Q": "0.24142166",		// quote volume of active buy
					# "B": "13279784.01349473"	// can be ignored
					# }
			# }		
		
		
	# Trades Websocket Endpoint	
	async def ws_trades(self):
		#wss://stream.binance.com:9443/ws/[symbol in lowercase]@aggTrade
		symbol_lower = self.symbol.lower()
		uri = 'wss://stream.binance.com:9443/ws/{}@aggTrade'.format(symbol_lower)
		async with ws.client.connect(uri) as opensocket:
			while(True):
				result = await opensocket.recv()
				result = json.loads(result)
				p.pprint(result)
				print("\n")
	# Event Data: {
				# "e": "aggTrade",		// event type
				# "E": 1499405254326,		// event time
				# "s": "ETHBTC",			// symbol
				# "a": 70232,				// aggregated tradeid
				# "p": "0.10281118",		// price
				# "q": "8.15632997",		// quantity
				# "f": 77489,				// first breakdown trade id
				# "l": 77489,				// last breakdown trade id
				# "T": 1499405254324,		// trade time
				# "m": false,				// whehter buyer is a maker
				# "M": true				// can be ignore
			# }
					
		
	# User Data Websocket Endpoint	
	async def ws_userdata(self, listenKey=None):
		#wss://stream.binance.com:9443/ws/[listenKey]
		symbol_lower = self.symbol.lower()
		uri = 'wss://stream.binance.com:9443/ws/{}'.format(listenKey)
		async with ws.client.connect(uri) as opensocket:
			while(True):
				result = await opensocket.recv()
				result = json.loads(result)
				p.pprint(result)
				print("\n")
		
	def ws_shell(self, func):
		return asyncio.get_event_loop().run_until_complete(func)


	
