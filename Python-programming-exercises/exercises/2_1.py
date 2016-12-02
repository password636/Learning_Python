n = int(input())

def factorial(n):
	sum = n
	while n > 1:
		n -= 1
		sum *= n
	return sum

def factorial_rec(n):
	if n == 1 :
		return 1
	else :
		return n * factorial_rec(n-1)

def factorial1(n):
	sum = 1
	while n > 1 :
		sum *= n
		n -= 1
	return sum

print(factorial(n))
print(factorial_rec(n))
print(factorial1(n))

