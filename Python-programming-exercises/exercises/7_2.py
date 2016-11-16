s = input()
dimens = [int(x) for x in s.split(',')]
row = dimens[0]
col = dimens[1]
#mylist = [[0 for j in range(col)] for i in range(row)]
#mylist = [[0 for j in range(row)] for i in range(col)]
mylist = [[i*j for j in range(col)] for i in range(row)]
print(mylist)
