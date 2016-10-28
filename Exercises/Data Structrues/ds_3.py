ab = {
	'126':'db_23@126.com',
	'gmail':'lizongliang111@gmail.com',
	'sina':'ekinlee1111@sina.com',
}
print(ab['gmail'])
del ab['126']
print('address book has {} entries'.format(len(ab)))

for name, address in ab.items():
	print('My {} e-mail box is {}'.format(name, address))

ab['hotmail'] = 'lizongliang111@hotmail.com'
if 'gmail' in ab :
	print(ab['gmail'])

if 'hello' not in ab:
	print('key "hello" not existed')
