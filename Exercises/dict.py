ab = {
	'126':'db_23@126.com',
	'sina':'ekinlee1111@sina.com',
	'hotmail':'lizongliang111@hotmail.com'
}

#print(ab.items())
print(ab)
print(ab['126'])
del ab['hotmail']
print(ab)
ab['gmail'] = 'lizongliang111@gmail.com'
print(ab)

for key,value in ab.items():
	print(key, value)


if 'db_23@126.com' not in ab:
	print('pair exists')

print(len(ab))
