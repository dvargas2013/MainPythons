import pytest

from done.Number.accuracy import SigFig
from done.Number.primes import PrimalNatural


def test_parsenum():
    from done.Number import parse_number
    assert parse_number("1") == 1
    assert parse_number("", onerror=9) == 9
    assert parse_number("0", onerror=4) == 0
    assert parse_number(4.3) == 4.3
    assert type(parse_number(4.3)) == float
    assert parse_number(4) == 4
    assert type(parse_number(4)) == int
    assert parse_number(4.0) == 4
    assert type(parse_number(4.0)) == int


def test_division():
    from done.Number.division import get_repeat
    assert get_repeat(1, 7) == '142857'
    assert get_repeat(1, 3) == '3'
    assert get_repeat(2, 3) == '6'


def test_primes():
    from done.Number.primes import isPrime, nextPrime, primeGen, primify

    Ps = {2, 3, 5, 7, 11, 13}
    for i in range(16):
        assert isPrime(i) == (i in Ps)

    Ps = [2, 2, 2, 3, 5, 5, 7, 7, 11, 11, 11, 11, 13, 13, 17, 17, 17, 17]
    for i, p in enumerate(Ps):
        assert nextPrime(i) == p

    assert list(primeGen(2, 11)) == [3, 5, 7, 11]
    assert tuple(primify(15)) == ((3, 1), (5, 1))


def test_totient():
    from done.Number.primes import totient, primeGen

    assert totient(400) == 160
    assert totient(529) == 506
    assert totient(29791) == 28830

    for p in primeGen(6, 25):
        assert totient(p) == p - 1
        for k in range(1, 6):
            assert totient(p ** k) == (p - 1) * p ** (k - 1)


def test_BaseChanger():
    from done.Number.display import BaseChanger

    assert BaseChanger(144).to_base(16) == [9, 0]
    assert BaseChanger.fromList([9, 1], 16) == 145
    assert BaseChanger.fromList([1, 0, 0, 1, 0, 0, 0], 2) == 72
    assert BaseChanger(6).to_base(2) == [1, 1, 0]
    assert BaseChanger.fromList([2, 0], 3).to_base(2) == [1, 1, 0]


def test_radtofrac():
    from done.Number.accuracy import radToFrac

    assert radToFrac(2) == [1, 2]
    assert radToFrac(3) == [1, 1, 2]
    assert radToFrac(5) == [2, 4]
    assert radToFrac(7) == [2, 1, 1, 1, 4]


def test_pi():
    from done.Number.accuracy import PI

    PI_const = "3.141592653589793238462643383279502884197169399375105820974944592307816406286"
    assert PI(len(PI_const) - 1).to_eng_string() == PI_const


def test_numtostr():
    from done.Number.display import NumToStr

    assert NumToStr(5) == "Five"
    assert NumToStr(10) == "Ten"
    assert NumToStr(11) == "Eleven"
    assert NumToStr(52) == "Fifty Two"
    assert NumToStr(683) == "Six Hundred Eighty Three"
    assert NumToStr(914_712) == "Nine Hundred Fourteen Thousand Seven Hundred Twelve"
    assert NumToStr(8_000_001) == "Eight Million One"


def test_rangedNumber():
    from done.Number import RangedNumber

    x = RangedNumber(30, -20)
    assert x.lo == -20 and x.hi == 30
    assert x.includes0
    assert x == RangedNumber(-20, 30)

    x = abs(x)
    assert x.lo == 0 and x.hi == 30
    assert x.includes0

    x = RangedNumber(2, 3) * 10
    assert (x - 25).includes0

    y = RangedNumber(10, 15)
    w = (x - y)
    assert w.lo == 5  # 20-15
    assert w.hi == 20  # 30-10

    w = y
    y *= 10
    assert w.lo != y.lo
    assert w.hi != y.hi

    assert x / y == RangedNumber(2 / 15, 0.30)


