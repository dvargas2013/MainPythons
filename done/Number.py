#!/usr/bin/env python3

"""Searching functions dealing with singular number space - Prioritized for human readability"""
from math import ceil
from decimal import Decimal, localcontext, Context
from fractions import Fraction
import itertools
import operator


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


def simplifyRadical(index, radicand):
    """_(2, 18) = 3*√(2)"""
    loop, test = int((radicand / 2) ** (1 / index)) + 2, .5
    while test != int(test):
        loop -= 1
        test = radicand / loop ** index
    return str(loop) + '*√(' + str(int(test)) + ')'


def pyTrip(m, n):
    """Generate a pythagorean triplet using the rule
    (twice the product , difference of squares , sum of squares)
    """
    # when n and m are both odd it is reducible by 2 because mm-nn will be a multiple of 4
    # if n and m have a cofactor . should be kinda obvious that it will be reducible by the cofactor
    return sorted([2 * m * n, abs(m * m - n * n), m * m + n * n])


def pythagoreanTriplets(i):
    """Generates pythagorean triplets that contain i"""
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


def factorsOf(i):
    """Finds the factors of i"""
    for k in range(1, int(i ** .5) + 1):
        if i % k == 0: yield k, int(i // k)


def isPrime(n):
    """returns true if n is a prime"""
    if int(n) != n: return False
    if n == 2 or n == 3: return True
    if n < 2 or n % 2 == 0: return False
    if n < 9: return True
    if n % 3 == 0: return False
    e = int(n ** .5) + 6
    for f in range(5, e, 6):
        if n % f == 0 or n % (f + 2) == 0: return False
    return True


def nextPrime(i):
    """_(5) = 5, _(15) = 17"""
    i = int(i)
    if i < 2: return 2
    if i < 3: return 3
    i = int(ceil(i))
    if i % 2 == 0: i += 1
    while not isPrime(i): i += 2
    return i


def primeGen(a, b):
    """_(2,11) = 3, 5, 7, 11"""
    while a < b:
        a = nextPrime(a + 1)
        yield a


def primify(i):
    """_(15) = ...(3,1), (5,1)"""
    i = int(i)
    prime = 0
    while i != 1:
        prime = nextPrime(prime + 1)
        if i < prime * prime: prime = i
        power = 0
        while i % prime == 0:
            power += 1
            i //= prime
        i = int(i)
        if power > 0:
            yield prime, power


def primeFactorize(i):
    """_(15) = ['3^1', '5^1']"""
    return [f"{prime}^{power}" for prime, power in primify(i)]


def distinctPrimeFactorsOf(i):
    """_(15) = [3,5]"""
    return [prime for prime, _ in primify(i)]


def totient(i):
    """euler's totient"""
    from functools import reduce
    import operator
    p = distinctPrimeFactorsOf(i)
    y = i / reduce(operator.mul, p, 1)
    return int(y * reduce(operator.mul, (x - 1 for x in p), 1))


def theFactorsOf(integer):
    """_(15) = ['1+15=16', '3+5=8']"""
    return ['%s+%s=%s' % (j, k, j + k) for j, k in factorsOf(integer)]


class BaseChanger:
    """Allows for conversion of non-negative integers into other bases"""

    def __init__(self, integer):
        self.value = abs(int(integer))

    def to_base(self, base):
        """return a list representing the number"""
        if self.value in {0, 1}: return [self.value]
        it = list(BaseChanger.__baseHelper(self.value, base))
        it.reverse()  # reverses list in place so you save 1 (one) list creation
        return it

    @staticmethod
    def fromList(digits, base):
        """given a list of numbers and a base will return to a BaseChanger object
_([1,0,1,1], 2) => BaseChanger(11)
"""
        return BaseChanger(sum(BaseChanger.__power(digits, base)))

    @staticmethod
    def __power(iterable, base):
        p = 1
        for n in reversed(iterable):
            yield n * p
            p *= base

    @staticmethod
    def __baseHelper(x, base):
        while x:
            yield x % base
            x //= base


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


def preciseSqrt_babylonian(N, decimals_wanted=100):
    """Gives the sqrt(N) to the appropriate decimal places

from my timeit tests this is 1.1x faster than Decimal.sqrt() don't ask me how
(maybe its cause its operating on N as integer)
"""
    with localcontext(Context(prec=decimals_wanted)):
        num = Decimal(N ** .5)
        while True:
            new_num = (num * num + N) / num / 2
            # TODO this looks like the wrong condition to be checking for, probably explains why its 1.1 times faster
            if new_num == num:
                return num
            else:
                num = new_num


def preciseSqrt(N, decimals_wanted=100):
    """Gives the sqrt(N) to the appropriate decimal places

This is just a proof that convergents work
This method is more than 3 orders of magnitude slower than babylonian method
Use decimal to take sqrt instead (uses newtonian method):
    >>> from decimal import Decimal,getcontext
    >>> getcontext().prec = decimals_wanted
    >>> Decimal(N).sqrt()
"""
    with localcontext(Context(prec=decimals_wanted)):
        csn = convergentSqrt(N)
        old = -1  # im pretty sure nothing will ever think its -1
        new = 0
        for a, b in csn:
            new = Decimal(a) / Decimal(b)
            # TODO: i dunno how much change is visible to indicate accuracy reached
            if abs(old - new) < 10 ** (-2 * decimals_wanted):
                return new
            old = new
        return new


def numToStr(num):
    """valid: 0 to 999"""

    def ones(n=num):
        return ['', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine'][n % 10]

    def hundred_and():
        if num > 99:  # 1XX-9XX
            needAnd = num % 100 != 0  # X01-X99
            return ' Hundred' + (' & ' if needAnd else "")
        return ''

    def huns():
        return ones(num // 100) + hundred_and()

    if num < 0 or num > 999:
        return 'Number Out Of Range'
    elif num == 0:
        return 'Zero'
    elif 9 < num % 100 < 20:
        return huns() + ['Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen',
                         'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen'][num % 10]
    else:
        tens = ['', '', 'Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety'][num % 100 // 10]
        tens += ('-' if num % 100 > 20 and num % 10 != 0 else '')

        return huns() + tens + ones()


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
            if lo <= 0 and 0 <= hi:
                raise ZeroDivisionError()
            return RangedNumber.fourwaymath(op, *RangedNumber.check_range(self), lo, hi)

        def ff(self, other):
            lo, hi = RangedNumber.check_range(other)
            if lo <= 0 and 0 <= hi:
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


class PrimalNatural:
    """Internally represents numbers as prime factorization
    in order to do some more specific operations more optimally"""

    def __new__(cls, obj):
        self = super(PrimalNatural, cls).__new__(cls)

        if issubclass(type(obj), PrimalNatural):
            self.pf = obj.pf  # trust in the immutability
        elif type(obj) is dict:
            self.pf = obj
        else:
            if obj == 0:
                raise ValueError("0 is not a Natural Number")
            elif obj < 0:
                raise ValueError("negatives are not Natural Numbers")
            self.pf = dict(primify(obj))

        return self

    def __mul__(self, other):
        other = PrimalNatural(other)
        return PrimalNatural({k: self.pf.get(k, 0) + other.pf.get(k, 0)
                              for k in set(self.pf.keys()).union(other.pf.keys())})

    def __truediv__(self, other):
        other = PrimalNatural(other)
        return PrimalNatural({k: self.pf.get(k, 0) - other.pf.get(k, 0)
                              for k in set(self.pf.keys()).union(other.pf.keys())})

    def __pow__(self, power, modulo=None):
        if modulo is not None: raise NotImplemented
        p = int(power)
        return PrimalNatural({k: self.pf.get(k, 0) * p for k in self.pf})

    def __int__(self):
        x = 1
        for p, t in self.pf.items():
            x *= p**t
        return x

    @property
    def divisor_count(self):
        x = 1
        for i in self.pf.values():
            x *= i + 1
        return x

    def divisor_generator(self):
        yield from self._divisors(1, tuple(self.pf))

    @property
    def divisors(self):
        return sorted(self._divisors(1, sorted(self.pf)))

    def _divisors(self, curDivisor, arr):
        if not len(arr):
            yield curDivisor
        else:
            prime, arr = arr[0], arr[1:]
            yield from self._divisors(curDivisor, arr)
            for _ in range(self.pf[prime]):
                curDivisor *= prime
                yield from self._divisors(curDivisor, arr)

    def __repr__(self):
        return f"PrimalNatural({self.pf})"

    def __str__(self):
        def K(k, v):
            if v == 1:
                return "%s" % k
            elif v == 2:
                return "%s*%s" % (k, k)
            else:
                return "%s**%s" % (k, v)

        return " * ".join(K(k, self.pf[k]) for k in sorted(self.pf))

    @staticmethod
    def from_factors(iterable_of_naturals):
        x = PrimalNatural(1)
        for i in iterable_of_naturals:
            x *= i
        return x
