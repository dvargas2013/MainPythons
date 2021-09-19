"""Searching functions dealing with singular number space - Prioritized for human readability"""

import operator
from math import atan2


def angle(x1, y1, x2, y2):
    """Calculate the angle made by the two points according to x axis"""
    return atan2(y2 - y1, x2 - x1)


def parse_number(input_string, onerror=0):
    """parses the string with int() and float() and picks the best one
if float has no fractional part, it prefers to return an int
if float() throws a value error, it'll return the onerror value
"""
    try:
        get = float(input_string)
        if get % 1: return get
        return int(get)
    except ValueError:
        return onerror


def pyTrip(m, n):
    """Generate a pythagorean triplet using the rule
    (twice the product , difference of squares , sum of squares)
    """
    # when n and m are both odd it is reducible by 2 because mm-nn will be a multiple of 4
    # if n and m have a cofactor . should be kinda obvious that it will be reducible by the cofactor
    return sorted([2 * m * n, abs(m * m - n * n), m * m + n * n])


def pythagoreanTriplets(i):
    """Generates pythagorean triplets that contain i"""
    from done.Number.primes import factorsOf
    i = int(i)
    # 2mn = i
    # procedure: i is even, pyTrip(factors of i/2)
    if i % 2 == 0:
        for k, j in factorsOf(i / 2): yield pyTrip(j, k)
    # mm-nn = i
    # m-n = k
    # procedure: k<√i,k factor of i,i/k-k is even, pyTrip((i/k-k)/2,(i/k+k)/2)
    for k, j in factorsOf(i):
        if (i / k - k) % 2 == 0: yield pyTrip((i / k + k) / 2, (i / k - k) / 2)


class RangedNumber:
    """
    Object brought about for the need to do (20k-30k) / (100k-150k) and give a result (13%-30%)
    """

    def __new__(cls, lo, hi):
        """basically a fancy pair of numbers with a lo and a hi and does math based on the range"""
        self = super(RangedNumber, cls).__new__(cls)

        self._lo, self._hi = sorted((min(RangedNumber.check_range(lo)),
                                     max(RangedNumber.check_range(hi))))

        return self

    @property
    def lo(self):
        return self._lo

    @property
    def hi(self):
        return self._hi

    @property
    def includes0(self):
        return self.lo <= 0 <= self.hi

    def __eq__(self, other):
        lo, hi = RangedNumber.check_range(other)
        return self.lo == lo and self.hi == hi

    def __str__(self):
        return f"({self.lo!s} <-> {self.hi!s})"

    def __repr__(self):
        return f"RangedNumber({self.lo!r},{self.hi!r})"

    def __abs__(self):
        if self.includes0:
            return RangedNumber(0, max(-self.lo, self.hi))
        return RangedNumber(abs(self.lo), abs(self.hi))

    def __neg__(self):
        return RangedNumber(-self.lo, -self.hi)

    @staticmethod
    def check_range(numeric):
        """call when you're not sure if the input is RangedNumber or another Number"""
        if hasattr(numeric, 'lo') and hasattr(numeric, 'hi'):
            # if it quacks like a duck, then it is
            return numeric.lo, numeric.hi
        else:
            return numeric, numeric

    @staticmethod
    def fourwaymath(op, alo, ahi, blo, bhi):
        if blo == bhi:
            return RangedNumber.create_fromsort(op(alo, blo), op(ahi, blo))
        return RangedNumber.create_fromsort(op(alo, blo), op(alo, bhi), op(ahi, blo), op(ahi, bhi))

    @staticmethod
    def create_fromsort(*args):
        if len(args) == 1:
            args = args[0]

        if len(args) > 1:
            x = sorted(args)
        else:
            raise ValueError("Nothing to sort")

        return RangedNumber(x[0], x[-1])

    @staticmethod
    def generate_division(op, doc=None):
        def fr(other, self):
            lo, hi = RangedNumber.check_range(other)
            if lo <= 0 <= hi:
                raise ZeroDivisionError()
            return RangedNumber.fourwaymath(op, *RangedNumber.check_range(self), lo, hi)

        def ff(self, other):
            lo, hi = RangedNumber.check_range(other)
            if lo <= 0 <= hi:
                raise ZeroDivisionError()
            return RangedNumber.fourwaymath(op, *RangedNumber.check_range(self), lo, hi)

        fr.__doc__ = ff.__doc__ = doc
        ff.__name__ = f"__{op.__name__}__"
        fr.__name__ = f"__r{op.__name__}__"
        return ff, fr

    @staticmethod
    def generate_dyadic(op, doc=None):
        def fr(other, self):
            return RangedNumber.fourwaymath(op, *RangedNumber.check_range(self), *RangedNumber.check_range(other))

        def ff(self, other):
            return RangedNumber.fourwaymath(op, *RangedNumber.check_range(self), *RangedNumber.check_range(other))

        fr.__doc__ = ff.__doc__ = doc
        ff.__name__ = f"__{op.__name__}__"
        fr.__name__ = f"__r{op.__name__}__"
        return ff, fr


RangedNumber.__truediv__, RangedNumber.__rtruediv__ = RangedNumber.generate_division(operator.truediv)
RangedNumber.__floordiv__, RangedNumber.__rfloordiv__ = RangedNumber.generate_division(operator.floordiv)
RangedNumber.__add__, RangedNumber.__radd__ = RangedNumber.generate_dyadic(operator.add)
RangedNumber.__sub__, RangedNumber.__rsub__ = RangedNumber.generate_dyadic(operator.sub)
RangedNumber.__mul__, RangedNumber.__rmul__ = RangedNumber.generate_dyadic(operator.mul)
RangedNumber.__pow__, RangedNumber.__rpow__ = RangedNumber.generate_dyadic(operator.pow)
