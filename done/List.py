"""Deals with lists of information. Many probability things are found here."""

from .Math import fact, comb
from math import exp
from collections import deque, defaultdict
from functools import wraps
from inspect import isgeneratorfunction

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


def poisson(y, x):
    """calculate the poisson probability given mean rate and successes"""
    if type(x) == list:
        return round(sum(poisson(y, i) for i in x), 4)
    return round(exp(-y) * (y ** x) / fact(x), 4)


def Dev(lis, population=False):
    """Sample Standard Deviation"""
    xbar = sum(lis) / len(lis)
    print('x%s = %s' % (chr(773), xbar))
    sum_square_deviation = sum(x * x for x in lis) - sum(x for x in lis) ** 2 / len(lis)
    print("(x-x%s)^2 = %s" % (chr(773), sum_square_deviation))
    var = sum_square_deviation / (len(lis) - (not population))
    print("Variance: %s" % var)
    return var ** .5


def freqDev(mid_freq):
    """Sample standard deviation with frequencies defined in a matrix form"""
    n = sum(mid_freq.values())
    print("n = %s" % n)
    x2 = sum(j * i * i for i, j in mid_freq.items())
    print("f*x^2 = %s" % x2)
    x = sum(j * i for i, j in mid_freq.items())
    print("f*x = %s" % x)
    x_2 = x * x
    print("(f*x)^2 = %s" % x_2)
    var = (x2 - x_2 / n) / (n - 1)
    print("Variance: %s" % var)
    return var ** .5


def probDev(x_px):
    """Sample standard deviation with probabilities defined in matrix form"""
    xbar = sum(i * j for i, j in x_px.items())
    print('x%s = %s' % (chr(773), xbar))
    var = sum((i - xbar) ** 2 * j for i, j in
              x_px.items())  # sum(j*i*i for i,j in x_px.items())-sum(j*i for i,j in x_px.items())**2
    print("Variance: %s" % var)
    dev = var ** .5
    return dev


def hypergeometric(start, total, runs, success):
    """Hyper-geometric probability given starting choice, total, tests to run, and successes"""
    if start <= total and runs <= total:
        if type(success) == list:
            return sum(hypergeometric(start, total, runs, i) for i in success)
        elif success <= start and success <= runs and success <= total:
            return comb(start, success) * comb(total - start, runs - success) / comb(total, runs)
    return 0


def online_average(item=0, p_sum=0, p_count=-1):
    """calculate the mean given 1 item at a time. defaults assigned such that online_average() == (0,0)

>>> p_sum, p_count = online_average() # 0, 0
>>> for i in range(100):
...     p_sum, p_count = online_average(i, p_sum, p_count)

>>> assert p_sum == sum(range(100))
>>> assert p_count == 100
    """
    return p_sum + item, p_count + 1


def median(lis):
    """Calculate the median of the list given"""
    a = (len(lis) + 1) // 2
    lis.sort()
    return (lis[a - 1] + lis[-a]) / 2


def gcd(lis):
    """Calculate the greatest common divisor of list given"""
    a = lis[0]
    for b in lis[1:]:
        while b: a, b = b, a % b
    return a


def lcm(lis):
    """Calculate the least common multiple of list given"""
    a = 1
    for i in lis: a *= i
    b = a / gcd(lis) ** (len(lis) - 1)
    if int(b) == b: return int(b)
    return b


def cross(*lists, tupled=False):
    """product magic"""
    from itertools import product
    pd = product(*lists)
    if not tupled:
        return [sum(i) for i in pd]
    return list(pd)


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
