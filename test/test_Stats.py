from done import Stats


def test_median():
    from random import randint
    for j in range(50):
        lis = [randint(-100, 100)]
        for i in range(9):
            lis.append(randint(-100, 100))
            lis.append(2 * lis[0] - lis[-1])
        assert lis[0] == Stats.median(lis)

def test_onlineave():
    psum, pcount = Stats.online_average()
    assert psum == pcount == 0
    for i in range(1, 100):
        psum, pcount = Stats.online_average(1, psum, pcount)
        assert psum == pcount == i

def test_poisson():
    # computer breaks an average of once a months
    # probability of it not breaking in a month == math.exp(-1)
    assert Stats.poisson(1, 0, rounding=5) == 0.36788
    assert Stats.poisson(1, [1, 2, 3], rounding=5) == sum([0.36788, 0.18394, 0.06131])

    # you receive an average of 3.5 calls a day
    # P(calls <= 4) = 0.72544
    assert Stats.poisson(3.5, [0, 1, 2, 3, 4], rounding=5) == 0.72544


def test_deviation(capsys):
    assert round(Stats.Dev([46, 69, 32, 60, 52, 41]), 2) == 13.31
    capsys.readouterr()


def test_freqDev(capsys):
    assert round(Stats.freqDev({2: 1, 3: 5, 4: 3, 6: 1}), 2) == 1.08
    capsys.readouterr()


def test_probDev(capsys):
    assert round(Stats.probDev({0: .18, 1: .34, 2: .35, 3: .11, 4: .02}), 4) == 0.9734
    capsys.readouterr()


def test_hypergeometric(capsys):
    # given a bag of 5 red and 3 blue
    # take out 4
    # P(red = blue = 2) = 3/7
    assert round(Stats.hypergeometric(5, 8, 4, 2), 8) == round(Stats.hypergeometric(3, 8, 4, 2), 8) == round(3 / 7, 8)
    # P(red >= 2) = 3/7+3/7+1/14 = 13/14
    assert round(Stats.hypergeometric(5, 8, 4, [2, 3, 4]), 8) == round(13 / 14, 8)
    capsys.readouterr()
