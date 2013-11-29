#!/d/python27/python
# -*- coding: utf8 -*-

from __future__ import division

import time
import math

import key
from btceapi import BTCEApi
from detector import Detector
from marketreader import MarketReader

STATUS_LOOK = 1
STATUS_START_BUY = 2
STATUS_BUYING = 3

def run(key, secret):
	detector = Detector()
	market_reader = MarketReader(key, secret)
	api = BTCEApi(key, secret)

	funds = get_funds(api)

	status = STATUS_LOOK

	look_sleep_time = 2
	
	while True:
		if status == STATUS_LOOK:
			market = market_reader.get_all_market()
			if market is not None:
				step = get_next_step(funds, market)
				if step is not None:
					status = STATUS_START_BUY
			if status == STATUS_LOOK:
				print '[%s] no route found' % get_time_str()
				time.sleep(look_sleep_time)
				look_sleep_time = math.sqrt(look_sleep_time/10) * 10
			else:
				look_sleep_time = 2
		if status == STATUS_START_BUY:
			if step[0][0] + step[1][0] in market:
				pair_key = step[0][0] + step[1][0]
				type = 'sell'
				next_rate = detector.get_rate_consider_amount(market[pair_key]['bids'], funds[step[0]], type)
				amount = funds[step[0]]
			else:
				pair_key = step[1][0] + step[0][0]
				type = 'buy'
				next_rate = detector.get_rate_consider_amount(market[pair_key]['asks'], funds[step[0]], type)
				amount = funds[step[0]]/next_rate
			pair = get_pair(pair_key)

			amount = round(amount - 0.000000004, 8)
			order_id = trade(api, pair, type, next_rate, amount)
			if order_id is not None:
				status = STATUS_BUYING
			else:
				status = STATUS_LOOK
		if status == STATUS_BUYING:
			funds = cancel_order(api, order_id)
			if funds is None:
				funds = get_funds(api)
			status = STATUS_LOOK

def cancel_order(api, order_id):
	if order_id == 0:
		orders = api.get_order_list();
		if orders is not None:
			order_id = orders.keys[0]
	if order_id > 0:
		res = api.cancel_order(order_id)
	else:
		res = None
	if res is not None:
		print 'cancel order', order_id
		print '[%s] order %s is canceled' % (get_time_str(), order_id)
		funds = make_simple_funds(res['funds'])
		print '[%s] %s' % (get_time_str(), funds)
		return funds
	else:
		if order_id > 0:
			print '[%s] order %s is filled' % (get_time_str(), order_id)
		else:
			print 'order is filled'
		return None

def trade(api, pair, type, rate, amount):
	if amount < 0.001:
		print 'too smal amount:', amount
		return None
	print '[%s] %s %s in %s, amount: %s' % (get_time_str(), type, pair, rate, amount)
	res = api.trade(pair, type, rate, amount)
	if res is None:
		print '[%s] make order fail' % get_time_str()
		return None
	else:
		print '[%s] make order succeed' % get_time_str()
		return res['order_id']

def get_time_str():
	return time.strftime('%H:%M:%S', time.localtime(time.time()))

def get_next_step(funds, market):
	detector = Detector()
	find_res = detector.find_best_route(market, funds)
	if find_res is not None:
		route = find_res[1]
		print '[%s] %s' % (get_time_str(), find_res)
		return route[:2]
	else:
		return None

def get_funds(api):
	funds_tmp = api.get_info()['funds']
	while funds_tmp is None:
		funds_tmp = api.get_info()['funds']
	funds = make_simple_funds(funds_tmp)
	print '[%s] %s' % (get_time_str(), funds)
	return funds

def make_simple_funds(tmp):
	funds = {
		'usd': tmp['usd'],
		'eur': tmp['eur'],
		'btc': tmp['btc'],
		'ltc': tmp['ltc'],}
	return funds

def get_pair(pair_key):
	return {
		'bu': BTCEApi.BTC_USD,
		'be': BTCEApi.BTC_EUR,
		'lb': BTCEApi.LTC_BTC,
		'lu': BTCEApi.LTC_USD,
		'le': BTCEApi.LTC_EUR,
		'eu': BTCEApi.EUR_USD,}[pair_key]

if __name__ == '__main__':
	run(key.key, key.secret)
