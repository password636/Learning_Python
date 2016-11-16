m = int(input('Enter an integer: '))
m1 = m

# implement by loop
r = 1
while m > 1:	# no need to multiple by 1, so >=1 can be just >1
	r *= m
	m -= 1
print(r)

#implement by recursive
def factorial(n):
	if n == 1:
		return 1
	return n * factorial(n-1)

print(factorial(m1))


