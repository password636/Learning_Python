lines = []
while True:
    s = input()
    if s:
        lines.append(s.upper())
    else:
        break;			# quit reading input when entering 

for sentence in lines:
    print( sentence )

