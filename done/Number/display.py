from fractions import Fraction

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
        it.reverse()  # reverses list in place, so you save 1 (one) list creation
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


class DivModChain:
    def __init__(self, *args):
        strings = tuple(i for i in args if isinstance(i, str))
        self.mod_chain = tuple([i for i in args if isinstance(i, int)][::-1])
        lmc1 = len(self.mod_chain) + 1
        if len(strings) < lmc1:
            self.strings = [chr(i) for i in range(65, 65 + lmc1)]
            if strings:
                self.strings[-len(strings):] = strings
        else:
            self.strings = strings

    @staticmethod
    def apply(r, chain):
        for i, c in enumerate(chain):
            p, r[i] = divmod(r[i], c)
            r[i + 1] += p
        return tuple(r[::-1])

    def _normalize(self, units: list[int], shift: int):
        """For when you want to call normalize, but you don't need the error checking"""
        r = [0] * len(self.strings)
        if shift == 0:
            r[-len(units):] = units
        else:
            r[-len(units) - shift:-shift] = units
        return DivModChain.apply(r[::-1], self.mod_chain)

    def units(self, units: int | list[int], unit=None):
        if unit is None:
            unit = self.strings[-1]
        elif unit not in self.strings:
            raise Exception(f"unit not found in strings: {unit!r}")

        if not hasattr(units, "__len__"):
            units = [units]

        shift = len(self.strings) - 1 - self.strings.index(unit)  # if it's the last one, shift is 0
        expected_len = len(self.strings) - shift  # if we need to shift we cant use the last ones
        if len(units) > expected_len:
            raise Exception(f"too many units given ({len(units)}) expecting at most {expected_len}")

        return units, shift

    def normalize(self, units: int | list[int], unit=None):
        units, shift = self.units(units, unit)
        return self._normalize(units, shift)

    def stringify(self, normal):
        return " ".join(f"{n} {s}{'' if n == 1 else 's'}" for n, s in zip(normal, self.strings) if n != 0)


YDHMS = DivModChain("year", 365, "day", 24, "hour", 60, "minute", 60, "second")
WDHMS = DivModChain("week", 7, "day", 24, "hour", 60, "minute", 60, "second")


def ConversionClass(cls):
    attrs = list(filter((lambda k: not k.startswith("_")), cls.__dict__.keys()))
    assert attrs
    from done.List import is_iterable, LagrangeInterpolation as Interpolate

    for i in attrs:
        x = getattr(cls, i)
        if not is_iterable(x): x = [x]
        if len(x) < 2: x.append(0)
        setattr(cls, i, [Fraction(j) if isinstance(j, int) else j for j in x])

    def __init__(self, amount, unit):
        self.amount = amount
        self.converter = self._converters[unit]

    cls.__init__ = __init__

    def identity(_):
        return _

    cls._converters = {i: {j: identity if i == j else Interpolate(getattr(cls, i), getattr(cls, j)) for j in attrs}
                       for i in attrs}

    def rounder(value, rounding=2):
        if rounding is None:
            return value
        return round(float(value), rounding)

    closure = {"cls": cls, "rounder": rounder}
    for i in attrs:
        exec(f"""def {i}(_, *args, **kwargs):
\tif not isinstance(_, cls): return cls(_, {i!r}, *args, **kwargs)
\treturn rounder(_.converter[{i!r}](_.amount), *args, **kwargs)""",
             closure)
        closure[i].__doc__ = f"""this function can be used to:
- initialize: {cls.__qualname__}.{i}([Number])
- convert: {cls.__qualname__}([...]).{i}(rounding)"""
        setattr(cls, i, closure[i])
    return cls


@ConversionClass
class Mass:
    kg = Fraction(1)
    lbs = Fraction("2.204623") * kg  # a kg is 2ish lbs
    oz = 16 * lbs
    grams = 1000 * kg
    grains = 7000 * lbs
    carats = 5 * grams
    ton = lbs / 2000
    metric_ton = kg / 1000


@ConversionClass
class Temp:
    celsius = [-40, 0]
    fahrenheit = [-40, 32]
    k = [_ + Fraction("273.15") for _ in celsius]


@ConversionClass
class Distance:
    miles = 1
    km = Fraction("1.609344")
    meters = 1000 * km
    feet = 5280 * miles
    yards = feet / 3
    inches = 12 * feet
    cm = 100 * meters
    mm = 1000 * meters
