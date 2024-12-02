"""Deals with anything with the human concept of time and dates"""

from contextlib import contextmanager
from datetime import datetime, timedelta
from itertools import islice
from math import ceil
from time import sleep, time as time_now
from timeit import timeit
from typing import Union


class Time:
    """
Time(hour, minute, second, microsecond, pm=False)
"""

    def __init__(self, hour=0, minute=0, second=0, microsecond=0, pm=False):
        if pm:
            hour += 12

        self.innertime = timedelta(
            hours=hour,
            minutes=minute,
            seconds=second,
            microseconds=microsecond)

    @property
    def hr(self):
        return self.innertime.seconds // 3600

    @property
    def mn(self):
        return self.innertime.seconds // 60 % 60

    @property
    def sc(self):
        return self.innertime.seconds % 60 + self.innertime.microseconds / 1e6

    @property
    def secondsSinceMidnight(self):
        return self.innertime.seconds + self.innertime.microseconds / 1e6

    @property
    def hrHandDeg(self):
        return self.secondsSinceMidnight / 120 % 360

    @property
    def mnHandDeg(self):
        return self.secondsSinceMidnight / 10 % 360

    @property
    def scHandDeg(self):
        return self.secondsSinceMidnight * 6 % 360

    @hr.setter
    def hr(self, hours: int):
        self.innertime += timedelta(hours=hours - self.hr)

    @mn.setter
    def mn(self, mins: int):
        self.innertime += timedelta(minutes=mins - self.mn)

    @sc.setter
    def sc(self, secs: float):
        self.innertime += timedelta(seconds=secs - self.sc)

    @hrHandDeg.setter
    def hrHandDeg(self, deg: float):
        self.hr = deg // 30

    @mnHandDeg.setter
    def mnHandDeg(self, deg: float):
        self.mn = deg // 6

    @scHandDeg.setter
    def scHandDeg(self, deg: float):
        self.sc = deg / 6

    # Some math operations for time
    def __add__(self, new: 'Time'):
        return Time.fromTimedelta(self.innertime + new.innertime)

    def __sub__(self, new: 'Time'):
        return Time.fromTimedelta(self.innertime - new.innertime)

    def __mod__(self, new: 'Time'):
        return Time.fromTimedelta(self.innertime % new.innertime)

    def __mul__(self, new: float):
        return Time.fromTimedelta(self.innertime * new)

    __rmul__ = __mul__

    def __truediv__(self, new: Union['Time', float]):
        if hasattr(new, "innertime"):
            return self.innertime / new.innertime
        else:
            return Time.fromTimedelta(self.innertime / new)

    def __floordiv__(self, new: Union['Time', int]):
        if hasattr(new, "innertime"):
            return self.innertime // new.innertime
        else:
            return Time.fromTimedelta(self.innertime // new)

    # Comparisons
    def __lt__(self, new: Union['Time', float]):
        if hasattr(new, "innertime"):
            return self.innertime < new.innertime
        return self.secondsSinceMidnight < new

    def __eq__(self, new: 'Time'):
        return hasattr(new, "secondsSinceMidnight") and self.secondsSinceMidnight == new.secondsSinceMidnight

    # Show the time in a cool way
    def __repr__(self):
        return f"Time({self!s})"

    @staticmethod
    def fromString(string: str):
        pm = False
        if string.endswith("pm"):
            string = string[:-2]
            pm = True
        elif string.endswith("am"):
            string = string[:-2]
        new = string.split(":")
        return Time(*map(float, new), pm=pm)

    @staticmethod
    def fromTimedelta(td: timedelta):
        r = Time(0)
        r.innertime = td
        return r

    def now(self):
        now = datetime.now()
        return Time(hour=now.hour,
                    minute=now.minute,
                    second=now.second,
                    microsecond=now.microsecond)

    def __str__(self):
        hr = self.hr
        p = 'a'
        if hr >= 12:
            hr -= 12
            p = 'p'
        if hr == 0:
            hr = 12

        return f'{hr:02}:{self.mn:02}:{self.sc:06.3f}{p}m'


months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
_mdy_const = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]


