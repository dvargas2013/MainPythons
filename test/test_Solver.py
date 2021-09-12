from done import Solver
from random import randint, sample
from done.List import lcm


def test_Solver_numRemainders():
    for j in range(50):
        giveup = randint(10, 99)
        lis = sample([2, 3, 5, 7, 11], 3)
        lis.sort()
        li = list(range(len(lis)))
        for i in range(3): li[i] = giveup % lis[i]
        n = lcm(lis)
        giveup %= n
        assert giveup in Solver.numRemainders(lis, li)

# TODO solve, sudoku
# TODO respart, addOrSub
