#!/d/python27/python
# -*- coding: utf8 -*-

from btceapi import BTCEApi
import threading

class Detector():
	def __init__(self, key, secret):
		self.key = key
		self.secret = secret
		
	def find_best_route(self, coins={}):
		rate = self.__get_all_rate()

		coin_best = {}
		max_benefit = -1
		best = ''
		for coin in coins:
			coin_best[coin] = find_best_route_ignore_amount(rate, coin)
			if coin_best[coin][0] > max:
				max_benefit = coin_best[coin][0]
				best = coin
		if max_benefit > 1.01
		for coin in coins:
			if coin == best:
				if get_best_route_benefit(coin, coin_best[coin][1] coins[coin]) > 1.01:
					return (coin, coin_best[coin])
		return None
	
	def find_best_route_ignore_amount(rate, name):
		return (best benefit, route)

	def get_best_route_benefit(self, route, amount):
		return fact benefit


	def __get_all_rate(self):
		rate={'buy':{'bu' : -1, 'be' : -1, 'lb' : -1, 'lu' : -1, 'le' : -1, 'eu' : -1}, 'sell':{'bu' : -1, 'be' : -1, 'lb' : -1, 'lu' : -1, 'le' : -1, 'eu' : -1}}
#		rate={'buy':{'bu' : -1, 'br' : -1, 'be' : -1, 'lb' : -1, 'lu' : -1, 'lr' : -1, 'le' : -1, 'ur' : -1, 'eu' : -1}, 'sell':{'bu' : -1, 'br' : -1, 'be' : -1, 'lb' : -1, 'lu' : -1, 'lr' : -1, 'le' : -1, 'ur' : -1, 'eu' : -1}}
		apis = []
		for i in range(0, 9):
			apis.append(BTCEApi(self.key, self.secret))

		read_threads = []
		read_threads.append(threading.Thread(target=self.__get_rate, args=(apis[0], rate, BTCEApi.BTC_USD, 'bu')))
#		read_threads.append(threading.Thread(target=self.__get_rate, args=(apis[1], rate, BTCEApi.BTC_RUR, 'br')))
		read_threads.append(threading.Thread(target=self.__get_rate, args=(apis[2], rate, BTCEApi.BTC_EUR, 'be')))
		read_threads.append(threading.Thread(target=self.__get_rate, args=(apis[3], rate, BTCEApi.LTC_BTC, 'lb')))
		read_threads.append(threading.Thread(target=self.__get_rate, args=(apis[4], rate, BTCEApi.LTC_USD, 'lu')))
#		read_threads.append(threading.Thread(target=self.__get_rate, args=(apis[5], rate, BTCEApi.LTC_RUR, 'lr')))
		read_threads.append(threading.Thread(target=self.__get_rate, args=(apis[6], rate, BTCEApi.LTC_EUR, 'le')))
		read_threads.append(threading.Thread(target=self.__get_rate, args=(apis[7], rate, BTCEApi.USD_RUR, 'ur')))
#		read_threads.append(threading.Thread(target=self.__get_rate, args=(apis[8], rate, BTCEApi.EUR_USD, 'eu')))

		for thread in read_threads:
			thread.start()
		for thread in read_threads:
			thread.join()

		return rate

	def __get_rate(self, api, rate, pair, pair_key, total=0):
		depth = api.get_depth(pair)
		if total is 0:
			rate['buy'][pair_key] = depth['asks'][0][0]
			rate['sell'][pair_key] = depth['bids'][0][0]

class RouteUtil():
	def __init__(self, rate):
		self.rate = rate

	def find_best_coin_route(start_coin, now_coin, route, max_benefit, rate):
		if start_coin == now_coin and len(route) > 2:
			return max_benefit[start_coin]
		ret = -1
		rate = -1
		for next_coin in ('btc', 'ltc', 'usd', 'eur'):
			if now_coin is next_coin:
				continue
			elif now_coin == 'btc':
				if next_coin == 'usd':
					rate = self.rate['sell']['bu']
				elif next_coin == 'ltc':
					rate = 1/self.rate['buy']['lb']
				elif next_coin == 'eur':
					rate = self.rate['sell']['be']
				else:
					raise Exception('unknow coin name: ' + next_coin)
			elif now_coin == 'ltc':
				if next_coin == 'btc':
					rate = self.rate['sell']['lb']
				elif next_coin == 'usd':
					rate = self.rate['sell']['lu']
				elif next_coin == 'eur':
					rate = self.rate['sell']['le']
				else:
					raise Exception('unknow coin name: ' + next_coin)
			elif now_coin == 'usd':
				if next_coin == 'btc':
					rate = 1/self.rate['buy']['bu']
				elif next_coin == 'ltc':
					rate = 1/self.rate['buy']['lu']
				elif next_coin == 'eur':
					rate = 1/self.rate['buy']['eu']
				else:
					raise Exception('unknow coin name: ' + next_coin)
			elif now_coin == 'eur':
				if next_coin == 'btc':
					rate = 1/self.rate['buy']['be']
				if next_coin == 'ltc':
					rate = 1/self.rate['buy']['le']
				if next_coin == 'usd':
					rate = self.rate['sell']['eu']
				else:
					raise Exception('unknow coin name: ' + next_coin)
			else:
				raise Exception('unknow coin name: ' + now_coin)
		rate = rate * 0.998

		for next_coin in ('btc', 'ltc', 'usd', 'eur'):
			try next coin

if __name__ == '__main__':
	import key
	d = Detector(key.key, key.secret)
	print d.find_best_route()
