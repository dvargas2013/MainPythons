from random import sample

import pytest
from done.String import Codes


def makeCases(howmany=100, string_pool="1234 567890 qwertyuio pasdfghjklz xcvbnm QWERTYU IOPASD FGHJKLZX CVBNM"):
    for _ in range(howmany):
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


def test_crosc():
    for s in makeCases():
        inversable(Codes.crosc, s)


def test_craziness():
    for s in makeCases():
        inversable(Codes.craziness, s)


def test_binary():
    for s in makeCases():
        inversable(Codes.binary, s,
                   invr=Codes.unbinary)


def test_numword():
    assert Codes.numword is Codes.num_letters
    for s in makeCases():
        inversable(Codes.numword, s,
                   invr=lambda x: Codes.numword(x, backToWords=1),
                   eq=equal_ignore_capital)


def test_eggnog():
    for s in makeCases():
        inversable(Codes.eggnog, s,
                   eq=equal_ignore_spaces)


def test_morse():
    for s in makeCases():
        inversable(Codes.morse, s,
                   invr=Codes.anti_morse,
                   eq=equal_ignore_capital)


@pytest.mark.parametrize("d", [1, 2, 3, 5, 13, 24, 25])
def test_cypher(d):
    for s in makeCases():
        inversable(lambda x: Codes.cypher(x, d), s,
                   lambda x: Codes.cypher(x, -d))


def test_updown():
    for s in makeCases():
        inversable(Codes.updown, s,
                   Codes.downup,
                   eq=equal_ignore_capital)
