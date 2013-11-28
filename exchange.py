#!/d/python27/python
# -*- coding: utf8 -*-

from __future__ import division

import key
from btceapi import BTCEApi
from detector import Detector()

STATUS_LOOK
STATUS_START_BUY
STATUS_BUYING

def run(key, secret):
	detector = Detector()
	market_reader = MarketReader(key, secret)
	api = BTCEApi(key, secret)

	funds = get_funds()

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
				time.sleep(sleep_time)
				look_sleep_time = math.sqrt(look_sleep_time/10) * 10
		if status == STATUS_START_BUY:
			if step[0][0] + route[1][0] in market:
				pair_key = route[0][0] + route[1][0]
				type = 'sell'
				next_rate = self.get_rate_consider_amount(market[pair_key]['bids'], funds[step[0]], type)
			else:
				pair_key = route[1][0] + route[0][0]
				type = 'buy'
				next_rate = self.get_rate_consider_amount(market[pair_key]['asks'], amount, type)
			pair = get_pair(pair_key)
			# buy in (next_rate)
		if status == STATUA_BUYING:



def get_next_step(funds, market):
	detector = Detector()
	find_res = detector.find_best_route(market, funds)
	if find_res is not None:
		return find_res[1][:2]
	else:
		return None


def get_funds():






if __name__ == '__main__':
	run(key.key, key.secret)
