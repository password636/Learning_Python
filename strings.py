# multi-line string
print("""How to learn English
              by Slash
    It seems excessive, but that doesn't mean
it didn't happen. """)
#print("this is a multi-
#line string")
print('this is a one \
line string, although I can \
write multi-line here')

# 3 types of delimiters(single, double, triple), use one of the types not appeared
# in string. For example, use double or triple if just single quotes appeared
# in string; use triple 
print('What\'s your name?') # also work, just need more favor
print("What's your name?")  # preferred way, double quotes design goal
print('''What's your name?''')
print("""What's your name?""")

print("What\"s your name?") # also work, just need more favor
print('What"s your name?')  # preferred way, single quotes design goal
print('''What"s your name?''')
print("""What"s your name?""")

print("""What"s your n'ame?""")  
print('''What"s your n'ame?''')
print('''2What\'''s your name?''')
print("""what\"""s your name?""")

print('1what\'''s your name?')
print('1what\'\'\'s your name?')
print('li''zongliang')

print("3what'''s your name?")
print("""3what'''s your name?""")

print('4what"""s your name?')
print("4what\"""s your name?")
print("4what\"\"\"s your name?")
print('''4what"""s your name?''')

print('''what''''s your na''me')

# no strong quotes in Python. 
print('Hello\nworld')
print("Hello\nworld")
print('''Hello\nworld''')
print("""Hello\nworld""")
