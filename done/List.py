Info ='''
---List---
Deals with lists of information
Many probability found here

poisson(y, x) - finds poisson probability (mean rate & successes)
Dev(list,population=False) - finds sample or population Deviation
freqDev(x_freq) - same as Dev but freq increases size
probDev(x_Px) - same as freq Dev 
hypergeometric(k, N, n, x) - stats stuff

mean(list) - average of all elements in list
median(list) - center of list when ordered
Range(list) - Maximum - Minumum

gcd(list) - finds gratest common factor of many numbers 
lcm(list) - finds least common multiple of many numbers
show(list) - prints a line for every element of the list given
cross(list1,list2) - combines 2 list (compressing 2d to 1d)
combine(lists) - combines many lists (compression nd to 1d)

dct(int[]) - frequencies yay
idct(float[]) - amplitudal yay
'''
def showInfo():
    from done.String import smartPrint
    smartPrint(Info)

def poisson(y, x):
    "_(mean rate, successes)"
    from done.Math import fact as F
    from math import e
    if type(x)==list:
        return round(sum(poisson(y,i) for i in x),4)
    return round(e**-y * y**x / F(x),4)
def Dev(lis,population=False):
    "Sample Standard Deviation"
    xbar=mean(lis)
    print('x%s = %s'%(chr(773),xbar))
    sumSqDev=sum(x*x for x in lis)-sum(x for x in lis)**2/len(lis)
    print("(x-x%s)^2 = %s"%(chr(773),sumSqDev))
    var=sumSqDev/(len(lis)-(not population))
    print("Variance: %s"%var)
    return var**.5
def freqDev(mid_freq):
    "_({13:5 , 15:10 , 17:5})"
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
    "_({13:.25 , 15:.5 , 17:.25})"
    xbar=sum(i*j for i,j in x_px.items())
    print('x%s = %s'%(chr(773),xbar))
    var=sum((i-xbar)**2*j for i,j in x_px.items()) #sum(j*i*i for i,j in x_px.items())-sum(j*i for i,j in x_px.items())**2
    print("Variance: %s"%var)
    dev=var**.5
    return dev
def hypergeometric(k, N, n, x):
    "_(starting choice total, total, tests to run, successes)"
    from done.Math import comb as C
    if k<=N and n<=N:
        if type(x)==list: return round(sum(hypergeometric(k,N,n,i) for i in x),5)
        elif x<=k and x<=n and x<=N: return round(C(k,x) * C(N-k,n-x) / C(N,n),5)
    return 0
def mean(lis):
    "_([1, 4, 9, 6, 3]) = 4.6"
    return sum(lis)/len(lis)
def Range(lis):
    "_([1, 4, 9, 6, 3]) = 8"
    return max(lis)-min(lis)
def median(lis):
    "_([1, 4, 9, 6, 3]) = 4"
    a=(len(lis)+1)//2
    lis.sort()
    return (lis[a-1]+lis[-a])/2
def gcd(lis):
    "_([8, 12]) = 4"
    a=lis[0]
    for b in lis[1:]: 
        while b: a,b = b,a%b
    return a 
def lcm(lis):
    "_([8, 12]) = 24"
    a=1
    for i in lis: a*=i
    b=a/gcd(lis)**(len(lis)-1)
    if int(b)==b: return int(b)
    return b
def show(lis, fast=True, File=None, openType='w'):
    "Display content of List, File=False returns String, Fast=None Pauses"
    if File == None:
        if fast == True: print(show(lis, File=False))
        elif fast==None: [(print(i),input()) for i in lis]
        else: [print(i) for i in lis]
    elif File == False: return '\n'.join(str(i) for i in lis)
    else: open(File, openType).write(show(lis,File=False))
def cross(A,B,tupled=False):
    if not tupled: return [a+b for a in A for b in B]
    if type(A[0])==tuple: return [a+(b,) for a in A for b in B]
    return [(a,)+(b,) for a in A for b in B]
def combine(*lists, tupled=False):
    oldlis=lists[0]
    for lis in lists[1:]: oldlis=cross(oldlis,lis,tupled)
    return oldlis

def dct(X):
    from math import cos,pi
    new = [];    N = len(X);    pin = pi/N;    N2 = 2/N
    return [ round(N2*sum( X[i]*cos( pin*(i+.5)*k ) for i in range(N) ), 9) for k in range(N) ]
def idct(X):
    from math import cos,pi
    new = [];    N = len(X);    pin = pi/N;    org = .5*X[0]
    return [ int(round( org + sum( X[i]*cos( pin*i*(k+.5) ) for i in range(1,N) ), 0)) for k in range(N) ]