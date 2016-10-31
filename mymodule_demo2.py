
__version__ = '1'

from mymodule import sayhi, __version__

__version__ = '2'
sayhi()
print('Version', __version__)
