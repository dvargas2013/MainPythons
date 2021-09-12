from done import List
from random import randint

def test_List_median():
    for j in range(50):
        lis = [randint(-100, 100)]
        for i in range(9):
            lis.append(randint(-100, 100))
            lis.append(2 * lis[0] - lis[-1])
        assert lis[0] == List.median(lis)

# TODO poisson, Dev, freqDev, probDev, hypergeometric
# TODO gcd,lcm,show,cross
