from random import sample

import pytest
from done import Codes


def makeCases(howmany=100, string_pool="1234 567890 qwertyuio pasdfghjklz xcvbnm QWERTYU IOPASD FGHJKLZX CVBNM"):
    for i in range(howmany):
        # the splitting and joining is to replace /\s+/g to " "
        yield ' '.join(''.join(sample(string_pool, len(string_pool) // 2)).split())


def equal_ignore_spaces(str1, str2):
    return ''.join(str1.split()) == ''.join(str2.split())


def equal_ignore_capital(str1, str2):
    return str1.lower() == str2.lower()


def eq_str_default(str1, str2):
    return str.__eq__(str1, str2)


def inversable(func, s, invr=None, eq=eq_str_default):
    if not invr: invr = func  # if not defined function is its own inverse
    assert eq(s, invr(func(s)))


def test_Codes_crosc():
    for s in makeCases():
        inversable(Codes.crosc, s)


def test_Codes_craziness():
    for s in makeCases():
        inversable(Codes.craziness, s)


def test_Codes_binary():
    for s in makeCases():
        inversable(Codes.binary, s,
                   invr=lambda x: Codes.binary(x, to_binary=0))


def test_Codes_numword():
    for s in makeCases():
        inversable(Codes.numword, s,
                   invr=lambda x: Codes.numword(x, backToWords=1),
                   eq=equal_ignore_capital)


def test_Codes_eggnog():
    for s in makeCases():
        inversable(Codes.eggnog, s,
                   eq=equal_ignore_spaces)


def test_Codes_morse():
    for s in makeCases():
        inversable(Codes.morse, s,
                   invr=Codes.anti_morse,
                   eq=equal_ignore_capital)

@pytest.mark.parametrize("d", [1, 2, 3, 5, 13, 24, 25])
def test_Codes_cypher(d):
    for s in makeCases():
        inversable(lambda x: Codes.cypher(x, d), s,
                   lambda x: Codes.cypher(x, -d))
