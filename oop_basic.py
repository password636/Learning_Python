class Person:
	'''This class tries to represent all the features of Python class/object'''

	name = 'human being'
	language = 'English'
	__sex = 'male'		# private data member

	def __init__ (self, name):	# constructor, private method
		self.name = name	# object variable, hides class.name

	@classmethod
	def sayhiforall(cls):		# class method
		'''say hi for all objects'''
		print('A big hi from all', cls.name)

	def welcome(self, yourname):	# oject method
		"""say some welcome message """
		print('Hello {}, {} welcomes you.'.format(yourname, self.name))

	def sayhi(self):
		self.hi = 'hi'		# add a new object variable
		self.__sayhi()		# __sayhi() is defined after

	def __sayhi(self):		# private method
		print(self.hi)

	# use members of the same class, must use self or class name
	def saymanyhi(self):
		print("****saymanyhi****")
		self.welcome('somebody')		# call another object method

		self.sayhiforall()	# call another class method via object
		Person.sayhiforall()	# call another class method via class name

		__sex = 'not human'	# belongs to saymanyhi(), not class member

		Person.__sex = 'female'	# access data member via class name
		self.__sex = 'female2'	# access data member via object, change it again

		Person.hi = 'HiPerson'	# add a new class variable
		self.hi = 'Hiself'	# change existed data member
		print("****saymanyhi end****")

	def getSex(self):
		return self.__sex

p = Person('Daniel')
# class docstring, class/object method docstring, either class name or object is ok
print(Person.__doc__)
print(p.__doc__)
print(Person.welcome.__doc__)
print(p.welcome.__doc__)
print(Person.sayhiforall.__doc__)
print(p.sayhiforall.__doc__)
print()

print('Before calling saymanyhi():', p.getSex())
print(p.__dict__.keys())	# get all object variables of an object
p.val1 = '100'
print(p.__dict__.keys())	# get all object variables of an object
print(Person.__dict__.keys())	# get all object variables of an object
Person.var2 = '1000'
print(Person.__dict__.keys())	# get all object variables of an object

# member: public or private
p.saymanyhi()	# public method
#p.__sayhi();	# error, private method
print(p.name)	# public data member
#print(p.__sex)	# error, private data member

print('After calling saymanyhi():', p.getSex())
print('After calling saymanyhi():', p.hi)
print('After calling saymanyhi():', Person.hi)

print()

# object method invocation
p.welcome('Zongliang')
Person('Jo').welcome('Zongliang')
#Person.welcome('Zongliang')	# error

# class method invocation
p.sayhiforall()	
Person('any').sayhiforall()
Person.sayhiforall()

print()

print(Person.language)	# access class variable via class name
print(p.language)	# access class variable via object
print(Person.name)	# access class variable via class name
print(p.name)		# object.name hides class.name

print()

print(p.__dict__.keys())
p.sayhi();			# now p has one more object variable - hi
print(p.__dict__.keys())
print(p.hi)

#t = Person('Carl')
#print(t.__dict__.keys())
# print(t.hi) 		# error, t has not called sayhi(), so it doesn't have member `hi'


