#!/d/python27/python
# -*- coding: utf8 -*-

from __future__ import division

from btceapi import BTCEApi
from marketreader import MarketReader
import threading
import copy
import time

AMOUNT_C = 0

class Detector():
	min_coin = {'usd':3, 'eur':3, 'btc':0.01, 'ltc':0.1}
	def find_best_route(self, market, coins={}):
		rate = self.__get_all_rate(market)
		if __debug__:
			print rate

		coin_best = {}
		max_benefit = [0, []]
		best = ''
		for coin in coins:
			if coins[coin] < self.min_coin[coin]:
				continue
			coin_best[coin] = self.find_best_route_ignore_amount(rate, coin)
			if len(coin_best[coin][1]) > 3 and coin_best[coin][0] > max_benefit[0]:
				max_benefit = coin_best[coin]
				best = coin
			if __debug__:
				print '* best for %s: %s' % (coin, coin_best[coin][1])
				print '* best for %s: %s' % (coin, coin_best[coin][0])
		if __debug__:
			print '** best route:', max_benefit[1]
			print '** best route:', max_benefit[0]

		for coin in coins:
			if coin == best:
				if self.__get_best_route_benefit(market, coin_best[coin][1], coins[coin]) > 1:
					return (coin, coin_best[coin])
		return None
	
	def find_best_route_ignore_amount(self, rate, name):
		max_benefit = {'btc':0, 'ltc':0, 'usd':0, 'eur':0}
		max_benefit[name] = 1
		(best_benefit, route) = RouteUtil(rate).find_best_coin_route(name, name, [name],  max_benefit)
		return (best_benefit, route)

	def __get_best_route_benefit(self, market, route, amount):
		rate = 1
		for i in range(0, len(route)-1):
			if route[i][0] + route[i+1][0] in market:
				pair_key = route[i][0] + route[i+1][0]
				next_rate = self.get_rate_consider_amount(market[pair_key]['bids'], amount, 'sell')
				rate = rate * next_rate * 0.998
				amount = amount * next_rate * 0.998
			else:
				pair_key = route[i+1][0] + route[i][0]
				next_rate = 1/self.get_rate_consider_amount(market[pair_key]['asks'], amount, 'buy')
				rate = rate * next_rate * 0.998
				amount = amount * next_rate * 0.998
		return rate

	def get_rate_consider_amount(self, depth, amount, type):
		total = 0
		for d in depth:
			if type == 'sell':
				total = total + d[1]
			else:
				total = total + d[0] * d[1]
			if total >= amount * AMOUNT_C:
				return d[0]
		print type
		print amount
		print depth

	def __get_all_rate(self, market):
		rate={'buy':{'bu' : -1, 'be' : -1, 'lb' : -1, 'lu' : -1, 'le' : -1, 'eu' : -1}, 'sell':{'bu' : -1, 'be' : -1, 'lb' : -1, 'lu' : -1, 'le' : -1, 'eu' : -1}}

		for pair_key in market:
			rate['buy'][pair_key] = market[pair_key]['asks'][0][0]
			rate['sell'][pair_key] = market[pair_key]['bids'][0][0]

		return rate

class RouteUtil():
	def __init__(self, rate):
		self.rate = rate

	def find_best_coin_route(self, start_coin, now_coin, route, max_benefit):
		if __debug__:
			print 'come to coin:', now_coin
			print 'route:', route
		if start_coin == now_coin and len(route) > 2:
			if __debug__:
				print 'go back'
			return (max_benefit[start_coin], route)
		if len(route) > 5:
			if __debug__:
				print 'go back'
			return (-1, route)
		ret = -1
		rate = -1
		best_next_coin = (-1, [])
		for next_coin in ('btc', 'ltc', 'usd', 'eur'):
			if __debug__:
				print 'try: %s -> %s' % (now_coin,  next_coin)
			if now_coin == next_coin:
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
				elif next_coin == 'ltc':
					rate = 1/self.rate['buy']['le']
				elif next_coin == 'usd':
					rate = self.rate['sell']['eu']
				else:
					raise Exception('unknow coin name: ' + next_coin)
			else:
				raise Exception('unknow coin name: ' + now_coin)

			(benefit, res_route) = self.try_next(start_coin, now_coin, next_coin, rate*0.998, route, max_benefit)
			if benefit > best_next_coin[0]:
				best_next_coin = (benefit, res_route)
		if __debug__:
			print 'go back'
		return best_next_coin

	def try_next(self, start_coin, now_coin, next_coin, rate, route, max_benefit):
		new_route = copy.copy(route)
		new_route.append(next_coin)
		next_benefit = max_benefit[now_coin] * rate
		if next_benefit <= max_benefit[next_coin]:
			if __debug__:
				print 'try failed'
			return (-1, new_route)
		max_benefit[next_coin] = next_benefit
		if __debug__:
			print 'max benefit:', max_benefit
		return self.find_best_coin_route(start_coin, next_coin, new_route, max_benefit)


if __name__ == '__main__':
	import key
	d = Detector()
	res = []
	funds = {'btc':1, 'ltc':0, 'usd':0, 'eur':0}
	mr = MarketReader(key.key, key.secret)
	while True:
		t = '[%s]' % (time.strftime('%H:%M:%S', time.localtime(time.time())))
		market = mr.get_all_market()
		if market == None:
			continue
		find_res = d.find_best_route(market, funds)
		if find_res is not None:
			res.append((t, find_res))
			route = find_res[1]
			if route[0][0] + route[1][0] in market:
				pair_key = route[0][0] + route[1][0]
				rate = market[pair_key]['bids'][0][0]
			else:
				pair_key = route[1][0] + route[0][0]
				rate = 1/market[pair_key]['asks'][0][0]
			funds[route[1]] = funds[route[0]] * rate
			funds[route[0]] = 0

			print t, find_res
			print t, funds
		else:
			print t, 'no route found'
		time.sleep(10)
