from done import Math


def test_Polynomial():
    assert Math.Polynomial.fromString("2x2+1")(4) == 2 * 16 + 1
    x = Math.Polynomial.fromString("x")
    assert x * x * [2] + [1] == Math.Polynomial.fromString("2x2+1")
    x1 = Math.Polynomial([1, 1])
    x2 = Math.Polynomial([-1, 1])
    x3 = x1 * x2
    assert x3 // x2 == x1
    assert x3 % x2 == [0]
    assert x3 // x1 == x2
    assert x3 % x1 == [0]
    assert x3(4) == 15
    x4 = x2 * x3
    assert x4 // x2 == x3
    assert x4 % x2 == [0]
    assert x4 // x3 == x2
    assert x4 % x3 == [0]

def test_bitstring():
    b = Math.BitString()
    b.add(5)
    b.add(12)
    assert str(b) == "05.12"
    assert b == Math.BitString(0xc5)


def test_comb_perm_fact():
    assert Math.fact is Math.factorial
    assert Math.perm is Math.permutation
    assert Math.comb is Math.combination
    assert Math.fact(5) == 120
    assert Math.permutation(6, 2) == 30
    assert Math.combination(6, 2) == 15
