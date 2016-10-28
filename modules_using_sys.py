import sys

print('The command line arguments are:')
for i in sys.argv:
    print(i)

print('\n\nThe PYTHONPATH is', sys.path, '\n')    

import os
print(os.getcwd())

print( type(sys.argv) )
print( type(sys.path) )
