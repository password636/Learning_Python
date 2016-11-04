def reverse(text):
	return text[::-1]
def is_palindrome(text):
	return text.lower() == reverse(text).lower()

something = input('Enter something: ')

forbidden = (
'.', '?', '!', ':',
';', '-', '_', '(',
')', '[', ']', '\'',
'"', '/', ',', '\\',
' ', '\t', '\n',
)
mylist = []
for c in something:
	if c not in forbidden:
		mylist.append(c)

something = ''.join(mylist)
print('stripped input: ', something)
if is_palindrome(something):
	print('Yes, it is a palindrome')
else:
	print('No, it is not a palindrome')
