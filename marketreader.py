#!/d/python27/python
# -*- coding: utf8 -*-

from btceapi import BTCEApi
import threading

class MarketReader():
	def __init__(self, key, secret):
		self.key = key
		self.secret = secret
		self.pairs = (
		{'pair_key':'bu', 'pair':BTCEApi.BTC_USD},
		{'pair_key':'be', 'pair':BTCEApi.BTC_EUR},
		{'pair_key':'lb', 'pair':BTCEApi.LTC_BTC},
		{'pair_key':'lu', 'pair':BTCEApi.LTC_USD},
		{'pair_key':'le', 'pair':BTCEApi.LTC_EUR},
		{'pair_key':'eu', 'pair':BTCEApi.EUR_USD},)
	
	def get_all_market(self):
		market = {}

		apis = []
		for i in range(0, len(self.pairs)):
			apis.append(BTCEApi(self.key, self.secret))
		read_threads = []

		for i in range(0, len(self.pairs)):
			read_threads.append(threading.Thread(target=self.__get_market, args=(apis[i], market, self.pairs[i]['pair'], self.pairs[i]['pair_key'])))
		for thread in read_threads:
			thread.start()
		for thread in read_threads:
			thread.join()

		for pair in self.pairs:
			if not pair['pair_key'] in market:
				return None
		return market

	def __get_market(self, api, market, pair, pair_key):
		depth = api.get_depth(pair)
		market[pair_key] = depth
