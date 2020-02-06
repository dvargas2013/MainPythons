#!/usr/bin/env python3

"""
These can be accessed using
>>> import done
and then calling
>>> done.*
"""
from . import File, Game, List, Math, Number, Solver, String, StringGenerators, StringSolver, Codes, Time

"""
These can be accessed using
>>> from done import *
"""
__all__ = ['File', 'Game', 'List', 'Math', 'Number', 'Solver',
           'String', 'StringGenerators', 'StringSolver', 'Codes', 'Time']


def TEST():
    """Runs the test module's main function"""
    from . import test
    test.main()
