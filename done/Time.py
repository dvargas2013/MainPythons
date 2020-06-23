#!/usr/bin/env python3
"""Deals with anything with the human concept of time and dates"""

from time import sleep, time as time_now
from timeit import timeit
from datetime import datetime
from contextlib import contextmanager
from itertools import islice
from math import ceil

class Time:
    """Instance of time can do many Timely things.

Keeps track of total seconds from midnight to time.

Initialization:

    All of these are equivalent and will initialize with 8 o'clock AM

    Time(8,0,0) - set hours, minutes, seconds
    Time(8,0) - set hours, minutes
    Time(8) - set hours
    Time('8') - set hours from string
    Time('8:0') - set hours, minutes from string
    Time('8:0:0') - set hours, minutes, seconds from string

    Time() - returns an instance with time of creation
"""

    def __init__(self, *time):
        if len(time) == 1:
            if type(time[0]) == str:
                new = time[0].split(":")
            else:
                new = [Time.run(time[0], 0), 0, 0]
        elif len(time) > 1:
            new = [Time.run(i, 0) for i in time[:3]]
        else:
            a = datetime.now()
            new = [a.hour, a.minute, a.second + a.microsecond / 1e6]
        while len(new) < 3: new = list(new) + [0]
        self.sc = float(new[2]) + (float(new[1]) + float(new[0]) * 60) * 60
        self.mn = int(self.sc // 60)  # Get some minutes from it
        self.hr = int(self.mn // 60 % 12)  # Get hours from the minutes gotten
        self.mn = int(self.mn % 60)  # Reduce minutes
        self.sc = round(self.sc % 60, 9)  # Reduce seconds
        # That's the best way I thought of at the moment

    @property
    def totalSc(self):
        """Total amount of seconds from midnight to time"""
        return 60 * (60 * self.hr + self.mn) + self.sc

    @property
    def hrHandDeg(self):
        """Angle between the 12 and position of the hour hand"""
        return (60 * (60 * self.hr + self.mn) + self.sc) / 120 % 360

    @property
    def mnHandDeg(self):
        """Angle between the 12 and position of the minute hand"""
        return (60 * self.mn + self.sc) / 10 % 360

    @property
    def scHandDeg(self):
        """Angle between the 12 and position of the second hand"""
        return self.sc * 6 % 360

    @hrHandDeg.setter
    def hrHandDeg(self, deg):
        """Set the hour hand of time to where it should be according to the angle given in degrees"""
        self.hr = deg // 30

    @mnHandDeg.setter
    def mnHandDeg(self, deg):
        """Set the minute hand of time to where it should be according to the angle given in degrees"""
        self.mn = deg // 6

    @scHandDeg.setter
    def scHandDeg(self, deg):
        """Set the second hand of time to where it should be according to the angle given in degrees"""
        self.sc = deg / 6

    def setHr(self, num):
        """Set the hours of time"""
        new = Time(num, self.mn, self.sc)
        self.hr, self.mn, self.sc = new.hr, new.mn, new.sc

    def setMn(self, num):
        """Set the minutes of time"""
        new = Time(self.hr, num, self.sc)
        self.hr, self.mn, self.sc = new.hr, new.mn, new.sc

    def setSc(self, num):
        """Set the seconds of time"""
        new = Time(self.hr, self.mn, num)
        self.hr, self.mn, self.sc = new.hr, new.mn, new.sc

    # Some math operations for time
    def __add__(self, new):
        return Time(self.hr + new.hr, self.mn + new.mn, self.sc + new.sc)

    def __sub__(self, new):
        return Time(self.hr - new.hr, self.mn - new.mn, self.sc - new.sc)

    def __mul__(self, new):
        return Time(0, 0, self.totalSc * Time.run(new))

    def __truediv__(self, new):
        return Time(0, 0, self.totalSc / Time.run(new))

    def __floordiv__(self, new):
        return Time(0, 0, self.totalSc // Time.run(new))

    def __mod__(self, new):
        new = Time.run(new, None)
        if new is None: return Time(self)
        return Time(0, 0, self.totalSc % new)

    def __round__(self, n=0):
        return Time(self.hr, self.mn, round(self.sc, n))

    # Comparisons
    def __lt__(self, new):
        if hasattr(new, "totalSc"): return self.totalSc < new.totalSc
        return self.totalSc < new

    def __eq__(self, new):
        return hasattr(new, "totalSc") and self.totalSc == new.totalSc

    def __le__(self, new):
        return self < new or self == new

    # Show the time in a cool way
    def __repr__(self):
        return "Time(%s)" % self.__str__()

    def __str__(self):
        return '{:0>2}:{:0>2}:{:0>2}'.format(self.hr, self.mn, self.sc)

    @classmethod
    def run(cls, num, default=1):
        """Convert parameter sent into the total amount of seconds.

Can accept int, float, and Time. Anything else and default is returned"""
        if isinstance(num, cls): return num.totalSc
        if isinstance(num, (int, float)): return num
        return default


def DayOfTheWeek(month, date, year):
    """"Calculate the Day of the Week according to month, day, year given."""
    if type(month) == str: month = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov',
                                    'dec'].index(month.lower()[:3]) + 1
    abs_month = -1 if month < 3 else 1
    abs_year = year - (1 - abs_month) // 2
    index = 23 * month // 9 + date + year - abs_month - 1 + abs_year // 4 - abs_year // 100 + abs_year // 400
    return ['Thursday', 'Friday', 'Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday'][index % 7]


@contextmanager
def timer(msg):
    """print time taken in ms by the block within context.

Usage:

>>> with timer('<Message>'):
>>>     <block>

if you do not wish to print and would rather receive the time to handle yourself,
pass in an object that allows self.__setitem__(0, <float>)

example:

>>> time_elapsed = [0]
>>> with timer(time_elapsed):
>>>     <block>
>>> print(time_elapsed[0])
    """
    start = time_now()
    yield
    end = time_now()

    if hasattr(msg, "__setitem__"):
        try:
            msg[0] = (end - start) * 1000
            return
        except (IndexError, ValueError):
            # if you cant reach [0] or you cant put the float in there
            # just resort to printing it as a string
            pass
    print(f"{msg!s}: {((end - start) * 1000):.02f}ms")


def maxtime_computation(generator, online_calculation, maxtime=10, initn=10_000,
                        unpack_generated=False, unpack_previous=False):
    """Given a max time in seconds will try to generate and compute within that alloted time

generator and online_calculation should be of the form such that
>>> previous = online_calculation()
>>> for i in generator:
>>>    previous = online_calculation(i, previous)

unpack_generated == True
>>> online_calculation(*i, previous)

unpack_previous == True
>>> online_calculation(i, *previous)
    """
    if unpack_previous and unpack_generated:
        calc = lambda gn, pv: online_calculation(*gn, *pv)
    elif unpack_generated:
        calc = lambda gn, pv: online_calculation(*gn, pv)
    elif unpack_previous:
        calc = lambda gn, pv: online_calculation(gn, *pv)
    else:
        calc = online_calculation

    time = [0]
    with timer(time):
        p = online_calculation()
        for i in islice(generator, initn):
            p = calc(i, p)

    time = time[0]

    its_per_ms = initn / time
    ms_left = maxtime * 1000 - time
    its_left = ceil(its_per_ms * ms_left)

    for i in islice(generator, its_left):
        p = calc(i, p)

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
    for i in range(n):
        input()
        print(datetime.now() - a)


countUp = stopwatch


def countBetween(n=10):
    """Give time BETWEEN key presses for {n*2} Enter Key presses."""
    for i in range(n):
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
