"""Deals with lists of information. Many probability things are found here."""

from math import exp, comb, factorial


def poisson(y, x, rounding=4):
    """calculate the poisson probability given mean rate and successes"""
    if type(x) == list:
        return round(sum(poisson(y, i, rounding=rounding * 2) for i in x), rounding)
    return round(exp(-y) * (y ** x) / factorial(x), rounding)


def Dev(lis, population=False):
    """Sample Standard Deviation"""
    xbar = sum(lis) / len(lis)
    print('x%s = %s' % (chr(773), xbar))
    sum_square_deviation = sum(x * x for x in lis) - sum(x for x in lis) ** 2 / len(lis)
    print("(x-x%s)^2 = %s" % (chr(773), sum_square_deviation))
    var = sum_square_deviation / (len(lis) - (not population))
    print("Variance: %s" % var)
    return var ** .5


def freqDev(mid_freq):
    """Sample standard deviation with frequencies defined in a matrix form"""
    n = sum(mid_freq.values())
    print("n = %s" % n)
    x2 = sum(j * i * i for i, j in mid_freq.items())
    print("f*x^2 = %s" % x2)
    x = sum(j * i for i, j in mid_freq.items())
    print("f*x = %s" % x)
    x_2 = x * x
    print("(f*x)^2 = %s" % x_2)
    var = (x2 - x_2 / n) / (n - 1)
    print("Variance: %s" % var)
    return var ** .5


def probDev(x_px):
    """Sample standard deviation with probabilities defined in matrix form"""
    xbar = sum(i * j for i, j in x_px.items())
    print('x%s = %s' % (chr(773), xbar))
    var = sum((i - xbar) ** 2 * j for i, j in
              x_px.items())  # sum(j*i*i for i,j in x_px.items())-sum(j*i for i,j in x_px.items())**2
    print("Variance: %s" % var)
    dev = var ** .5
    return dev


def hypergeometric(start, total, runs, success):
    """Hyper-geometric probability given starting choice, total, tests to run, and successes"""
    if start <= total and runs <= total:
        if type(success) == list:
            return sum(hypergeometric(start, total, runs, i) for i in success)
        elif success <= start and success <= runs and success <= total:
            return comb(start, success) * comb(total - start, runs - success) / comb(total, runs)
    return 0


def online_average(item=0, p_sum=0, p_count=-1):
    """calculate the mean given 1 item at a time. defaults assigned such that online_average() == (0,0)

sample code:
p_sum, p_count = online_average() # 0, 0
for i in range(100):
    p_sum, p_count = online_average(i, p_sum, p_count)

assert p_sum == sum(range(100))
assert p_count == 100
    """
    return p_sum + item, p_count + 1


def median(lis):
    """Calculate the median of the list given"""
    a = (len(lis) + 1) // 2
    lis.sort()
    return (lis[a - 1] + lis[-a]) / 2
