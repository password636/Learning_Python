#
def func(a, b):
    print('func:', a)
    print('func:', b)

func(a=3, b=4)
func(b=4, a=3)

def func(a, b=5, c=10):
	print('a is', a, 'and b is', b, 'and c is', c)


func(25, c=24)
func(25, c=24, 9)
func(a=3, b=4)	# overwrite


