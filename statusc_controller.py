#!/d/python27/python
# -*- coding: utf8 -*-



class StatusController():
	def __init__(self):
		self.file_name = 'exchange status.txt'
	
	def read_status(self):
		f = open(self.file_name, 'w+')
		status = f.read()
		f.close()
		return int(status)
	
	def write_status(self, status):
		f = open(self.file_name, 'w')
		f.write(str(status))
		f.close()
