n = int(input('Enter an integer: '))
d = dict()	# for d used in for-loop, otherwise name 'd' is not defined
for i in range(1, n+1):
	d[i] = i*i
print(d)
print(d[2])
