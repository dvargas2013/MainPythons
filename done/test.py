#!/usr/bin/env python3

""" Tests for the Done Files
Just in case some random edit Breaks something one day
"""
from contextlib import contextmanager
from contextlib import redirect_stdout
from io import StringIO


def notequal_ignore_spaces(str1, str2): return ''.join(str1.split()) != ''.join(str2.split())


def notequal_ignore_capital(str1, str2): return str1.lower() != str2.lower()


def inversable(func, s, invr=None, ne=str.__ne__, name=""):
    if not name: name = func.__name__
    if not invr: invr = func  # if not defined function is its own inverse
    try:
        a = func(s)
    except Exception as e:
        print("%s Failed: Function throws Error: " % name)
        print("\tInput:", s)
        print("\t", e)
        return 0
    try:
        b = invr(a)
    except Exception as e:
        print("%s Failed: Inverse throws Error: " % name)
        print("\tInput:", s)
        print("\tOutput:", a)
        print("\t", e)
        return 0
    if ne(s, b):
        print("%s Failed: Not Equal" % name)
        print("\tInput: %s" % s)
        print("\tOutput: %s" % a)
        print("\tInverse Output: %s" % b)
        return 0
    return 1


def Codes_test():
    from . import Codes
    from random import sample

    succ = 1

    from random import randint

    string_pool = "1234 567890 qwertyuio pasdfghjklz xcvbnm QWERTYU IOPASD FGHJKLZX CVBNM"

    for i in range(100):
        # No double spaces pls
        s = ' '.join(''.join(sample(string_pool, len(string_pool) // 2)).split())

        succ &= inversable(Codes.crosc, s)
        succ &= inversable(Codes.craziness, s)

        succ &= inversable(Codes.binary, s,
                           invr=lambda x: Codes.binary(x, to_binary=0))

        succ &= inversable(Codes.numword, s,
                           invr=lambda x: Codes.numword(x, backToWords=1),
                           ne=notequal_ignore_capital)

        succ &= inversable(Codes.eggnog, s,
                           ne=notequal_ignore_spaces)

        succ &= inversable(Codes.morse, s,
                           invr=Codes.anti_morse,
                           ne=notequal_ignore_capital)

        d = randint(0, 50)
        succ &= inversable(lambda x: Codes.cypher(x, d), s,
                           lambda x: Codes.cypher(x, -d),
                           name='Codes.cypher')

    print("Codes.py " + ("Passed" if succ else "did not Pass"))


def File_test():
    from . import File
    succ = 1
    if not File.exists(File.getHome()):
        succ = 0
        print("Desktop doesn't exist?")
    # TODO how to test done.File

    print("File.py " + ("Passed" if succ else "did not Pass"))


@contextmanager
def redirect_stdin(stringio):
    import sys
    save = sys.stdin
    sys.stdin = stringio
    try:
        yield
    finally:
        sys.stdin = save


def GameTester(func, send="giveup\ngiveup\n15\n12\n"):
    succ = 1

    with redirect_stdin(StringIO(send)):
        with redirect_stdout(StringIO()):
            try:
                func()
            except Exception as e:
                succ = 0
                output = "%s doesnt work. Exception: %s" % (
                    func.__name__, str(e))

    if not succ: print(output)

    return succ


def Game_test():
    from . import Game
    succ = 1

    succ &= GameTester(Game.multiplication)
    succ &= GameTester(Game.pattern)
    succ &= GameTester(Game.physics)
    succ &= GameTester(Game.thinker)
    succ &= GameTester(Game.number_guesser1, send="3\n4\n")
    succ &= GameTester(Game.zombie, "1\n1\n1\n1\n1\n2\n2\n1\n3\n1\n")
    succ &= GameTester(Game.ultimate_rps(), "nat\nhot\nmet\nqui\n")
    succ &= GameTester(Game.murder, "q\n")

    print("Game.py " + ("Passed" if succ else "did not Pass"))


def List_test():
    from . import List
    from random import randint
    succ = 1

    # TODO poisson, Dev, freqDev, probDev, hypergeometric
    for j in range(50):
        lis = [randint(-100, 100)]
        for i in range(9):
            lis.append(randint(-100, 100))
            lis.append(2 * lis[0] - lis[-1])
        if lis[0] != List.median(lis):
            succ = 0
            print("List.median Failed:")
            print("Input: %s" % lis)
            print('Output: %s' % List.median(lis))

    # TODO gcd,lcm,show,cross

    print("List.py " + ("Passed" if succ else "did not Pass"))


def Math_test():
    # import done.Math as Math
    # succ = 1

    # TODO angle, angleForStar, nomial/polynom, BitString, factorial, permutation, combination

    # print("Math.py "+("Passed" if succ else "did not Pass"))
    pass


def Number_test():
    # import done.Number as Number
    # succ = 1

    # TODO done.Number testing

    # print("Number.py "+("Passed" if succ else "did not Pass"))
    pass


def Solver_test():
    from . import Solver
    from random import randint, sample
    from .List import lcm
    succ = 1

    # TODO solve, sudoku

    for j in range(50):
        giveup = randint(10, 99)
        lis = sample([2, 3, 5, 7, 11], 3)
        lis.sort()
        li = list(range(len(lis)))
        for i in range(3): li[i] = giveup % lis[i]
        n = lcm(lis)
        giveup %= n
        n = Solver.numRemainders(lis, li)
        if giveup not in n:
            succ = 0
            print("Solver.numRemainder Failed:")
            print("\tInput: %s,%s" % (lis, li))
            print("\tOutput: %s" % n)
            print("\tActual Output: %s" % giveup)

    # TODO respart, addOrSub

    print("Solver.py " + ("Passed" if succ else "did not Pass"))


def String_test():
    # import done.String as String
    # succ = 1

    # TODO done.String testing

    # print("String.py "+("Passed" if succ else "did not Pass"))
    pass


def Time_test():
    from .Time import Time
    succ = 1

    succ &= (Time(8).hr == 8)
    succ &= (Time(8, 8).mn == 8)
    succ &= (Time(8, 8, 8).sc == 8)
    succ &= (Time(minute=8).mn == 8)
    succ &= (Time(8, pm=True).hr == 20)
    succ &= (Time(16, 8, 8) == Time(8, 8, 8) + Time(8))
    succ &= (Time(20) + Time(5) == Time(1))
    succ &= (Time(20) + Time(5) > Time(1))
    succ &= ((Time(1) > Time(1)) is False)

    # TODO DayOfTheWeek, stopwatch, countdown

    print("Time.py " + ("Passed" if succ else "did not Pass"))


def main():
    for test in [String_test, Codes_test, File_test, Game_test,
                 List_test, Math_test, Number_test,
                 Solver_test, Time_test]:
        try:
            test()
        except: pass


if __name__ == '__main__':
    main()