def DayOfTheWeek(month, date, year):
    """Calculate the Day of the Week according to month, day, year given."""
    if type(month) == str: month = months.index(month.lower()[:3]) + 1
    abs_year = year - int(month < 3)  # year if month < 3 else year-1
    leap = (1 if month < 3 else -1) + abs_year // 4 - abs_year // 100 + abs_year // 400
    index = 23 * month // 9 + date + year + leap
    return ['Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'Monday', 'Tuesday'][index % 7]


def _mdy_convert(month, date, year):
    LY = year - int(month < 3)
    return LY // 4 - LY // 100 + LY // 400 + 365 * year + date + _mdy_const[month - 1]


def days_between(mdy1, mdy2):
    return _mdy_convert(*mdy2) - _mdy_convert(*mdy1)


def MoonPhase(month, date, year, baseline=(_mdy_convert(1, 6, 2000), 0.00)):
    baseday, basephase = baseline
    days = _mdy_convert(month, date, year) - baseday
    return (days / 29.530588 + basephase) % 1


@contextmanager
def timer(msg=None):
    """print time taken in ms by the block within context.

Usage:

>>> with timer('<Message>'):
>>>     pass

if you do not wish to print and would rather receive the time to handle yourself,
use ``as TARGET`` to get a list of size 1 with a float inside containing the same number as would have been printed

example:

>>> with timer() as time_elapsed:
>>>     pass
>>> print(time_elapsed[0])
    """
    ba = [None]
    start = time_now()
    yield ba
    ba[0] = (time_now() - start) * 1000

    if msg is not None:
        print(f"{msg!s}: {ba[0]:.02f}ms")


def maxtime_computation(generator, online_calculation, maxtime=10, init_n=10_000,
                        unpack_generated=False, unpack_previous=False):
    """Given a max time in seconds will try to generate and compute within that alloted time

generator and online_calculation should be of the form such that
previous = online_calculation()
for i in generator:
   previous = online_calculation(i, previous)

unpack_generated == True: online_calculation(*i, previous)
unpack_previous == True: online_calculation(i, *previous)
    """
    # set up the function to be called as the online calculation
    if unpack_previous and unpack_generated:
        def calc(gn, pv):
            return online_calculation(*gn, *pv)
    elif unpack_generated:
        def calc(gn, pv):
            return online_calculation(*gn, pv)
    elif unpack_previous:
        def calc(gn, pv):
            return online_calculation(gn, *pv)
    else:
        calc = online_calculation

    # time how much time the calculation takes
    with timer() as time:
        p = online_calculation()
        for i in islice(generator, init_n):
            p = calc(i, p)
    time = time[0]

    # calculate how many iterations should be left
    its_per_ms = init_n / time
    ms_left = maxtime * 1000 - time
    its_left = ceil(its_per_ms * ms_left)

    # preform the iterations
    for i in islice(generator, its_left):
        p = calc(i, p)

    # return the value
    return p


def function_time(func_or_str, times=3, initn=10_000, **kwargs):
    """basically a wrapper for timeit.timeit. returns number of times you could run the function in a second"""
    kwargs.pop('number', 0)

    n = initn
    x = timeit(func_or_str, **kwargs, number=n)

    while round(x) != 1:
        n = int(n / x)
        x = timeit(func_or_str, **kwargs, number=n)

    n *= times
    return n / timeit(func_or_str, **kwargs, number=n)


def stopwatch(n=10):
    """Give time SINCE call for {n} Enter Key presses."""
    a = datetime.now()
    for _ in range(n):
        input()
        print(datetime.now() - a)


countUp = stopwatch


def countBetween(n=10):
    """Give time BETWEEN key presses for {n*2} Enter Key presses."""
    for _ in range(n):
        input("[Start]")
        a = datetime.now()
        input("Counting...")
        print(datetime.now() - a)


def countdown(n=10, count=1):
    """Show a countdown on the Terminal starting at {n} counting down by {count}"""
    a = Time() + Time(0, 0, n * count)
    while a > Time():
        print(round((a - Time()) / count, 0), end="\r")
        sleep(count)


def QuickThread(f):
    """run the function in a new Thread (returns the Thread object)"""
    from threading import Thread
    t = Thread(target=f, daemon=True)
    t.start()
    return t
