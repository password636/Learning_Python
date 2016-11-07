class TestClass(object):
	a = 10
	b = 20
	c = 30
	def __init__(self):
		self.d = 40


#print(TestClass.__dict__.keys())
inst1 = TestClass()


print(inst1.a)

#inst1.a = 100
inst1.__class__.a = 100
print(TestClass.__dict__)
#del( TestClass.a )
#print(inst1.__class__.a)
#inst1.d = 50
#print(inst1.__dict__.keys())
try:
	inst1.e
except:
	print('inst1.e is not defined yet')
else:
	print('inst1.e is defined already')

TestClass.e = 50	# add a class variable to class variable model
inst2 = TestClass()	# new object has this new class variable
print('inst2.e', inst2.e)
print('inst1.e', inst1.e)

print()

print(inst1.a)
del TestClass.a		# delete a class variable from class variable model
try:
	inst1.a		# inst1.a is not COW yet, so the pointer is empty now
except:
	print('inst1.a is not defined yet')
else:
	print('inst1.a is defined already')

inst3 = TestClass()
try:
	inst3.a		# inst3 doesn't have the pointer to a since it has been deleted from class variable model
except:
	print('inst3.a is not defined yet')
else:
	print('inst3.a is defined already')
