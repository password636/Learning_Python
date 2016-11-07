try:
	s = input('Enter something --> ')
except (EOFError, KeyboardInterrupt):
	print('Why did you do an EOF on me?')
except KeyboardInterrupt:
	print('You cancelled the operation.')
else:
	print('You entered {}.'.format(s))
