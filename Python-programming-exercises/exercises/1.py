# 1st edition
mylist = []	# empty list
for i in range(2000, 3201) :	# +1->stop, [start, stop]
	if i % 7 == 0 and i % 5 != 0:
		mylist.append(i)

print(mylist)

# answer
l=[]
for i in range(2000, 3201):
    if (i%7==0) and (i%5!=0):
        l.append(str(i))

print (','.join(l))

# 2nd edition
mylist = []
for i in range(2000, 3201):
	if i%7==0 and i%5!=0:
		mylist.append(str(i))

print(','.join(mylist))
