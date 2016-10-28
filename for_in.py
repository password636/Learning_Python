# can get only keys
for key in {'126':'com', 'hotmail':'org'}: 
	print(key)

# must use items()
for key,value in {'126':'com', 'hotmail':'org'}.items(): 
	print(key,value)

# with set
for element in {'126','com', 'hotmail','org'}: 
	print(element)
