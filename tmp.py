#import sys
#print (sys.path)

from sys import path;
print (path);
#print (sys.path)	# error

from math import sqrt
print('Square root of 16 is', sqrt(16))

if __name__ == '__main__':
	print('This program is running by itself')
else:
	print('I am being imported from another module')


print (r'hello, \
			world')

