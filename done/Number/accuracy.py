import itertools
import decimal
from decimal import localcontext, Decimal, Context
from fractions import Fraction
from typing import Union


def radToFrac(D):
    """Turns √D into continued fraction
    in the form [a0; a1, a2, ..., ar] where a1 to ar is the period of the Fraction

    _(2) = [1,2]
    _(3) = [1,1,2]
    _(5) = [2,4]
    _(7) = [2,1,1,1,4]
    """
    d = int(D)
    f = int(d ** .5)

    def _():
        yield f
        if f * f == d: return  # length of period is 0 since its a square
        Q = 1
        P = f
        while True:
            Q = int((D - P * P) // Q)
            a = int((f + P) // Q)
            yield a
            if f * 2 == a:
                break
            P = a * Q - P

    return list(_())


def convergentSqrt(D):
    """Yields increasingly accurate numerator and denominator of the number √D

    Uses the Convergent of the Continued Fraction representation of √D

    Usage:
        def F(D):
            for i in _(D):
                if sufficientCondition(i): return i
        def F(D):
            a=_(D)
            for i in range(100): next(a)
            return next(a)

    Note: be careful when D is a square number; the iteration will stop
    """
    f, *a = radToFrac(D := int(D))
    yield f, 1
    if f * f == D: return
    P0, P1 = 1, f
    Q0, Q1 = 0, 1
    for a in itertools.cycle(a):
        P0, P1 = P1, a * P1 + P0
        Q0, Q1 = Q1, a * Q1 + Q0
        yield P1, Q1


def convergents(a, b):
    """Yields the numerator and denominator of the convergents of the Continued Fraction
given by the two sequences of numbers passed in

Yield 1: b(0)
Yield 2: b(0) + a(0)/b(1)
Yield 3: b(0)+a(0)/(b(1) + a(1)/(b(2) ))

Passing in a int will repeat that digit for the portion of the sequence
    _(1,2) becomes 2+1/(2+1/(2+1/(2 ...

Passing a list will start the sequence with the 0th item and repeat the last n-1 items
    _(1,[3,2]) becomes 3+1/(2+1/(2+1/(2 ...

Passing a function will query the function for the n-th item which it should return without fail
    _(1,lambda x: x*x) becomes 0+1/(1+1/(4+1/(9 ...

Usage:
    _(1,[1,2]) will converge to the √2
    _(1,1) will converge on golden ratio
"""

    def number(s):
        """convert any input into a callable"""
        if callable(s): return s
        if type(s) == list:
            k = s[0]
            s = s[1:]
            length = len(s)
            return lambda n: k if n == 0 else s[(n - 1) % length]
        S = int(s)
        return lambda n: S

    a = number(a)
    b = number(b)
    A0, A1 = 1, b(0)
    B0, B1 = 0, 1
    for i in itertools.count(1):
        yield A1, B1
        ai = a(i)
        bi = b(i)
        A0, A1 = A1, bi * A1 + ai * A0
        B0, B1 = B1, bi * B1 + ai * B0


def convergentsE():
    """returns the convergents of euler's number: e"""

    def b(i):
        """e = [2; 1,2,1, 1,4,1, 1,2k,1, ...]"""
        if i == 0: return 2
        if (i - 1) % 3 != 1: return 1
        return 2 * (i + 1) // 3

    yield from convergents(1, b)


def PI(decimals_wanted=10):
    """Calculates pi to the decimal place precision wanted"""

    def pi_df(loops):
        """gets a ratio that approximates pi better and better the higher the input"""
        p, d, n = range(3)  # 0,1,2
        for n0 in range(1, loops):  # 1 2 3 4 ...
            p += Fraction(n, d)
            n *= n0  # 2 2 2*2 2*2*3 ...
            d *= 2 * n0 + 1  # 1 3 3*5 3*5*7 ...
        return p.numerator, p.denominator

    a, b = pi_df(4 * decimals_wanted)
    with localcontext(Context(prec=decimals_wanted)):
        return Decimal(a) / Decimal(b)


class SigFig:
    """
    Follows the rules of significant figures
    1. All non zero numbers are significant
    2. Zeros located between non-zero digits are significant
    3. Trailing zeros are significant only if the number contains a decimal
    4. Zeros to left of the first nonzero digit are insignificant

    Exact Numbers:
    exact counts don't affect sigfigs in calculations
    and are said to have an infinite number of significant figures

    """
    _Inf = float("inf")

    def __new__(cls, value: Union[str, int, 'SigFig', Decimal], exact=False, precision=None, decimalplaces=None):
        self = object.__new__(cls)

        try:
            self.value = Decimal(value)
        except TypeError:
            if hasattr(value, "value"):
                self.value = Decimal(value.value)
            else:
                raise TypeError(f"cant convert from {value!r} to SigFig")

        if decimalplaces is None and precision is None:
            if '.' not in str(value):
                # no decimal . remove trailing zeroes
                self.value = self.value.normalize()
        else:
            if precision is not None:
                # if u are given a precision compute the best one given precision
                dp = precision - self.value.adjusted() - 1
                decimalplaces = dp if decimalplaces is None else min(dp, decimalplaces)

            self.value = self.value.__round__(decimalplaces)

        if exact:
            self.precision = SigFig._Inf
            self.decimal_places = SigFig._Inf
        else:
            self.precision = len(self.value.as_tuple().digits)
            self.decimal_places = self.precision - self.value.adjusted() - 1

        return self

    def __str__(self):
        try:
            return f"{round(self.value, self.decimal_places)}"
        except decimal.InvalidOperation:
            return f"{self.value}"

    def __repr__(self):
        if self.precision == SigFig._Inf:
            return f"SigFig({str(self)!r},exact=True)"
        else:
            return f"SigFig({str(self)!r})"

    def __add__(self, other):
        """addition keeps the number of least precise decimal"""
        if not isinstance(other, self.__class__):
            other = self.__class__(other)
        return SigFig(self.value + other.value, decimalplaces=min(self.decimal_places, other.decimal_places))

    __radd__ = __add__

    def __sub__(self, other):
        """subtraction keeps the number of least precise decimal"""
        if not isinstance(other, self.__class__):
            other = self.__class__(other)
        return SigFig(self.value - other.value, decimalplaces=min(self.decimal_places, other.decimal_places))

    def __rsub__(self, other):
        if not isinstance(other, self.__class__):
            other = self.__class__(other)
        return other - self

    def __mul__(self, other):
        """multiplication keeps the precision of number with the least amount of sigfigs"""
        if not isinstance(other, self.__class__):
            other = self.__class__(other)
        return SigFig(self.value * other.value, precision=min(self.precision, other.precision))

    __rmul__ = __mul__

    def __truediv__(self, other):
        """division keeps the precision of number with the least amount of sigfigs"""
        if not isinstance(other, self.__class__):
            other = self.__class__(other)
        return SigFig(self.value / other.value, precision=min(self.precision, other.precision))

    def __rtruediv__(self, other):
        if not isinstance(other, self.__class__):
            other = self.__class__(other)
        return other / self

    def __neg__(self):
        return SigFig(-self.value, decimalplaces=self.decimalplaces, precision=self.precision)

    def __eq__(self, other):
        if hasattr(other, "value"):
            return self.value == other.value
        return self.value == Decimal(other)

    def __lt__(self, other):
        if hasattr(other, "value"):
            return self.value < other.value
        return self.value < Decimal(other)

    def __le__(self, other):
        if hasattr(other, "value"):
            return self.value <= other.value
        return self.value <= Decimal(other)
