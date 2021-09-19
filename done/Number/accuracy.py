import itertools
from decimal import localcontext, Decimal, Context
from fractions import Fraction


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
