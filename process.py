import multiprocessing
import os 

class AdminSessionHandler(multiprocessing.Process):
	def __init__(self):
		multiprocessing.Process.__init__(self)
		print('th pid:', os.getpid())

	def run(self):
		print('this pid:', os.getpid())
		



print('pid:', os.getpid())
ad = AdminSessionHandler()
ad.start()
