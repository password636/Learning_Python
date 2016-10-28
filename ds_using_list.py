# This is my shopping list
shoplist = ['apple','pen','soap','shampoo']
print('I have', len(shoplist), 'items to purchase.')

print('These items are:', end=' ')
for i in shoplist:
	print(i, end=' ')

print('\nI also have to buy rice')
shoplist.append('rice')
print('My shopping list is now', shoplist)

print('I will sort my list now')
shoplist.sort()
print('Sorted shopping list is', shoplist)

print('The first item I want to buy is', shoplist[0])
olditem = shoplist[0]
del(shoplist[0])
print('I have bought', olditem)
print('My shopping list is now', shoplist)
