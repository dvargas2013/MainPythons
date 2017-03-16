'''Deals with lists of information. Many probability things are found here.'''

from done.Math import fact as F,comb as C
from math import e,cos,pi
def poisson(y, x):
    """calculate the poisson probability given mean rate and successes"""
    if type(x)==list:
        return round(sum(poisson(y,i) for i in x),4)
    return round(e**-y * y**x / F(x),4)
def Dev(lis,population=False):
    """Sample Standard Deviation"""
    xbar=mean(lis)
    print('x%s = %s'%(chr(773),xbar))
    sumSqDev=sum(x*x for x in lis)-sum(x for x in lis)**2/len(lis)
    print("(x-x%s)^2 = %s"%(chr(773),sumSqDev))
    var=sumSqDev/(len(lis)-(not population))
    print("Variance: %s"%var)
    return var**.5
def freqDev(mid_freq):
    "Sample standard deviation with frequencies defined in a matrix form"
    n=sum(mid_freq.values())
    print("n = %s"%n)
    x2=sum(j*i*i for i,j in mid_freq.items())
    print("f*x^2 = %s"%x2)
    x=sum(j*i for i,j in mid_freq.items())
    print("f*x = %s"%x)
    x_2=x*x
    print("(f*x)^2 = %s"%x_2)
    var=(x2-x_2/n)/(n-1)
    print("Variance: %s"%var)
    return var**.5
def probDev(x_px):
    "Sample standard deviation with probabilities defined in matrix form"
    xbar=sum(i*j for i,j in x_px.items())
    print('x%s = %s'%(chr(773),xbar))
    var=sum((i-xbar)**2*j for i,j in x_px.items()) #sum(j*i*i for i,j in x_px.items())-sum(j*i for i,j in x_px.items())**2
    print("Variance: %s"%var)
    dev=var**.5
    return dev
def hypergeometric(k, N, n, x):
    "Hypergeometric probability given starting choice total, total, tests to run, and successes"
    if k<=N and n<=N:
        if type(x)==list: return round(sum(hypergeometric(k,N,n,i) for i in x),5)
        elif x<=k and x<=n and x<=N: return round(C(k,x) * C(N-k,n-x) / C(N,n),5)
    return 0
def median(lis):
    "Calculate the median of the list given"
    a=(len(lis)+1)//2
    lis.sort()
    return (lis[a-1]+lis[-a])/2
def gcd(lis):
    "Calculate the greatest common divisor of list given"
    a=lis[0]
    for b in lis[1:]: 
        while b: a,b = b,a%b
    return a 
def lcm(lis):
    "Calculate the least common multiple of list given"
    a=1
    for i in lis: a*=i
    b=a/gcd(lis)**(len(lis)-1)
    if int(b)==b: return int(b)
    return b
def show(lis, fast=True, File=None, openType='w'):
    "Display content of List, File=False returns String, Fast=None Pauses"
    if File == None:
        if fast == True: print(show(lis, File=False))
        elif fast==None:
            for i in lis: input(i)
        else:
            for i in lis: print(i)
    elif File == False: return '\n'.join(str(i) for i in lis)
    else:
        with open(File, openType) as f: f.write(show(lis,File=False))
def cross(A,B,tupled=False):
    ""
    # TODO can be done with creative zip(). if want
    if not tupled: return [a+b for a in A for b in B]
    if type(A[0])==tuple: return [a+(b,) for a in A for b in B]
    return [(a,)+(b,) for a in A for b in B]
def combine(*lists, tupled=False):
    oldlis=lists[0]
    for lis in lists[1:]: oldlis=cross(oldlis,lis,tupled)
    return oldlis

def dct(X):
    new = [];    N = len(X);    pin = pi/N;    N2 = 2/N
    return [ round(N2*sum( X[i]*cos( pin*(i+.5)*k ) for i in range(N) ), 9) for k in range(N) ]
def idct(X):
    new = [];    N = len(X);    pin = pi/N;    org = .5*X[0]
    return [ int(round( org + sum( X[i]*cos( pin*i*(k+.5) ) for i in range(1,N) ), 0)) for k in range(N) ]