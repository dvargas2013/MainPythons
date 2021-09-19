"""Formulaic, singular number functions are stored here"""

import math
from itertools import zip_longest
from typing import Union, List, Tuple

from done.Number import parse_number


def angle(x1, y1, x2, y2):
    """Calculate the angle made by the two points according to x axis"""
    return math.atan2(y2 - y1, x2 - x1)


def angleForStar(spokes, enturtle=False):
    """Calculate angle to create a nice star"""

    def f():
        """draw a star using a turtle"""
        import turtle
        # Turtle set up
        s = turtle.Screen()
        t = turtle.Turtle()
        # get angle
        a = angleForStar(spokes)
        # preform
        for _ in range(spokes):
            t.fd(100)
            t.rt(a)
        s.exitonclick()
        return a

    if enturtle:
        return f()

    i = next((i for i in range(spokes // 2, spokes) if math.gcd(spokes, i) == 1), default=1)
    return round(360 * i / spokes, 9)


class Polynomial:
    """polynomial class: add, subtract, multiply, divide

    internally represented by a tuple of ints and floats
    in little endian
    so that the constant term is accessed via data[0]
    and the coefficient of x squared via data[2]
    """

    def __init__(self, data: Union[List[int], Tuple[int]] = tuple()):
        if type(data) == str and 'x' in data:
            from warnings import warn
            warn(f"It seems you might want Polynomial.fromString: Polynomial({data})")

        if len(data) == 0:
            self.data = (0,)
            return

        data = list(map(parse_number, data))
        while len(data) > 1 and data[-1] == 0:
            data.pop()

        self.data = data

    def __copy__(self):
        return Polynomial(self.data)

    @staticmethod
    def fromString(in_str):
        to_parse = ''.join(i for i in str(in_str) if i.isalnum() or i in '.+-/*')
        sym = {i for i in to_parse if i.isalpha()}
        if len(sym) == 0: return [parse_number(to_parse)]
        if len(sym) != 1: return []
        sym = sym.pop()
        to_parse = to_parse.replace('-', '+-').replace('-' + sym, '-1' + sym)
        n, p = [], []
        if to_parse[0] == '+': to_parse = '0' + to_parse
        for string in to_parse.rsplit('+'):
            if string[-1] == sym: string += '1'
            if string[0] == sym: string = '1' + string
            if string.find(sym) == -1: string += sym + '0'
            n += [parse_number(string.rsplit(sym)[0])]
            p += [parse_number(string.rsplit(sym)[1])]
        dic = [0] * int(max(p) + 1)
        for pi, ni in zip(p, n): dic[pi] += ni
        return Polynomial(dic)

    def __call__(self, num):
        return sum(coef * num ** power for power, coef in enumerate(self.data))

    def __eq__(self, other):
        return len(self) == len(other) and all(i == j for i, j in zip(self, other))

    def __add__(self, l2):
        return Polynomial([a + b for a, b in zip_longest(self.data, l2, fillvalue=0)])

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
        l3 = [0] * (len(self) + len(l2) - 1)
        for p1, c1 in enumerate(self.data):
            if c1 == 0: continue  # this one is worth checking cause it skips a whole loop
            for p2, c2 in enumerate(l2):
                l3[p1 + p2] += c1 * c2
        return Polynomial(l3)

    def __truediv__(self, s2):
        return str(self // s2) + '+(' + str(self % s2) + ')'

    def _truediv(self, l2):
        num = list(self.data)
        den = list(l2.data)

        if len(num) < len(den):
            return [0, *num]

        # Shift den towards right so it's the same degree as num
        shiftlen = len(num) - len(den)
        den = [0] * shiftlen + den

        quot = []
        divisor = den[-1]
        for i in range(shiftlen + 1):
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
        return "BitString(0x%s)" % format(self.data, 'x')


fact = factorial = math.factorial


def permutation(n, r):
    """Calculate Permutation"""
    if type(n * r) != int or n * r < 0 or r > n: return 0
    import operator
    from functools import reduce
    n += 1
    return reduce(operator.mul, range(n - r, n), 1)


perm = permutation


def combination(n, r):
    """Calculate Combination"""
    if type(n * r) != int or n * r < 0 or r > n: return 0
    r = min(r, n - r)
    return int(perm(n, r) // fact(r))


comb = combination
