n = int(input())

def factorial(n):
	sum = n		#
	n -= 1		#
	while n > 1:
		sum *= n
		n -= 1
	return sum

def factorial1(n):
	sum = 1		#
	while n > 1:
		sum *= n
		n -= 1
	return sum

print(factorial(n))
print(factorial1(n))
