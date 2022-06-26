import math

from done.List import product


def factorsOf(i):
    """Finds the factors of i"""
    for k in range(1, int(i ** .5) + 1):
        if i % k == 0: yield k, int(i // k)


def isPrime(n):
    """returns true if n is a prime"""
    if int(n) != n: return False
    if n in {2, 3, 5, 7}: return True
    if n < 2 or n % 2 == 0 or n % 3 == 0: return False

    e = int(n ** .5) + 6
    return all(n % f != 0 and n % (f + 2) != 0 for f in range(5, e, 6))


def nextPrime(i):
    """_(5) = 5, _(15) = 17"""
    i = int(i)
    if i < 3: return 2
    if i < 4: return 3
    i = int(math.ceil(i))
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


def distinctPrimeFactorsOf(i):
    """_(15) = [3,5]"""
    return [prime for prime, _ in primify(i)]


def totient(i):
    """euler's totient"""
    p = distinctPrimeFactorsOf(i)
    y = i / product(p)
    return int(y * product(x - 1 for x in p))


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
            x *= p ** t
        return x

    def __eq__(self, other):
        other = PrimalNatural(other)
        return all(self.pf.get(k, 0) == other.pf.get(k, 0)
                   for k in set(self.pf.keys()).union(other.pf.keys()))

    def coprime(self, other):
        other = PrimalNatural(other)
        return set(self.pf).isdisjoint(other.pf)

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
                return f"{k}"
            elif v == 2:
                return f"{k}*{k}"
            else:
                return f"{k}**{v}"

        return " * ".join(K(k, self.pf[k]) for k in sorted(self.pf))

    @staticmethod
    def from_factors(iterable_of_naturals):
        x = PrimalNatural(1)
        for i in iterable_of_naturals:
            x *= i
        return x
