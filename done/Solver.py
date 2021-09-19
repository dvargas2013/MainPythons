"""Deals with the things that need solving in the world

Basically if you are tempted to use a brute force algorithm for something it's probably in here.
my pride and joys are the sudoku solver and the 24 game solver.
there are others but they are really obscure problems and puzzles.
"""

from fractions import Fraction
from functools import reduce, lru_cache
from itertools import product
from typing import Union

from done.List import lcm


@lru_cache
def __solve_equals_lookup(a, b, lookup):
    """helper function for solve(). base-case where *nums is empty"""
    if a + b == lookup: return f"{a} + {b}"
    if a - b == lookup: return f"{a} - {b}"
    if b - a == lookup: return f"{b} - {a}"
    if a * b == lookup: return f"{a} * {b}"
    if b != 0 and a == lookup * b: return f"{a} / {b}"
    if a != 0 and b == lookup * a: return f"{b} / {a}"


@lru_cache
def __solve_single(a, *nums, lookup, a_string=None):
    """helper function for solve(). recursive helper where u extract a single num"""
    if a_string is None: a_string = str(a)
    if _ := solve(*nums, lookup=lookup - a):
        return f"{a_string} + ({_})"
    if a != 0 and (_ := solve(*nums, lookup=Fraction(lookup, a))):
        return f"{a_string} * ({_})"
    if _ := solve(*nums, lookup=a - lookup):
        return f"{a_string} - ({_})"
    if _ := solve(*nums, lookup=lookup + a):
        return f"({_}) - {a_string}"
    if a * lookup != 0 and (_ := solve(*nums, lookup=Fraction(a, lookup))):
        return f"{a_string} / ({_})"
    if a != 0 and (_ := solve(*nums, lookup=lookup * a)):
        return f"({_}) / {a_string}"


@lru_cache
def __solve_double(a, b, *nums, lookup):
    """helper function for solve(). """
    if _ := __solve_single(a + b, *nums, lookup=lookup, a_string=f"({a} + {b})"):
        return _
    if _ := __solve_single(a * b, *nums, lookup=lookup, a_string=f"({a} * {b})"):
        return _
    if _ := __solve_single(a - b, *nums, lookup=lookup, a_string=f"({a} - {b})"):
        return _
    if _ := __solve_single(b - a, *nums, lookup=lookup, a_string=f"({b} - {a})"):
        return _
    if b != 0 and (_ := __solve_single(Fraction(a, b), *nums, lookup=lookup, a_string=f"({a} / {b})")):
        return _
    if a != 0 and (_ := __solve_single(Fraction(b, a), *nums, lookup=lookup, a_string=f"({b} / {a})")):
        return _


@lru_cache
def solve(*nums, lookup: Union[Fraction, int] = 24):
    """_(1,2,3,4,lookup=30) yields '3*(2*(4+1))'"""
    if len(nums) == 0: raise Exception("no numbers given")
    if not all((type(i) in [int, Fraction]) for i in [*nums, lookup]):
        # all the inputs must be int or Fraction types
        raise Exception("only integers and Fractions allowed for computation")

    if len(nums) == 1:
        if nums[0] == lookup:
            return str(lookup)
        return
    elif len(nums) == 2:
        return __solve_equals_lookup(nums[0], nums[1], lookup)

    def splitter(num_array):
        """generates a middle element and the two outer ranges"""
        for i in range(len(num_array)):
            yield num_array[i], num_array[:i] + num_array[i + 1:]

    for a, rest in splitter(nums):
        if _ := __solve_single(a, *rest, lookup=lookup):
            return _

        for b, rest1 in splitter(rest):
            if _ := __solve_double(a, b, *rest1, lookup=lookup):
                return _


