l = input().split(',')
row = int(l[0])
column = int(l[1])
twod = []

for i in range(row):
	tmplist = []
	for j in range(column):
		tmplist.append(i*j)
	twod.append(tmplist)

print(twod)
