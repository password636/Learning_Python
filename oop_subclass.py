class SchoolMember:
	"""Represents any school member."""
	def __init__(self, name, age):
		self.name = name
		self.age = age
		print('(Initialized SchoolMember: {})'.format(name))

	def tell(self):
		'''Tell my details.'''
		print('Name: "{}" Age: "{}"'.format(self.name, self.age), end=" ")

class empty:
	pass

class Teacher(SchoolMember):
	'''Represents a teache'''
	def __init__(self, name, age, salary):
		SchoolMember.__init__(self, name, age)
		self.salary = salary
		print('(Initialized Teacher: {})'.format(self.name))

	def tell(self):
		SchoolMember.tell(self)
		print('Salary: "{:d}"'.format(self.salary))

class Student (SchoolMember, empty):
	'''Represents a student.'''
	def __init__(self, name, age, marks):
		SchoolMember.__init__(self, name, age)
		self.marks = marks
		print('(initialized student: {})'.format(self.name))
	def tell(self):
		SchoolMember.tell(self)
		print('Marks: "{:d}"'.format(self.marks))


t = Teacher('Mrs. Shrividya', 40, 30000)
s = Student('Swaroop', 25, 75)

print()

members = [t, s]

for member in members:
	member.tell()

		
