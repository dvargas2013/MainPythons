from random import randint

from done import List


def test_median():
    for j in range(50):
        lis = [randint(-100, 100)]
        for i in range(9):
            lis.append(randint(-100, 100))
            lis.append(2 * lis[0] - lis[-1])
        assert lis[0] == List.median(lis)


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


def test_onlineave():
    psum, pcount = List.online_average()
    assert psum == pcount == 0
    for i in range(1, 100):
        psum, pcount = List.online_average(1, psum, pcount)
        assert psum == pcount == i


def test_gcd():
    assert List.gcd((5, 10)) == 5
    assert List.gcd((5, 10, 25)) == 5
    assert List.gcd((5, 10, 25, 6)) == 1

def test_lcm():
    assert List.lcm((5, 10)) == 10
    assert List.lcm((5, 10, 25)) == 50
    assert List.lcm((5, 10, 25, 6)) == 150

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


def test_poisson():
    # computer breaks an average of once a months
    # probability of it not breaking in a month == math.exp(-1)
    assert List.poisson(1, 0, rounding=5) == 0.36788
    assert List.poisson(1, [1, 2, 3], rounding=5) == sum([0.36788, 0.18394, 0.06131])

    # you receive an average of 3.5 calls a day
    # P(calls <= 4) = 0.72544
    assert List.poisson(3.5, [0, 1, 2, 3, 4], rounding=5) == 0.72544


def test_deviation(capsys):
    assert round(List.Dev([46, 69, 32, 60, 52, 41]), 2) == 13.31
    capsys.readouterr()


def test_freqDev(capsys):
    assert round(List.freqDev({2: 1, 3: 5, 4: 3, 6: 1}), 2) == 1.08
    capsys.readouterr()


def test_probDev(capsys):
    assert round(List.probDev({0: .18, 1: .34, 2: .35, 3: .11, 4: .02}), 4) == 0.9734
    capsys.readouterr()


def test_hypergeometric(capsys):
    # given a bag of 5 red and 3 blue
    # take out 4
    # P(red = blue = 2) = 3/7
    assert round(List.hypergeometric(5, 8, 4, 2), 8) == round(List.hypergeometric(3, 8, 4, 2), 8) == round(3 / 7, 8)
    # P(red >= 2) = 3/7+3/7+1/14 = 13/14
    assert round(List.hypergeometric(5, 8, 4, [2, 3, 4]), 8) == round(13 / 14, 8)
    capsys.readouterr()

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
