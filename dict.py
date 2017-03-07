mydict = {'name':'li zongliang', 'age': 34}
# view objects are iterable
for i in mydict.keys():
    print(i)
for i in mydict.values():
    print(i)
for i in mydict.items():
    print(i)

mydict.update(sex='male', marriage='single')
print(mydict)

print(mydict.setdefault('sex'))
print(mydict.setdefault('child'))
print(mydict)
print(mydict.setdefault('height', 170))
print(mydict)
