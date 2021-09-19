import pytest
from done import Number


def test_parsenum():
    assert Number.parse_number("1") == 1
    assert Number.parse_number("", onerror=9) == 9
    assert Number.parse_number("0", onerror=4) == 0
    assert Number.parse_number(4.3) == 4.3
    assert type(Number.parse_number(4.3)) == float
    assert Number.parse_number(4) == 4
    assert type(Number.parse_number(4)) == int
    assert Number.parse_number(4.0) == 4
    assert type(Number.parse_number(4.0)) == int


def test_getrepeat():
    assert Number.get_repeat(1, 7) == '142857'
    assert Number.get_repeat(1, 3) == '3'
    assert Number.get_repeat(2, 3) == '6'


def test_isPrime():
    Ps = {2, 3, 5, 7, 11, 13}
    for i in range(16):
        assert Number.isPrime(i) == (i in Ps)


def test_nextPrime():
    Ps = [2, 2, 2, 3, 5, 5, 7, 7, 11, 11, 11, 11, 13, 13, 17, 17, 17, 17]
    for i, p in enumerate(Ps):
        assert Number.nextPrime(i) == p


def test_primeGen():
    assert list(Number.primeGen(2, 11)) == [3, 5, 7, 11]


def test_primify():
    assert tuple(Number.primify(15)) == ((3, 1), (5, 1))


def test_totient():
    assert Number.totient(400) == 160
    assert Number.totient(529) == 506
    assert Number.totient(29791) == 28830

    for p in Number.primeGen(6, 25):
        assert Number.totient(p) == p - 1
        for k in range(1, 6):
            assert Number.totient(p ** k) == (p - 1) * p ** (k - 1)


def test_BaseChanger():
    assert Number.BaseChanger(144).to_base(16) == [9, 0]
    assert Number.BaseChanger.fromList([9, 1], 16) == 145
    assert Number.BaseChanger.fromList([1, 0, 0, 1, 0, 0, 0], 2) == 72
    assert Number.BaseChanger(6).to_base(2) == [1, 1, 0]
    assert Number.BaseChanger.fromList([2, 0], 3).to_base(2) == [1, 1, 0]


def test_radtofrac():
    assert Number.radToFrac(2) == [1, 2]
    assert Number.radToFrac(3) == [1, 1, 2]
    assert Number.radToFrac(5) == [2, 4]
    assert Number.radToFrac(7) == [2, 1, 1, 1, 4]


def test_pi():
    PI = "3.141592653589793238462643383279502884197169399375105820974944592307816406286"
    assert Number.PI(len(PI) - 1).to_eng_string() == PI


def test_numtostr():
    assert Number.NumToStr(5) == "Five"
    assert Number.NumToStr(10) == "Ten"
    assert Number.NumToStr(11) == "Eleven"
    assert Number.NumToStr(52) == "Fifty Two"
    assert Number.NumToStr(683) == "Six Hundred Eighty Three"
    assert Number.NumToStr(914_712) == "Nine Hundred Fourteen Thousand Seven Hundred Twelve"
    assert Number.NumToStr(8_000_001) == "Eight Million One"


def test_rangedNumber():
    x = Number.RangedNumber(30, -20)
    assert x.lo == -20 and x.hi == 30
    assert x.includes0
    assert x == Number.RangedNumber(-20, 30)

    x = abs(x)
    assert x.lo == 0 and x.hi == 30
    assert x.includes0

    x = Number.RangedNumber(2, 3) * 10
    assert (x - 25).includes0

    y = Number.RangedNumber(10, 15)
    w = (x - y)
    assert w.lo == 5  # 20-15
    assert w.hi == 20  # 30-10

    w = y
    y *= 10
    assert w.lo != y.lo
    assert w.hi != y.hi

    assert x / y == Number.RangedNumber(2 / 15, 0.30)


def test_primalNat_initerrors():
    pytest.raises(ValueError, Number.PrimalNatural, -1)
    pytest.raises(ValueError, Number.PrimalNatural, 0)


def test_primalNat_inits_and_eq():
    nums = [Number.PrimalNatural(4.99),
            Number.PrimalNatural(4),
            Number.PrimalNatural({2: 2}),
            Number.PrimalNatural.from_factors((2, 2)),
            4]
    for i in nums:
        for j in nums:
            assert i == j


def test_primalNat_maths():
    assert Number.PrimalNatural(4) * Number.PrimalNatural(49) == Number.PrimalNatural({2: 2, 7: 2})
    assert Number.PrimalNatural(4) / Number.PrimalNatural(49) == Number.PrimalNatural({2: 2, 7: -2})

    n = Number.PrimalNatural(2) ** 3
    assert isinstance(n, Number.PrimalNatural)
    assert n == 8

    n = pow(Number.PrimalNatural(2), Number.PrimalNatural(3))
    assert isinstance(n, Number.PrimalNatural)
    assert n == 8


def test_primalNat_properties():
    assert Number.PrimalNatural(4).coprime(Number.PrimalNatural(49))
    assert Number.PrimalNatural(4).divisors == [1, 2, 4]

    # divisors of P*P will always be [1, P, P*P]
    assert Number.PrimalNatural(10037 * 10037).divisor_count == 3
