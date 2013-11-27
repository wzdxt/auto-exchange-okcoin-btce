#!/d/python27/python
# -*- coding: utf8 -*-

import httplib
import json
import hashlib
import hmac
import urllib



class BTCEApi():
	nonce = 0
	BTC_USD = 'btc_usd'
	LTC_USD = 'ltc_usd'
	LTC_BTC = 'ltc_btc'
	def __init__(self, key, secret):
		self.public_api = '/api/2'
		self.key = key
		self.secret = secret
	
	def _get_nonce(self):
		BTCEApi.nonce = BTCEApi.nonce + 1
		return BTCEApi.nonce
	
	def _send_public_request(self, pair, item):
		conn = httplib.HTTPSConnection('btc-e.com')
		conn.request('POST', '%s/%s/%s' % (self.public_api, pair, item))
		response = conn.getresponse()
		if response.status == 200:
			resp_dict = json.loads(response.read())
			if 'success' in resp_dict and resp_dict['success'] == 0:
				print 'error, response success = 0'
			else:
				return resp_dict
		else:
			print 'status:', response.status
			print 'reason:', response.reason

	def get_fee(self, pair):
		return self._send_public_request(pair, 'fee')

	def get_depth(self, pair):
		return self._send_public_request(pair, 'depth')

	def _get_hashed_params(self, params):
		return hmac.new(self.secret, params, hashlib.sha512).hexdigest()
	
	def get_info(self):
		params = {}
		params['method'] = 'getInfo'
		nonce = self._get_nonce()
		params['nonce'] = nonce
		params = urllib.urlencode(params)

		sign = self._get_hashed_params(params)
		headers = {'Sign' : sign, 'Key' : self.key, 'Content-type' : 'application/x-www-form-urlencoded'}
#		, 'User-Agent': 'Mozilla/4.0 (Windows; U; Windows NT 5.0; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}

		conn = httplib.HTTPSConnection('btc-e.com')
		conn.request('POST', '/tapi', params, headers)
		response = conn.getresponse()

		return response
