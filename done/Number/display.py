from done.Number import primes


def simplifyRadical(index, radicand):
    """_(2, 18) = 3*√(2)"""
    loop, test = int((radicand / 2) ** (1 / index)) + 2, .5
    while test != int(test):
        loop -= 1
        test = radicand / loop ** index
    return f'{loop}*√({int(test)})'


def theFactorsOf(integer):
    """_(15) = ['1+15=16', '3+5=8']"""
    return [f'{j}+{k}={j + k}' for j, k in primes.factorsOf(integer)]


def primeFactorize(i):
    """_(15) = ['3^1', '5^1']"""
    return [f"{prime}^{power}" for prime, power in primes.primify(i)]


class BaseChanger(int):
    """Allows for conversion of non-negative integers into other bases"""

    def __new__(cls, integer: int):
        return super(BaseChanger, cls).__new__(cls, abs(int(integer)))

    def to_base(self, base):
        """return a list representing the number"""
        if self in {0, 1}: return [int(self)]
        it = list(self.__baseHelper(base))
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

    def __baseHelper(self, base):
        """yields the numbers in base representation of the number x"""
        x = int(self)
        while x:
            yield x % base
            x //= base

    def __repr__(self):
        return f"BaseChanger({int(self)})"


class NumToStr:
    Ones = ['', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine']
    Teen = ['Ten', 'Eleven', 'Twelve', 'Thir', 'Four', 'Fif', 'Six', 'Seven', 'Eigh', 'Nine']
    for i in range(3, 10): Teen[i] += "teen"
    Tenty = ['', '', 'Twen', 'Thir', 'For', 'Fif', 'Six', 'Seven', 'Eigh', 'Nine']
    for i in range(2, 10): Tenty[i] += "ty"

    @classmethod
    def huns(cls, num):
        def tens(n):
            # rescoping so %= 100 applies to its own variable
            n %= 100
            if 9 < n < 20: return cls.Teen[n % 10]
            if n < 10: return cls.Ones[n % 10]
            return f"{cls.Tenty[n // 10]} {cls.Ones[n % 10]}".strip()

        num %= 1_000
        t = tens(num)

        num //= 100
        if num == 0: return t

        return f"{cls.Ones[num % 10]} Hundred {t}".strip()

    @staticmethod
    def TMB():
        yield ""
        yield " Thousand "
        yield " Million "
        yield " Billion "
        yield " Trillion "

    def __new__(cls, num):
        if num < 0 or num > 999_999_999_999_999:
            return 'Number Out Of Range'
        if num == 0: return 'Zero'

        s = ""
        tmb = cls.TMB()
        while num > 0:
            num, n = divmod(num, 1_000)
            t = next(tmb)
            if n == 0: continue
            s = (cls.huns(n) + t + s).strip()

        return s
