#!/usr/bin/env python3

# These can be accessed using
## from done import *
__all__ = ['File', 'Game', 'List', 'Math', 'Number', 'Solver', 'String', 'Codes', 'Time']

# These can be accessed using
## import done
# and then calling
## done.*
from . import File,Game,List,Math,Number,Solver,String,Codes,Time

def TEST():
    from . import test
    test.main()

'''
from sys import version_info
if version_info > (3,0): _range = range
else: _range = xrange
    
import platform
if platform.mac_ver()[0]: comp = 'st_birthtime'
elif platform.win32_ver()[0]: comp = 'ctime'
else: comp = ''
'''