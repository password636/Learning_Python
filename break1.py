running = True
n = 0
while running:
	s = input('Enter something : ')
	if s == 'break':
		break
	elif s == 'quit':
		running = False
else:
	print('quit the while loop')
print('continue after while')
