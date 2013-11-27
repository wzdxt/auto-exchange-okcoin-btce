#!/d/python27/python
# -*- coding: utf8 -*-

from btceapi import BTCEApi
import thread

class Detector():
	def __init__(self, key, secret):
		self.key = key
		self.secret = secret
		
	def find_best_route(self):
		print get_all_rate()


	def get_all_rate(self):
		rate={'buy':{'bu' : -1, 'br' : -1, 'be' : -1, 'lb' : -1, 'lu' : -1, 'lr' : -1, 'le' : -1, 'ur' : -1, 'eu' : -1}, 'sell':{'bu' : -1, 'br' : -1, 'be' : -1, 'lb' : -1, 'lu' : -1, 'lr' : -1, 'le' : -1, 'ur' : -1, 'eu' : -1}}
		apis = []
		for i in range(0, 9):
			apis.append(BTCEApi(self.key, self.secret))

		a=thread.start_new_thread(self.__get_rate, (apis[0], rate, BTCEApi.BTC_USD, 'bu'))
		a.join(1)

		return rate

	def __get_rate(self, api, rate, pair, pair_key):
		depth = api.get_depth(pair)
		rate['buy'][pair_key] = depth['asks'][0][0]
		rate['sell'][pair_key] = depth['bids'][0][0]
