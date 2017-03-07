for i in range(1,5):
    print(i)
else:
    print('The for loop is over')


# string
for i in 'hello':
    print(i)



i = 100
print(i)
for i in range(4):  # not a new i
    print(i)
print(i)            # value changed


for j in range(4,0,-1):     # a new name j
    print(j)    
print(j)            # Names in the target list are not deleted when the loop is finished

# for-else, else just focuses on break
for k in range(4):
    if k == 3:
        break
    print(k)
else:
    print('no break in the for loop')
    
    
for l in range(4):
    if l == 3:
        continue
    print(l)            
else:
    print('no break in the for loop')

    
for l in range(4):
    print(l)            
else:
    print('no break in the for loop')
    
for k,v in {'name':'li zongliang', 'age': 34}.items():
    print(k)
    print(v)
    print(k,v)

for k in {'name':'li zongliang', 'age': 34}.items():
    print(k)
     
    
# bug: for loop on list
mylist = ['a','b','c','d','e']
mylist1 = ['a','b','c','d','e']
for i in mylist:
    print(i)
    mylist.remove(i)
print('mylist', mylist)
# use soft copy to iterate
for i in mylist1[:]:
    print(i)
    mylist1.remove(i)
print('mylist1', mylist1)

