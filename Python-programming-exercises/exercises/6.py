import math
mylist = input('Enter some integers with commas: ').split(',')
outlist = []
C=50
H=30
for i in mylist:
	outlist.append( int( math.sqrt( (2*C*int(i))/H ) ) )
print(outlist)

