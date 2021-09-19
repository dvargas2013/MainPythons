"""Deals with lists of information. Many probability things are found here."""

import math
from collections import deque, defaultdict
from functools import wraps, reduce
from inspect import isgeneratorfunction
from operator import mul

if hasattr(math, "lcm"):
    lcm = math.lcm
    gcd = math.gcd
else:
    def gcd(*lis):
        """Calculate the greatest common divisor of list given"""
        a = lis[0]
        for b in lis[1:]:
            a = math.gcd(a, b)
        return a


    def lcm(*lis):
        """Calculate the least common multiple of list given"""
        a = lis[0]
        for b in lis[1:]:
            a //= math.gcd(a, b)
            a *= b
        return a


def is_iterable(potentially_iterable):
    """checks if something is iterable"""
    # try:
    #     (*potentially_iterable,)
    #     for _ in potentially_iterable:
    #         break
    # except TypeError:
    #     return False
    # return True
    return hasattr(potentially_iterable, "__iter__")


def window(seq, n=2):
    """Returns a sliding window (of width n) over data from the iterable
s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ..."""
    it = iter(seq)
    win = deque((next(it, None) for _ in range(n)), maxlen=n)
    yield win
    append = win.append
    for e in it:
        append(e)
        yield win


def batch(seq, n=2):
    """Cuts up a iterable into chunks os size n. the last one is whatever data is left"""
    length = len(seq)
    for i in range(0, length, n):
        yield seq[i:i + n]


def interleave(*iterables):
    iterables = list(iterables)
    for ind, _i in enumerate(iterables):
        if not is_iterable(_i):
            raise Exception(f"doesn't seem to be iterable: {_i!s}")
        if not hasattr(_i, "__next__"):
            iterables[ind] = iter(_i)

    while iterables:
        i = 0
        try:
            for i, n in enumerate(iterables):
                yield next(n)
        except StopIteration:
            iterables.pop(i)


def product(iterable):
    return reduce(mul, iterable, 1)


def cross(*lists, sum_func=None):
    """returns a list such that every element in every sublist is paired together
    by default will return a list of tuples. each tuple of size len(lists)
    if sum_func is given, function evaluates to [sum_func(tuple) for tuple in cross(*lists)]
    """
    from itertools import product
    pd = product(*lists)
    if sum_func is None:
        return list(pd)
    return [sum_func(i) for i in pd]


def applyToGenerator(f):
    """
    applies the given function to the generator created when the generator function is called

    example usage:

lets say you have a generator that behaves like

>>> lambda n: iter(range(n, 0, -1))

but you want it to act like

>>> lambda n: list(range(n, 0, -1))

you could define the generator function like so:

>>> @applyToGenerator(list)
... def wild(n):
...    while n > 0:
...         yield n
...         n -= 1
now calling ``wild(5)`` is equivalent to calling ``list(wild(5))``
    """

    def outer(generator):
        if not isgeneratorfunction(generator):
            from warnings import warn
            warn(f"{generator.__qualname__} does not seem to be a generator function", stacklevel=2)

        @wraps(generator)
        def inner(*args, **kwargs):
            return f(generator(*args, **kwargs))

        return inner

    return outer


class CollisionDict(defaultdict):
    def __init__(self, factory, add_func, data=None):
        super().__init__(factory)
        self.add_func = add_func

        if data is not None:
            for k, v in data:
                self.addItem(k, v)

    def addItem(self, key, value):
        self.add_func(self[key], value)


class CollisionDictOfLists(CollisionDict):
    def __init__(self, data=None):
        super().__init__(list, list.append, data)


class CollisionDictOfSets(CollisionDict):
    def __init__(self, data=None):
        super().__init__(set, set.add, data)
