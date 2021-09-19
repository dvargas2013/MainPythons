from done import List


def test_isiterable():
    assert List.is_iterable([])
    assert List.is_iterable(tuple())
    assert List.is_iterable(dict())
    assert List.is_iterable(set())
    assert List.is_iterable("")
    assert not List.is_iterable(5)


def test_window():
    for (a1, b1), (a2, b2) in zip(
            List.window("abcd", n=2),
            ("ab", "bc", "cd")):
        assert a1 == a2
        assert b1 == b2


def test_batch():
    for (a1, b1), (a2, b2) in zip(
            List.batch("abcd", n=2),
            ("ab", "cd")):
        assert a1 == a2
        assert b1 == b2


def test_interleave():
    assert ''.join(List.interleave("abc", "d", "ef")) == 'adebcf'


def test_cross():
    assert set(List.cross("ab", "12", sum_func="".join)) == {"a1", "a2", "b1", "b2"}


def test_applytogen():
    @List.applyToGenerator(list)
    def wild(n):
        while n > 0:
            yield n
            n -= 1

    for i in range(10):
        assert wild(i) == list(range(i, 0, -1))


def test_collisiondict_list():
    cd = List.CollisionDictOfLists()
    cd.addItem(1, 2)
    cd.addItem(1, 3)
    cd.addItem(2, 1)
    cd.addItem(2, 1)
    assert cd[1] == [2, 3]
    assert cd[2] == [1, 1]
    assert cd == List.CollisionDictOfLists(((1, 2), (1, 3), (2, 1), (2, 1)))
    assert dict(cd) == {1: [2, 3], 2: [1, 1]}


def test_Polynomial():
    assert List.Polynomial.fromString("2x2+1")(4) == 2 * 16 + 1
    x = List.Polynomial.fromString("x")
    assert x * x * [2] + [1] == List.Polynomial.fromString("2x2+1")
    x1 = List.Polynomial([1, 1])
    x2 = List.Polynomial([-1, 1])
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
    b = List.BitString()
    b.add(5)
    b.add(12)
    assert str(b) == "05.12"
    assert b == List.BitString(0xc5)


def test_collissiondict_set():
    cd = List.CollisionDictOfSets()
    cd.addItem(1, 2)
    cd.addItem(1, 3)
    cd.addItem(2, 1)
    cd.addItem(2, 1)
    assert cd[1] == {2, 3}
    assert cd[2] == {1}
    assert cd == List.CollisionDictOfSets(((1, 2), (1, 3), (2, 1), (2, 1)))
    assert dict(cd) == {1: {2, 3}, 2: {1}}
