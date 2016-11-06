print('{0:.3f}'.format(1.0/3))
print('{0:_^11}'.format('hello'))
print('{name} wrote {book}'.format(name='Swaroop', book='A Byte of Python'))
print('{:d}'.format(3))

class Person:
	def __init__(self, name, age = 30):
		self.name = name
		self.age  = age

p = Person('Daniel')

print('The peroson\'s name is {0.name}, age is {1.age}.'.format(p, p))

shoplist = ['apple', 'mango', 'carrot']
print('My second to buy is {0[1]}.'.format(shoplist))
