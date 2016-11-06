class TestClass(object):
	a = 10
	b = 20
	c = 30
	def __init__(self):
		self.d = 40


inst1 = TestClass()
print(inst1.a)
#inst1.a = 100
inst1.__class__.a = 100
print(inst1.a)
print(inst1.__class__.a)
inst2 = TestClass()
print(inst2.a)

