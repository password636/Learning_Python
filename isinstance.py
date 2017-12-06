class A(object):
	pass

class B(A):
	pass

b = B()
print(isinstance(b, A))
