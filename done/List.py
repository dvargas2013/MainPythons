"""Deals with lists of information. Many probability things are found here."""

import math
import itertools
from collections import deque, defaultdict
from functools import wraps, reduce
from inspect import isgeneratorfunction
from itertools import zip_longest
from operator import mul
from typing import Collection
from numbers import Number

from done.Number import parse_number

if hasattr(math, "lcm"):
    product = math.prod
    lcm = math.lcm
    gcd = math.gcd
else:
    def product(iterable):
        """basically sum but its product instead"""
        return reduce(mul, iterable, 1)


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


def batch(seq, n=2):
    """Cuts up an iterable into chunks os size n. the last one is whatever data is left

DEPRECATION WARNING: unless you NEED the output to be the same type as the input. use `itertools.batched` instead
    """
    for i in range(0, len(seq), n):
        yield seq[i:i + n]


if hasattr(itertools, "batched"):
    chunk = itertools.batched
else:
    chunk = batch


def is_iterable(potentially_iterable):
    """checks if something is iterable"""
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


def tupleSum(tuple1, tuple2):
    return tuple(map(sum, zip(tuple1, tuple2)))


def line(start: tuple, incr: tuple, length: int):
    """start+incr is first, start+incr+incr is 2nd, etc"""
    return [(start := tupleSum(start, incr)) for _ in range(length)]


def diagonals(N, M):
    for i in range(N):
        yield line((i + 1, -1), (-1, 1), min(i + 1, M))
    for j in range(1, M):
        yield line((N, j - 1), (-1, 1), min(M - j, N))


def interleave(*iterables):
    iterables = list(iterables)
    for ind, _i in enumerate(iterables):
        if not is_iterable(_i):
            raise IndexError(f"doesn't seem to be iterable: {_i!s}")
        if not hasattr(_i, "__next__"):
            iterables[ind] = iter(_i)

    while iterables:
        i = 0
        try:
            for i, n in enumerate(iterables):
                yield next(n)
        except StopIteration:
            iterables.pop(i)


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


def applyToGenerator(*fs, warning=True):
    """
    applies the given function to the generator created when the generator function is called

    examples:

>>> @applyToGenerator(list)
... def fibo(n):
...    a, b = 0, 1
...    for i in range(n):
...        yield a
...        a, b = b, a + b
>>> fibo(10) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

>>> @applyToGenerator(list, reversed, list)
... def squares(n):
...     for i in range(n):
...         yield i * i
>>> squares(10) == [81, 64, 49, 36, 25, 16, 9, 4, 1, 0]
        """

    def outer(generator):
        if warning and not isgeneratorfunction(generator):
            from warnings import warn
            warn(f"{generator.__qualname__} does not seem to be a generator function", stacklevel=2)

        @wraps(generator)
        def inner(*args, **kwd):
            rv = generator(*args, **kwd)
            for f in fs:
                rv = f(rv)
            return rv

        return inner

    return outer


def apply(*x):
    """
this is just applyToGenerator without the warning if you are applying it to something other than a generator

for example, you might want to call it to print output:
>>> @apply(print)
... def helloworld(): return "Hello, World!"
... helloworld()
is a valid hello world script
it prints hello world (returns None)

basically if there was no decorator, you'd have to do
>>> print(helloworld())
every time
"""
    return applyToGenerator(*x, warning=False)


