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


def count_decimal_places(s_num: str):
    """number of characters after the final period (.)"""
    dot_found = s_num.rfind(".")
    if dot_found < 0:
        return 0
    return len(s_num) - dot_found - 1


def rounds_to(s_num: str):
    """rational approximation with the smallest denominator : given a rounded float as a string"""
    f_num = float(s_num)
    n_digits = count_decimal_places(s_num)
    for deno in range(2, 10 ** (n_digits + 1)):
        numerator = int(f_num * deno)
        if f"{numerator / deno:.{n_digits}f}" == s_num:
            return numerator, deno
        if f"{(numerator + 1) / deno:.{n_digits}f}" == s_num:
            return numerator + 1, deno
