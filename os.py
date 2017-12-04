import os
# for absolute pathname, return it untouched
# for relative pathname or filename, return process's cwd + the argument
# the pathname or filename doesn't need to be existed

# construct an absolute pathname, depends on cwd
print( os.path.abspath('os.py') )
print( os.path.abspath('/a/b/os.py') )
print( os.path.abspath('b/os.py') )

print( os.path.join('a', 'b', 'c') )	# a/b/c, not /a/b/c
print( os.path.join('..', '..', 'c') )	# a/b/c, not /a/b/c

print( 'Current Working Directory is', os.getcwd() )





lib_path = os.path.abspath(os.path.join('..', '..', '..', 'lib'))
print(lib_path)

print(os.path.abspath('./ddd'))