class Polynomial:
    """polynomial class: add, subtract, multiply, divide

    internally represented by a tuple of ints and floats
    in little endian
    so that the constant term is accessed via data[0]
    and the coefficient of x squared via data[2]
    """

    def __init__(self, data: Collection[Number] = tuple()):
        if type(data) == str:
            from warnings import warn
            warn(f"You might be looking for Polynomial.fromString: Polynomial({data})")

        if len(data) == 0:
            self.data = (0,)
            return

        data = list(map(parse_number, data))
        while len(data) > 1 and data[-1] == 0:
            data.pop()

        self.data = data

    def __copy__(self):
        return Polynomial(self.data)

    # TODO : implement derivative

    @staticmethod
    def fromString(in_str):
        to_parse = ''.join(i for i in str(in_str) if i.isalnum() or i in '.+-/*')
        sym = {i for i in to_parse if i.isalpha()}
        if not sym: return [parse_number(to_parse)]
        if len(sym) != 1: return []
        sym = sym.pop()
        to_parse = to_parse.replace('-', '+-').replace(f'-{sym}', f'-1{sym}')
        n, p = [], []
        if to_parse[0] == '+': to_parse = f'0{to_parse}'
        for string in to_parse.rsplit('+'):
            if string[-1] == sym: string += '1'
            if string[0] == sym: string = f'1{string}'
            if string.find(sym) == -1: string += f'{sym}0'
            n += [parse_number(string.rsplit(sym)[0])]
            p += [parse_number(string.rsplit(sym)[1])]
        dic = [0] * int(max(p) + 1)
        for pi, ni in zip(p, n): dic[pi] += ni
        return Polynomial(dic)

    def __call__(self, num):
        return sum(coef * num ** power for power, coef in enumerate(self.data))

    def iterCall(self, iterable):
        for i in iterable:
            yield self(i)

    def __eq__(self, other):
        return len(self) == len(other) and all(i == j for i, j in zip(self, other))

    def __add__(self, l2):
        if isinstance(l2, Number):
            l2 = Polynomial([l2])

        return Polynomial([a + b for a, b in zip_longest(self.data, l2, fillvalue=0)])

    __radd__ = __add__

    def __neg__(self):
        return Polynomial([-i for i in self.data])

    def __sub__(self, l2):
        return self + -l2

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return f"Polynomial({self.data!r})"

    def __iter__(self):
        return iter(self.data)

    def __getitem__(self, i):
        if type(i) == int: return parse_number(self.data[i])
        if type(i) == slice: return [self[i] for i in range(parse_number(i.start), parse_number(i.stop) or len(self),
                                                            parse_number(i.step) or 1)]

    def __mul__(self, l2):
        if isinstance(l2, Number):
            l2 = Polynomial([l2])

        l3 = [0] * (len(self) + len(l2) - 1)
        for p1, c1 in enumerate(self.data):
            if c1 == 0: continue  # this one is worth checking cause it skips a whole loop
            for p2, c2 in enumerate(l2):
                l3[p1 + p2] += c1 * c2
        return Polynomial(l3)

    __rmul__ = __mul__

    def __truediv__(self, s2):
        return f'{self // s2}+({self % s2})'

    def _truediv(self, l2):
        if isinstance(l2, Number):
            l2 = Polynomial([l2])

        num = list(self.data)
        den = list(l2.data)

        if len(num) < len(den):
            return [0, *num]

        # Shift den towards right, so it's the same degree as num
        shiftlen = len(num) - len(den)
        den = [0] * shiftlen + den

        quot = []
        divisor = den[-1]
        for _ in range(shiftlen + 1):
            quot.append(mult := num[-1] / divisor)

            # num - mult * den, but don't bother if mult == 0
            if mult != 0:
                num = [u - (mult * v) for u, v in zip(num, den)]

            num.pop()
            den.pop(0)

        quot.reverse()
        return quot, num

    def __floordiv__(self, l2):
        return Polynomial(self._truediv(l2)[0])

    def __mod__(self, l2):
        return Polynomial(self._truediv(l2)[1])

    def __str__(self):
        return '+'.join(f"{'' if coef == 1 and power else coef}x{'' if power == 1 else power}"
                        for power, coef in reversed(list(enumerate(self.data)))
                        if coef).replace('x0', '').replace('+-', '-')


def LagrangeInterpolation(xs: Collection[int], ys: Collection[int]):
    """find a polynomial where all(f(x)==y for x,y in zip(xs,ys))

    note: use scipy.interpolate.lagrange instead
    """
    xset = set(xs)

    def Li(x, y):
        """polynomial where f(x)=y for given x,y and f(x)=0 for all x in zeroxs"""
        zeroxs = xset - {x}
        # y = (x - a) / (x1 - a)
        # == 1 when x == x1
        # == 0 when x == a
        return y * product(Polynomial([-a, 1]) // (x - a) for a in zeroxs)

    return sum(Li(x, y) for x, y in zip(xs, ys))


class BitString:
    """compact hex storage"""

    def __init__(self, ints=None):
        if type(ints) == int:
            self.data = ints
            self.length = math.ceil(ints.bit_length() / 4)
        else:
            self.data = 0
            self.length = 0
            if ints is not None:
                for i in ints: self.add(i)

    def add(self, num):
        """inserts num into the BitString (%16 only)"""
        self.data += (num % 16) << (4 * self.length)
        self.length += 1

    def __len__(self):
        return self.length

    def __getitem__(self, i):
        if i >= self.length or i < 0: i %= self.length
        return (self.data >> (4 * i)) % 16

    def __iter__(self):
        x = self.data
        for _ in range(self.length):
            yield x % 16
            x >>= 4

    def __eq__(self, other):
        return len(self) == len(other) and all(i == j for i, j in zip(self, other))

    def __str__(self):
        return '.'.join(format(i, '02d') for i in self)

    def __repr__(self):
        return f"BitString(0x{format(self.data, 'x')})"


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
