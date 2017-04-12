class TruthValueTesting(object):
	#def __bool__(self):
	#	return True
	#def __len__(self):
	#	return 100
	def any(self):
		return False
if TruthValueTesting() :
	print('true')
else:
	print('false')


a = set()
if a:
	print('tt')
else:
	print('ff')
