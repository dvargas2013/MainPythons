"""Deals with the things that need solving in the world

Basically if you are tempted to use a brute force algorithm for something it's probably in here.
my pride and joys are the sudoku solver and the 24 game solver.
there are others but they are really obscure problems and puzzles.
"""

from itertools import product
from functools import reduce
from .List import lcm, cross


def __solve_equals_lookup(a, b, lookup, epsilon=1e-6):
    """helper function for solve(). base-case where *nums is empty"""
    if abs(a + b - lookup) < epsilon: return f"{a} + {b}"
    if abs(a - b - lookup) < epsilon: return f"{a} - {b}"
    if abs(b - a - lookup) < epsilon: return f"{b} - {a}"
    if abs(a * b - lookup) < epsilon: return f"{a} * {b}"
    if b != 0 and abs(a - lookup * b) < epsilon: return f"{a} / {b}"
    if a != 0 and abs(b - lookup * a) < epsilon: return f"{b} / {a}"


def __solve_single(a, *nums, lookup, a_string=None):
    """helper function for solve(). recursive helper where u extract a single num"""
    if a_string is None: a_string = str(a)
    if _ := solve(*nums, lookup=lookup - a):
        return f"{a_string} + ({_})"
    if a != 0 and (_ := solve(*nums, lookup=lookup / a)):
        return f"{a_string} * ({_})"
    if _ := solve(*nums, lookup=a - lookup):
        return f"{a_string} - ({_})"
    if _ := solve(*nums, lookup=lookup + a):
        return f"({_}) - {a_string}"
    if lookup != 0 and (_ := solve(*nums, lookup=a / lookup)):
        return f"{a_string} / ({_})"
    if a != 0 and (_ := solve(*nums, lookup=lookup * a)):
        return f"({_}) / {a_string}"


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
    if b != 0 and (_ := __solve_single(a / b, *nums, lookup=lookup, a_string=f"({a} / {b})")):
        return _
    if a != 0 and (_ := __solve_single(b / a, *nums, lookup=lookup, a_string=f"({b} / {a})")):
        return _


def solve(*nums, lookup=24):
    """_(1,2,3,4,lookup=30) yields '3*(2*(4+1))'"""
    if len(nums) == 0:
        raise Exception("im not sure how u did this")

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

    for a, rest in splitter(nums):
        for b, rest1 in splitter(rest):
            if _ := __solve_double(a, b, *rest1, lookup=lookup):
                return _

def cross_str(a,b):
    return [i+j for i in a for j in b]

# These are static vars
sudoku_rows, sudoku_cols = 'ABCDEFGHI', '123456789'
sudoku_squares = cross_str(sudoku_rows, sudoku_cols)  # Every boxy (denoted by s)
sudoku_units = dict((s, [u for u in  # s:[Column, Row, Square] (all three units denoted by u=s[])
                         [cross_str(sudoku_rows, c) for c in sudoku_cols] +
                         [cross_str(r, sudoku_cols) for r in sudoku_rows] +
                         [cross_str(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
                         if s in u]) for s in sudoku_squares)
sudoku_peers = dict((s, set(sum(sudoku_units[s], [])) - {s}) for s in sudoku_squares)  # s:union(u1,u2,u3)
sudoku_values = dict((s, sudoku_cols) for s in sudoku_squares)  # s:'123456789' (denoted by d)


def sudoku(string_grid):
    """solves sudokus"""

    def parse():
        """parse out numbers given in string_grid and adjust values to those numbers by using assign"""
        parse_values = sudoku_values.copy()
        for s, d in dict(zip(sudoku_squares, [c for c in string_grid if c in sudoku_cols + '0.'])).items():
            if d in sudoku_cols and not assign(parse_values, s, d): return 0
        return parse_values

    def assign(v, s, d):
        """in order to put number d in location s of v. eliminate all the other numbers from v[s]"""
        if not all(eliminate(v, s, d2) for d2 in v[s].replace(d, '')):
            return 0  # if elimination failed. it has become an invalid board
        return v

    def eliminate(v, s, d):
        """eliminate d from v[s]. and then check if d has been singled out somewhere"""
        if d not in v[s]: return v  # already eliminated. nothing to do
        v[s] = v[s].replace(d, '')
        if len(v[s]) == 0:
            return 0  # if you eliminated all the numbers . this is now invalid board
        elif len(v[s]) == 1:  # if v[s] only has 1 value: eliminate value from peers.
            if not all(eliminate(v, s2, v[s]) for s2 in sudoku_peers[s]): return 0

        for u in sudoku_units[s]:  # for all lil boxes, see if they're singletons
            d_places = [s for s in u if d in v[s]]
            if len(d_places) == 0:
                return 0
            elif len(d_places) == 1:  # if only 1 more place for d to go, then assign d.
                if not assign(v, d_places[0], d): return 0
        return v

    def search(v):
        """try all possible values. """
        if v == 0: return None
        if all(len(v[s]) == 1 for s in sudoku_squares): return v
        s = min((len(v[s]), s) for s in sudoku_squares if len(v[s]) > 1)[1]  # choose square s with least values
        for d in v[s]:  # it has to be one of those d so pick one and search again
            if _ := search(assign(v.copy(), s, d)):
                return _

    def print_grid():
        """a quick and dirty string accumulator to print out the grid"""
        out = '\n'
        for r, c in sudoku_squares:
            out += values[r + c]
            if c in '36':
                out += '|'
            elif c == '9':
                out += '\n'
                if r in 'CF':
                    out += '-----------\n'
        print(out)

    # Prepare for Ultra-Recursion
    # search() and parse() both call assign() which calls eliminate() which calls assign() and itself
    values = search(parse())
    if not values: return "No Solution for this Grid"
    print_grid()


def numRemainders(divisors, remainders):
    """_(sorted({3,8,3,7}),list([2,4,2])) = 74"""
    divisors = sorted(set(divisors))
    remainders = list(remainders)
    if len(divisors) != len(remainders) or any(r != r % d for d, r in zip(divisors, remainders)): return False
    divisors_lcm = lcm(divisors)
    return reduce(set.intersection, (set(range(r, divisors_lcm, d)) for d, r in zip(divisors, remainders)))


def linear_combination(num, lis, sort=True):
    """yields figures out an array c given an array a such that c0*a0 + c1*a1 + c2*a2 ... = num

_(50, [4, 7]) yields '6*7+2*4'"""
    if sort: lis = [i for i in sorted(lis, reverse=True) if i > 0]
    for i in range(num // lis[0] + 1):
        new = num - i * lis[0]
        if new == 0:
            yield '{}*{}'.format(i, lis[0])
        elif new > 0 and len(lis) > 1:
            for piece in linear_combination(new, lis[1:], False):
                if i == 0:
                    yield piece
                elif i == 1:
                    yield '{} + '.format(lis[0]) + piece
                else:
                    yield '{}*{} + '.format(i, lis[0]) + piece


def addOrSub(string, num):
    """Adds +, -, or nothing between every number and evaluates to num"""
    if not (string.isnumeric() and type(num) == int): return "Why are you here?"
    n = len(string)
    for stry in product('+ -', repeat=n - 1):
        stry += (' ',)
        math = ''.join(string[i] + stry[i] for i in range(n)).replace(' ', '')
        if eval(math) == num: print(stry.count('+') + stry.count('-'), math)
