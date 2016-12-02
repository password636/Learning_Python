# 1st edition
mylist = []				# create an empty list
for i in range(2000, 3201) :		# [2000, 3200]
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
		# mylist.append(i)	# why must use str()?

print(','.join(mylist))
