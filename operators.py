print(13 % 3)		# 1
print(1 + 2)		# 3
print(2 - 1)		# 1
print(2 * 3)		# 6
print(4 / 2)		# 2.0, [S]
# Just like in C, operators will cause (implicit) conversions. 
# If either operand is float, (maybe the other is converted to float, so) the result will be float. 
print(13 % 3.0)		# 1.0
print(1.0 + 2)		# 3.0
print(2 - 1.0)		# 1.0
print(2.00 * 3)		# 6.0
print(4 / 2.0)		# 2.0

# something new
print('a' + 'b')	# ab			string concatenation
print('la' * 3)		# lalala		string repetition
print(13 // 3)		# 4  (4.333~)
print(-13 // 3)		# -5 (-4.333~)
print(7.2 // 2)		# 3.0 (3.6)		
print(2 ** 10)		# 1024

# integer division, not like C, but like Perl
print(13 / 3)		# 4.333333333333333

print(2 << 2)		# 8
print(11 >> 2)		# 2
print(-2 << 2)		# -8?
print(-11 >> 1)		# -6?

print(5 ^ 3)		# 6	 [S]
print(~5)			# -6 [S]

# relational operators. Can operate both numbers and strings, but can't mix.
print(1 < 2)
print('A' < 'a')

# logical operators.
print(not True)
x = True
print(not x)

x = False
y = True
print(x and y)
print(y or x)




