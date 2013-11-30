#!/d/python27/python
# -*- coding: utf8 -*-

import threading
import time
import sys
import os

import exchange

def test_thread(key, secret):
	for i in range(0, 10):
		print '%s %s' % (threading.currentThread(), i)
		if __debug__:
			print 'it is debug'
		time.sleep(1.1)

if __name__ == '__main__':
	import key

	while True:
#		exchange_thread = threading.Thread(target=test_thread, args=(key.key, key.secret))
		exchange_thread = threading.Thread(target=exchange.run, args=(key.key, key.secret))
		exchange_thread.setDaemon(True)
		exchange_thread.start()

		time.sleep(60*5)
		
		python = sys.executable
		os.execl(python, python, '-O', *sys.argv)
