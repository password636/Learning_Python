shoplist = ['apple', 'mango', 'carrot', 'banana']
print('I have', len(shoplist), 'items to buy')
print('The items are:', end=' ')
for item in shoplist:
	print(item, end=' ')
print()

print('Adding rice to the list')
shoplist.append('rice')
print(shoplist)

shoplist.sort()
print('Sorted shoplist:', shoplist)

print('The first item I want to buy is', shoplist[0])
del shoplist[0]
print('Bought the first, left itmes are:', shoplist)

