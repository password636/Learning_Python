class InputShortException(Exception):
	def __init__(self, length, atleast):
		Exception.__init__(self)	# need to pass self
		self.length = length
		self.atleast = atleast

try:
	line = input('Enter something --> ')
	if len(line) < 3:
		raise InputShortException(len(line), 3)
except InputShortException as ex:
	print('InputShortError: entered {} characters, at least {} needed.'.format(ex.length, ex.atleast))
else:
	print('You have entered', line)
