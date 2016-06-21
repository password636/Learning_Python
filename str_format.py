age = 20 # `age' is an int object
name = 'Swaroop' # name is a str object

print('{0} was {1} years old when he wrote this book'.format(name, age))
print('Why is {0} playing with that python?'.format(name))
#
my_str = name + ' is ' + str(age) + ' years old'
print (my_str)
#
print (name + ' is ' + str(age) + ' years old')
#
print ('{} was {} years old when he wrote this book'.format(name, age))
print ('Why is {} playing with that python?'.format(name))
#
print('{0:.3f}'.format(1.0/3))
print('{0:_^11}'.format('hello'))
print('{name} wrote {book}'.format(name='Swaroop', book='A Byte of Python'))
#
print('a', end='')
print('b', end='')
#
print('a', end=' ')
print('b', end=' ')
print('c')
#

#

#
print ('hello\tworld')
print (r'hello\tworld')
print (R'hello\tworld')
#
print('''hello\tworld''')
#
print (r'''This is will not remove
the magic of triquotes.''')