class Sudoku:
    # Prepare for Ultra-Recursion
    # search() and parse() both call assign()
    # assign() calls eliminate()
    # eliminate() calls assign() and itself

    class EliminationError(Exception):
        """Exception so I could catch specifically things thrown by Sudoku.eliminate"""
        pass

    # 81 squares of the form A1, G4, D9, mapped to 3 lists denoting Column, Row, and 3x3 units
    # every unit has 9 elements including the square itself
    # ex: 'A1': [['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9'],
    #            ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1'],
    #            ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']]
    # set(sum(unit,[])) is 21 elements including the square itself
    units = dict((s0 + s1, [[s0 + i for i in "123456789"],
                            [i + s1 for i in "ABCDEFGHI"],
                            [i + j
                             for i in [a for a in ('ABC', 'DEF', 'GHI') if s0 in a][0]
                             for j in [b for b in ('123', '456', '789') if s1 in b][0]]])
                 for s0 in 'ABCDEFGHI' for s1 in '123456789')

    def __init__(self, string_grid="", blank_character="0"):
        """initializes possibilities (ignores anything thats not 1-9 or the specified blank character)"""
        # d: all 81 boxes matched with the numbers 1-9
        self.values = dict((s, "123456789") for s in Sudoku.units)

        if string_grid:
            self._parse(string_grid, blank_character)

    def _parse(self, string_grid, blank_character):
        """parse out numbers given in string_grid and adjust data by using assign"""
        accept_set = set("123456789" + blank_character)

        for s, d in zip(sorted(Sudoku.units), filter(accept_set.__contains__, string_grid)):
            if '1' <= d <= '9': self.assign(s, d)
        return self

    def assign(self, position, digit_str):
        """eliminate all numbers other than d from position s"""
        for d2 in self.values[position]:
            if d2 != digit_str: self.eliminate(position, d2)
        return self

    def eliminate(self, pos, digit):
        """eliminate d from v[s]. and then check if d has been singled out somewhere"""
        if digit not in self.values[pos]: return self  # already eliminated. nothing to do

        self.values[pos] = self.values[pos].replace(digit, '')
        if self.amntof_vals_at(pos) == 0:
            # eliminated all the numbers
            raise Sudoku.EliminationError(f"No more digits can go at {pos}, eliminated: {digit}")
        if self.amntof_vals_at(pos) == 1:  # only has 1 value left
            peers = set(sum(Sudoku.units[pos], []))
            peers.remove(pos)
            for s2 in peers:  # eliminate value from peers
                self.eliminate(s2, self.values[pos])

        for unit in Sudoku.units[pos]:  # for all units, see if there's a number that only goes in 1 place
            d_places = [p for p in unit if digit in self.values[p]]
            if len(d_places) == 0:
                raise Sudoku.EliminationError(f"No more digit {digit} in unit {unit[0]}-{unit[-1]}, @pos: {pos}")
            if len(d_places) == 1:  # if only 1 more place for d to go, then assign d.
                self.assign(d_places[0], digit)

        return self

    def amntof_vals_at(self, position):
        """amount of values left in the box"""
        return len(self.values[position])

    def search(self, debug=False):
        """try all possible values."""
        if all(self.amntof_vals_at(s) == 1 for s in Sudoku.units):
            yield self
            return

        # choose a square s with least values
        s = min((s for s in Sudoku.units if self.amntof_vals_at(s) > 1),
                key=self.amntof_vals_at)

        for d in self.values[s]:  # it has to be one of those d so pick one and search again
            try:
                yield from self.copy().assign(s, d).search(debug=debug)
            except Sudoku.EliminationError as e:
                if debug: print(e)

        raise Sudoku.EliminationError(f"Reached end of search loop at {s} and no numbers worked {self!r}")

    def solve(self):
        """return new board solve or same board if already solved"""
        return next(self.search())

    def all_solves(self):
        """returns an iterator which if list(self.all_solves()) will give a list of Solved Sudoku objects"""
        _it = self.search()
        while True:
            try:
                yield next(_it)
            except Sudoku.EliminationError:
                return

    def copy(self):
        """create a new sudoku board and copy over the possible values"""
        n = Sudoku()
        n.values = self.values.copy()  # only needs shallow cause strings are immutable
        return n

    def display(self, blank="."):
        """prints out an ok looking grid"""
        print('\n-----------\n'.join(  # between triple rows
            "\n".join(  # between rows
                "|".join(  # between triple columns
                    "".join((d if len(d := self.values[r + c]) == 1 else blank)
                            for c in cs)
                    for cs in ("123", "456", "789"))
                for r in rs)
            for rs in ("ABC", "DEF", "GHI")))

    def __str__(self):
        return "".join((s if len(s) == 1 else f"<{s}>") for s in self)

    def __repr__(self):
        return f"Sudoku({''.join((s if len(s) == 1 else '0') for s in self)!r})"

    def __iter__(self):
        yield from (self.values[rc] for rc in sorted(Sudoku.units))


def numRemainders(divisors, remainders):
    """_(sorted({3,8,3,7}),list([2,4,2])) = {74}"""
    divisors = sorted(set(divisors))
    remainders = list(remainders)
    if len(divisors) != len(remainders) or any(r != r % d for d, r in zip(divisors, remainders)): return False
    divisors_lcm = lcm(divisors)
    return reduce(set.intersection, (set(range(r, divisors_lcm, d)) for d, r in zip(divisors, remainders)))


def linear_combination(num, lis, sort=True, tupled=False):
    """yields strings representing sums of products with elements from given lis
        (n1*lis[0] + n2*lis[1] + n3*lis[2] + ...)
    such that eval(string) would return the desired number

_(50, [4, 7]) yields '6*7+2*4', '2*7+9*4'"""
    if sort: lis = [i for i in sorted(lis, reverse=True) if i > 0]
    first = lis[0]
    for i in reversed(range(num // first + 1)):
        new = num - i * first
        if new == 0:
            yield ((i, first),) if tupled else f'{i}*{first}'
        elif new > 0 and len(lis) > 1:
            for piece in linear_combination(new, lis[1:], False, tupled):
                if i == 0:
                    yield piece
                elif tupled:
                    yield (i, first), *piece
                elif i == 1:
                    yield f'{first} + {piece}'
                else:
                    yield f'{i}*{first} + {piece}'


def addOrSub(string, num):
    """Adds +, -, or nothing between every number and evaluates to num"""
    if not string.isnumeric():
        raise Exception(f"invalid parameter: string {string} contains non-numerics")
    num = abs(int(num))

    n = len(string)
    for stry in product('+ -', repeat=n - 1):
        math = ''.join(s + op for s, op in zip(string, stry + (' ',)))
        if eval(math) == num: print(stry.count('+') + stry.count('-'), math.replace(' ', ''))
