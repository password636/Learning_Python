def get_all_index(mylist, value):
	'''
	'''
	try:
		resultList = []
		start = 0
		while True:
			index = mylist.index(value, start)
			resultList.append(index)
			start = index + 1
	except ValueError:
		pass

	return resultList

def remove_all_item(mylist, value):
	'''
	'''
	try:
		while True:
			mylist.remove(value)
	except ValueError:
		pass

#a = ['a', 'b', 0, 1, 2, 3, 'b']
#print(get_all_index(a, 'b'))
