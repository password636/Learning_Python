def add(a, b, c):
	return a+b+c

x, y, z = 10, 11, 12
print(add(x,y,z))

i, j, k = x, y, z = 3, 5, 7
print(add(i,j,k))
print(add(x,y,z))
