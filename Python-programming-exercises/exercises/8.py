#print([x for x in input().split(',')].sort())a

mylist = [x for x in input().split(',')]
mylist.sort()
print(','.join(mylist))

'''
l.split() returns None, not the sorted list
'''
