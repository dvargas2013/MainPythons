from random import randrange, sample

import pytest
from done import Solver


def test_24solve():
    pytest.raises(Exception, Solver.solve)
    pytest.raises(Exception, Solver.solve, 4.2)

    assert Solver.solve(5, lookup=5) == "5"
    assert Solver.solve(6, lookup=5) is None

    # a common fail state is that you try to solve (0 / 0) = lookup cause 0 = lookup * 0
    assert Solver.solve(0, 0, lookup=2) is None
    assert Solver.solve(1, 1, 0, lookup=200) is None

    s = Solver.solve(1, 2, 3, 4, lookup=30)
    assert "1" in s and "2" in s and "3" in s and "4" in s
    assert eval(s) == 30


def test_numRemainders():
    for a in range(3, 6):
        lis = sorted(sample((2, 3, 5, 7, 11, 13), a))
        n = 1
        for i in lis: n *= i

        for _ in range(50):
            giveup = randrange(10, n)
            li = [giveup % i for i in lis]
            assert giveup in Solver.numRemainders(lis, li)


def test_Sudoku():
    pytest.raises(Solver.Sudoku.EliminationError, Solver.Sudoku, "99")
    s = Solver.Sudoku('100920000524017009000000271050008132000102000412703098060009010001036945040071026')
    pytest.raises(Solver.Sudoku.EliminationError, s.solve)
    s = Solver.Sudoku('100920000524017009000000271050008102000102000412700090060009010001036945040071026')
    assert len(list(s.all_solves())) == 1
    s = Solver.Sudoku('001900003905703160030015007050000009004302600200000070600100730042007006500006800')
    assert len(list(s.all_solves())) == 1
    s = Solver.Sudoku('123 456 789'
                      '456 789 123'
                      '789 123 456'
                      '231 564 897'
                      '564 897 231'
                      '897 231 564')
    assert sum(1 for _ in s.all_solves()) == 1728


def test_linearcomb():
    for s in Solver.linear_combination(50, [4, 7]):
        assert eval(s) == 50
    for s in Solver.linear_combination(50, [4, 7], tupled=True):
        for a, b in s:
            assert b in {4, 7}
        assert sum(a * b for a, b in s) == 50
