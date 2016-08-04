#!/usr/bin/env python3

__all__ = ['AllInfo', 'showInfo',
           'File', 'Game', 'List', 'Math', 'Number', 'Solver', 'String', 'Time']

from . import File,Game,List,Math,Number,Solver,String,Time

AllInfo = '\n\n'.join([eval(i).Info for i in __all__[2:]])
def showInfo(): String.smartPrint(AllInfo)

'''
from sys import version_info
if version_info > (3,0): _range = range
else: _range = xrange
    
import platform
if platform.mac_ver()[0]: comp = 'st_birthtime'
elif platform.win32_ver()[0]: comp = 'ctime'
else: comp = ''
'''