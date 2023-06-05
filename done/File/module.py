from inspect import ismodule
from os.path import dirname
from pkgutil import iter_modules
from importlib import reload
from sys import modules

reImport = reload


def submodules(_file):
    """given a __file__ will dirname and iter_modules to get .name s

>>> __all__ = submodules(__file__)
"""
    return [module_info.name for module_info in iter_modules([dirname(_file)])]


def filter_off_modules_and_dunder(_dir, _globals):
    """given dir() will filter off any modules and __ names. needs globals()

>>> __all__ = filter_off_modules_and_dunder(dir(),globals())
"""

    def _filter(s):
        return not (s.startswith("__") or ismodule(_globals[s]))

    return list(filter(_filter, _dir))


def add_to_all(f):
    module = modules[f.__module__]
    if not hasattr(module, "__all__"):
        setattr(module, "__all__", [])
    if f.__name__ not in module.__all__:
        module.__all__.append(f.__name__)
    return f
