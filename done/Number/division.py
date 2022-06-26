from functools import lru_cache

@lru_cache
def nth_remainder(a, b, n):
    """gives the nth remainder in the long division process of a/b"""
    return (a if n == 0 else 10 * nth_remainder(a, b, n - 1)) % b


# the main idea is that modulo OP
def decimal_length(a, b):
    """gives the length of the pre-sequence and the length of the repeat of the rational a/b"""
    # find a value for u that repeats twice distance away
    u = 1
    v = 2
    while nth_remainder(a, b, u) != nth_remainder(a, b, v):
        u += 1
        v += 2

    # reset v and find where it starts repeating
    v = 0
    while nth_remainder(a, b, u) != nth_remainder(a, b, v):
        v += 1
        u += 1

    # find the length of the repeating segment
    p = v
    v += 1
    while nth_remainder(a, b, u) != nth_remainder(a, b, v):
        v += 1

    return p, v - p


def get_repeat(a, b):
    """finds the repeating decimal portion of the rational a/b"""
    p, q = decimal_length(a, b)
    return "".join(str(10 * nth_remainder(a, b, i) // b) for i in range(p, p + q))
