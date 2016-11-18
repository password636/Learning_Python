mylist = []
try:
	while True:
		mylist.append(input())
except EOFError:
	for i in mylist:
		print(i.upper())	

'''
There is no function in Python for you to read multi lines
from standard input. You have to do it by yourself!
'''
