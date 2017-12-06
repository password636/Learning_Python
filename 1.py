class MyTest(object):
	def _getitem__(self, i):
		return i*2

mytest = MyTest()
#print(mytest[4])
print(type(mytest).__getitem__(mytest, 4))
