content = '''
Python is fun?
I guess you'd say
But from what I experienced
It was not that fun
	So 
	Just bear with it!
'''

f = open('mypoem.txt', 'w')
f.write(content)
f.close()

f = open('mypoem.txt')
while True:
	l = f.readline()
	if len(l) == 0:
		break
	print(l, end='')

f.close()
