shoplist = ['apple','carrot','banana']
print(shoplist)
shoplist.sort()
print(shoplist)

shoplist.append('apple')
print(shoplist)

print(len(shoplist))

for i in shoplist:
	print(i)


print(shoplist[1])
del shoplist[0]
print(shoplist)


list2 = ['tree', 'flower', shoplist]
print(len(list2))
print(list2)
list2.append(shoplist)
print(len(list2))
print(list2)

list2.append(('tu1','tu2'))
print(len(list2))
print(list2)

list3 = ['in', 'ser', 't', 'd']
print(list3[1:3])
print('hello'[:])
print('hello'[1:])
print('hello'[:3])
print('hello'[1:4])
print('hello'[:-1])
print('hello'[::-1])



