class A:
	def getString(self):
		self.s = input('Enter something: ')

	def printString(self):
		print(self.s.upper())

a = A();
a.getString()
a.printString()

