def total(a=5, *numbers, **phonebook):
	print('a', a)

	for single_item in numbers:
		print('single_item', single_item)

	for first_part, second_part in phonebook.items():
		print(first_part, second_part)

total(10,1,2,3,Jack=1123,John=2231,Inge=1560)

def totala(a=5, *numbers, b, **phonebook):
	print('a', a)

	for single_item in numbers:
		print('single_item', single_item)

	for first_part, second_part in phonebook.items():
		print(first_part, second_part)

totala(10,1,2,3,b=8,Jack=1123,John=2231,Inge=1560)

def func(**arg):
	for key,value in arg.items():
		print(key, value)

func(a=1,b=2)
