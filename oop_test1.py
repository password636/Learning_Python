class Person:
	'''A test class'''
	name = 'human being'
	
	def __init__(self, name):
		self.name = name
	def sayhi(self, yourname):
		print('Hi {}, I\'m {}.'.format(yourname, self.name))

class subPerson(Person):
	def __init__(self, name):
		Person.__init__(self, name)# must call base class __init__() explicitly 
	def sayhi(self, yourname):
		print('I\'m subPerson {} to say hi'.format(self.name))
		Person.sayhi(self, yourname)


def sayhi(person, name):
	person.sayhi(name)


p = Person('Daniel')
sp= subPerson('Jo')

sayhi(p, 'Zongliang')
sayhi(sp,'Zongliang')