def test_primalNat_initerrors():
    pytest.raises(ValueError, PrimalNatural, -1)
    pytest.raises(ValueError, PrimalNatural, 0)


def test_primalNat_inits_and_eq():
    nums = [PrimalNatural(4.99),
            PrimalNatural(4),
            PrimalNatural({2: 2}),
            PrimalNatural.from_factors((2, 2)),
            4]
    for i in nums:
        for j in nums:
            assert i == j


def test_primalNat_maths():
    assert PrimalNatural(4) * PrimalNatural(49) == PrimalNatural({2: 2, 7: 2})
    assert PrimalNatural(4) / PrimalNatural(49) == PrimalNatural({2: 2, 7: -2})

    n = PrimalNatural(2) ** 3
    assert isinstance(n, PrimalNatural)
    assert n == 8

    n = pow(PrimalNatural(2), PrimalNatural(3))
    assert isinstance(n, PrimalNatural)
    assert n == 8


def test_primalNat_properties():
    assert PrimalNatural(4).coprime(PrimalNatural(49))
    assert PrimalNatural(4).divisors == [1, 2, 4]

    # divisors of P*P will always be [1, P, P*P]
    assert PrimalNatural(10037 * 10037).divisor_count == 3


def test_SigFig_precision():
    # All non zero numbers are significant
    assert SigFig("613").precision == 3
    assert SigFig("6.13").precision == 3
    assert SigFig("123456").precision == 6
    assert SigFig("123.456").precision == 6
    # Zeros located between non-zero digits are significant
    assert SigFig("5004").precision == 4
    assert SigFig("602").precision == 3
    # Trailing zeros are significant only if the number contains a decimal
    assert SigFig("5.640").precision == 4
    assert SigFig("120000.0").precision == 7
    assert SigFig("120000.").precision == 6
    assert SigFig("120000").precision == 2
    assert SigFig("1.20e5").precision == 3
    assert SigFig("1.2e5").precision == 2
    # Zeros to left of the first nonzero digit are insignificant
    assert SigFig("0.000456").precision == 3
    assert SigFig("0.052").precision == 2
    assert SigFig("0.0000000000052").precision == 2


def test_SigFig_decimalplaces():
    assert SigFig("613").decimal_places == 0
    assert SigFig("123456").decimal_places == 0
    assert SigFig("5004").decimal_places == 0
    assert SigFig("602").decimal_places == 0

    assert SigFig("6.13").decimal_places == 2
    assert SigFig("123.456").decimal_places == 3
    assert SigFig("5.640").decimal_places == 3

    assert SigFig("0.000456").decimal_places == 6
    assert SigFig("0.052").decimal_places == 3
    assert SigFig("0.0520").decimal_places == 4
    assert SigFig("0.0000000000052").decimal_places == 13

    assert SigFig("120000.").decimal_places == 0
    assert SigFig("120000.0").decimal_places == 1
    assert SigFig("120000").decimal_places == -4
    assert SigFig("1.2e5").decimal_places == -4
    assert SigFig("1.20e5").decimal_places == -3


def test_SigFig_constructorparams():
    assert SigFig(4, decimalplaces=5).decimal_places == 5
    assert SigFig(400, decimalplaces=5).decimal_places == 5

    assert SigFig(4, precision=10).decimal_places == 9
    assert SigFig(400, precision=10).decimal_places == 7

    # decimalplaces is more specific than the precision
    assert SigFig(4, decimalplaces=5, precision=10).decimal_places == 5

    # precision restricts the decimal places
    assert SigFig(400, decimalplaces=5, precision=5).decimal_places == 2


def test_SigFig_math():
    assert SigFig("7.939") + "6.26" + "11.1" == "25.3"  # 25.299
    assert SigFig("27.2") * "15.63" / "1.846" == "230"  # 230.3011918
    assert (SigFig("27") + 3) / SigFig("10.0") == "3.0"
    assert (27 + SigFig(3)) / SigFig("10.0") == "3.0"
