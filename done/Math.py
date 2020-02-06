"""Formulaic, singular number functions are stored here"""

import math
from Number import parse_number


def angle(x1, y1, x2, y2):
    """Calculate the angle made by the two points according to x axis"""
    return math.atan2(y2 - y1, x2 - x1)


def angleForStar(spokes):
    """Calculate angle to create a star
    
Starts working best for {spokes} > 9.

Example Usage:
    def f(n):
        "draw a star using a turtle"
        import turtle
        # Turtle set up
        s = turtle.Screen()
        t = turtle.Turtle()
        # set angle needed to rotate
        a = angleForStar(n)
        # preform
        for i in range(n*2):
            t.fd(100)
            t.rt(a)
    """
    # TODO the formula doesnt really work. You need to base it on co-primes
    return round(180 * (spokes - 2 - spokes % 2) / spokes, 9)


class Nomial:
    """polynomial list class: add, subtract, multiply, divide"""

    # This is basically a list wrapper that can be used to represent polynomials
    def __init__(self, data):
        if type(data) == str or type(data) == Polynom:
            self.data = Nomial.lis(data)
        else:
            self.data = Nomial.lis(Polynom(data))

    def __call__(self, num):
        return sum(self[i] * num ** (len(self) - 1 - i) for i in range(len(self)))

    def __add__(self, l2):
        return Nomial([self[-i] + l2[-i] for i in range(max(len(self), len(l2)), 0, -1)])

    def __neg__(self):
        return Nomial([-i for i in self])

    def __sub__(self, l2):
        return self + -l2

    def __mul__(self, l2):
        l3 = [0] * (len(self) + len(l2) - 1)
        for a in range(len(self)):
            for b in range(len(l2)): l3[a + b] += self[a] * l2[b]
        return Nomial(l3)

    def __truediv__(self, l2):
        l3 = [-i / l2[0] for i in l2]
        mat = [[0] * len(self)] * len(l2)
        for x in range(len(self)):
            for y in range(len(l2)):
                if y + 1 == len(l2):
                    mat[y][x] = self[x] + sum([mat[i][x] for i in range(len(l2) - 1)])
                elif len(l2) - 2 < x + y < len(self):
                    mat[y][x] = mat[len(l2) - 1][x + y - len(l2) + 1] * l3[len(l3) - 1 - y]
        return [mat[len(l2) - 1][i] / l2[0] for i in range(len(self))]

    def __floordiv__(self, l2):
        return Nomial((self / l2)[:1 - len(l2)])

    def __mod__(self, l2):
        return Nomial((self / l2)[1 - len(l2):])

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return ','.join([str(i) for i in self])

    def __iter__(self):
        for i in range(len(self)): yield self[i]

    def __getitem__(self, i):
        if type(i) == int: return parse_number(self.data[i])
        if type(i) == slice: return [self[i] for i in range(parse_number(i.start), parse_number(i.stop) or len(self),
                                                            parse_number(i.step) or 1)]

    @staticmethod
    def lis(to_parse):
        """_('4x2+3') = [4, 0, 3]"""
        to_parse = ''.join(i for i in str(to_parse) if i.isalnum() or i in '.+-/*')
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
        dic = dict((i, 0) for i in range(int(max(p) + 1)))
        for i in range(len(p)): dic[p[i]] += n[i]
        return [dic[i] for i in range(len(dic) - 1, -1, -1)]


class Polynom:
    """polynomial string class: add, subtract, multiply, divide"""

    # This is basically a wrapper for the nomial class
    def __init__(self, data, sym='x'):
        if type(data) == list or type(data) == Nomial:
            self.data = Polynom.term(data)
        else:
            self.data = Polynom.term(Nomial(data), sym)

    def __call__(self, num):
        return Nomial(self)(num)

    def __add__(self, s2):
        return Polynom(Nomial(self) + Nomial(s2))

    def __neg__(self):
        return Polynom(-Nomial(self))

    def __sub__(self, s2):
        return Polynom(Nomial(self) - Nomial(s2))

    def __mul__(self, s2):
        return Polynom(Nomial(self) * Nomial(s2))

    def __truediv__(self, s2):
        return str(self // s2) + '+(' + str(self % s2) + ')'

    def __floordiv__(self, s2):
        return Polynom(Nomial(self) // Nomial(s2))

    def __mod__(self, s2):
        return Polynom(Nomial(self) % Nomial(s2))

    def __repr__(self):
        return self.data

    @staticmethod
    def term(lis, sym='x'):
        """_([4, 0, 3]) = '4x2+3'"""
        ret = '+'.join(str(parse_number(lis[i])) + sym + str(len(lis) - i - 1) for i in range(len(lis)))
        return ret.replace(sym + '0', '').replace(sym + '1+', sym + '+').replace('+1' + sym, '+' + sym).replace(
            '-1' + sym, '+' + sym).replace('+-', '-')


class BitString:
    """compact hex storage"""

    def __init__(self, ints=None):
        if type(ints) == int:
            self.data = ints
            self.length = math.ceil(ints / 4)
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
    return reduce(operator.mul, range(n - r, n), 1)


perm = permutation


def combination(n, r):
    """Calculate Combination"""
    if type(n * r) != int or n * r < 0 or r > n: return 0
    r = min(r, n - r)
    return int(perm(n, r) // fact(r))


comb = combination
