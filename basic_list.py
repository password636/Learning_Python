shoplist = ['apple', 'mango', 'carrot', 'banana']

# reference an item
print(shoplist[2])      # index starting from 0

# print the list
print(shoplist)         # neatly with print()

# iterate the list
for item in shoplist:   # use for..in loop to iterate directly
    print('*'+item, end=' ')
print()

# append an item
shoplist.append('rice')
print('appended:', shoplist)

# delete an item
del shoplist[1]
print(' deleted:', shoplist)

# sort the list
shoplist.sort()         # side effects
print('  sorted:', shoplist)

