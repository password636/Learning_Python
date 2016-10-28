print('hello'[1])

if 'e' in 'hello':
	print('in the word')

print('hello'[-1])

name = 'Swaroop'
if name.startswith('Swa'):
	print('Yes, the string starts with "Swa"')

if 'a' in name:
	print('Yes, it contains the string "a"')

if name.find('war') != -1:
	print('Yes, it contains the string "war"')

delimiter = '_*_'
mylist = ['Brazil', 'Russia', 'India', 'China']
print(delimiter.join(mylist))

