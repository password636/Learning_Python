a = 'A'
b = 10
mydict = {'f':'first', 's':'second'}
print('{1} {0}'.format(a, b))
print(mydict['f'])
#print('{mydict["f"]} {mydict["s"]}'.format(first=a, second=b))
mylist = ['first', 'second']
print('{first["f"]}'.format(first=mydict, second=b))
