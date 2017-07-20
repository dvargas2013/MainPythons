#!/usr/bin/env python3

'''Searching functions dealing with singular number space - Prioritized for human readability'''

from math import ceil
def simplifyRadical(index,radicand):
    "_(2, 18) = 3*√(2)"
    loop,test=int((radicand/2)**(1/index))+2,.5
    while test!=int(test):
        loop-=1
        test=radicand/loop**index
    return str(loop)+'*√('+str(int(test))+')'
def pyTrip(m,n):
    '''Generate a pythagorean triplet using the rule
    (twice the product , difference of squares , sum of squares)
    '''
    # when n and m are both odd it is reducible by 2 because mm-nn will be a multiple of 4
    # if n and m have a cofactor . should be kinda obvious that it will be reducible by the cofactor
    n,m = sorted(int(i) for i in [m,n]) # if n>m: mm-nn < 0 so assert n<m
    return sorted([2*m*n, m*m-n*n, m*m+n*n])
def pythagoreanTriplets(i):
    "Generates pythagorean triplets that contain i"
    i = int(i)
    # 2mn = i
    # procedure: i is even, pyTrip(factors of i/2)
    if i%2==0:
        for k,j in factorsOf(i/2): yield pyTrip(j,k)
    
    # mm-nn = i
    # m-n = k
    # procedure: k<√i,k factor of i,i/k-k is even, pyTrip((i/k-k)/2,(i/k+k)/2)
    for k,j in factorsOf(i):
        if (i/k-k) % 2 == 0: yield pyTrip((i/k+k)/2,(i/k-k)/2)
def factorsOf(i):
    "Finds the factors of i"
    for k in range(1,ceil(i**.5)):
        if i%k == 0: yield k,int(i//k)
def isPrime(n):
    if int(n) != n: return False
    if n==2 or n==3: return True
    if n<2 or n%2==0: return False
    if n<9: return True
    if n%3==0: return False
    e = int(n**.5)+6
    for f in range(5,e,6):
        if n%f == 0 or n%(f+2) == 0: return False
    return True
def nextPrime(i):
    "_(5) = 5, _(15) = 17"
    i = int(i)
    if i<2: return 2
    if i<3: return 3
    i=int(ceil(i))
    if i%2==0: i+=1
    while not isPrime(i): i+=2
    return i
def primeFactorize(i):
    "_(15) = ['3^1', '5^1']"
    i = int(i)
    prime,lis=1,[]
    while i!=1:
        prime=nextPrime(prime+1)
        if i**.5<prime: prime=i
        power=0
        while i%prime==0:
            power+=1
            i//=prime
        i = int(i)
        if power>0: lis.append( '%s^%s'%(prime,power) )
    return lis
def theFactorsOf(integer):
    "_(15) = ['1+15=16', '3+5=8']"
    for j,k in factorsOf(integer): lis.append( '%s+%s=%s'%(j,k,j+k) )
    return lis
class BaseInteger():
    """Manipulates numbers in other bases
    
    _(5)         = 5
    _([5])       = 5
    _([5],10)    = 5
    _([1,0,1],2) = 5
    _(5,2)       = 5
    _(55)        = 55
    _([5,5])     = 55
    """
    def __init__(self, num, base=10):
        if type(base) != int: raise Exception("Base must be an integer")
        if not (type(num) == int or type(num) == list and all(type(i)==int for i in num)):
            raise Exception("Number must be integer or list of integers")
        self.b = base
        if type(num) == list:
            self.r = num
            self.n = toBaseTen(num,base)
        else:
            self.r = fromBaseTen(num,base)
            self.n = num
    def __repr__(self):
        if self.b == 10: return self.n.__repr__()
        else: return "BaseInteger(%s,%s)"%( self.r, self.b )
    def __int__(self): return self.n.__int__()
    def changeBase(self,newbase):
        self.r = changeBase(self.r,self.b,newbase)
        self.b = newbase
from math import log
def changeBase(lists,oldbase,newbase):
    "_([1,0,1],2,10) = [5]"
    summ = toBaseTen(lists,oldbase)
    return fromBaseTen(summ,newbase)
def toBaseTen(lis,oldbase):
    n,p,s = len(lis)-1,1,0
    for i in range(n,-1,-1):
        s += lis[i]*p
        p *= oldbase
    return s
def fromBaseTen(num,newbase):
    stop=int(log(num,newbase))+1
    lis=list(range(stop))
    n = newbase**(stop-1)
    for i in range(stop):
        lis[i]=num//n
        num-=lis[i]*n
        n=int(n//newbase)
    return lis
def radToFrac(D):
    """Turns √D into continued fraction
    in the form [a0; a1, a2, ..., ar] where a1 to ar is the period of the Fraction
    
    _(2) = [1,2]
    _(3) = [1,1,2]
    """
    D = int(D)
    a = [int(D**.5)]
    if a[0]*a[0] == D: return a # length of period is 0 since its a square
    P = [0,a[0]]
    Q = [1,D-a[0]*a[0]]
    a.append( int( (2*a[0]) // Q[-1] ) )
    while a[0]*2 != a[-1]:
        P.append( a[-1]*Q[-1]-P[-1] )
        Q.append( int( (D-P[-1]*P[-1]) // Q[-1] ) )
        a.append( int( (a[0]+P[-1]) // Q[-1] ) )
        P.pop(0); Q.pop(0)
    return a
def convergentSqrt(D):
    """Yields incresingly accurate numerator and denominator of the number √D
    
    Uses the Convergants of the Continued Fraction representation of √D
    
    Usage:
        def F(D):
            for i in _(D):
                if sufficientCondition(i): return i
        def F(D):
            a=_(D)
            for i in range(100): a.send(None)
            return a.send(None)
    
    Note: be careful when D is a square number; the iteration will stop
    """
    D = int(D)
    a0=int(D**.5)
    yield a0,1
    if a0*a0 == D: return
    a = [a0]
    P = [0,a0]
    Q = [1,D-a0*a0]
    a.append( int((2*a0)/Q[-1]) )
    p = [a0,a0*a[1]+1]
    q = [1,a[1]]
    while 1:
        yield p[-1],q[-1]
        P.append( a[-1]*Q[-1]-P[-1] )
        Q.append( int( (D-P[-1]*P[-1]) // Q[-1] ) )
        a.append( int( (a0+P[-1]) // Q[-1] ) )
        p.append( a[-1]*p[-1] + p[-2] )
        q.append( a[-1]*q[-1] + q[-2] )
        # Some cool properties
        # p[n]*q[n-1] - p[n-1]*q[n] = (-1)**(n+1)
        # p[n]*p[n] - D*q[n]*q[n] = (-1)**(n+1)*Q[n+1]
        P.pop(0);Q.pop(0);a.pop(0);p.pop(0);q.pop(0)

#### This will lead to an infinate loop because they are literally the same
#>>> a=convergants(1,radToFrac(5))
#>>> b=convergantSqrt(5)
#>>> while a.send(None) == b.send(None): pass
#### Note: though they are equivalent convergantSqrt does it all directly so it is faster
#### But only marginally!!!

def convergents(a,b):
    """Yields the numerator and denominator of the convergants of the Continued Fraction
given by the two sequences of numbers passed in
    
    Yield 1: b(0)
    Yield 2: b(0) + a(0)/b(1)
    Yield 3: b(0)+a(0)/(b(1) + a(1)/(b(2) ))
    
    Passing in a int will repeat that digit for the portion of the sequence
        _(1,2) becomes 2+1/(2+1/(2+1/(2 ...
    
    Passing a list will start the sequence with the 0th item and repeat the last n-1 items
        _(1,[3,2]) becomes 3+1/(2+1/(2+1/(2 ...
        
    Passing a function will query the function for the n-th item which it should return without fail
        _(1,lambda x: x*x) becomes 0+1/(1+1/(4+1/(9 ...
    
    Usage:
        _(1,[1,2]) will converge to the √2
        _(1,1) will converge on golden ratio
    """
    def number(s):
        if callable(s): return s
        if type(s) == list:
            k = s[0]
            s = s[1:]
            l = len(s)
            return lambda n: k if n==0 else s[(n-1)%l]
        S = int(s)
        return lambda n: S
    a=number(a); b=number(b)
    A = [1,b(0)]; B = [0,1]
    i = 1
    while 1:
        ai = a(i)
        bi = b(i)
        yield A[-1],B[-1]
        A.append( bi*A[-1] + ai*A[-2] )
        B.append( bi*B[-1] + ai*B[-2] )
        A.pop(0); B.pop(0)
        i += 1
def convergentsE():
    def b(i):
        """e = [2; 1,2,1, 1,4,1, 1,2k,1, ...]"""
        if i==0: return 2
        if (i-1)%3 != 1: return 1
        return 2*(i+1)//3
    yield from iterateContinuedFraction(1,b)



def numToStr(num):
    "valid: 0 to 999"
    def ones(num): return ['','One','Two','Three','Four','Five','Six','Seven','Eight','Nine'][num%10]
    def tens(num): return ['','','Twenty','Thirty','Forty','Fifty','Sixty','Seventy','Eighty','Ninety'][num%100//10]+('-' if num%100>20 and num%10!=0 else '')
    def huns(num): return ones(num//100)+(' Hundred & ' if num>99 and num%100!=0 else (' Hundred' if num>99 else ''))
    if num<0 or num>999: return 'Number Out Of Range'
    elif num==0: return 'Zero'
    elif num%100>9 and num%100<20:
        return huns(num)+['Ten','Eleven','Twelve','Thirteen','Fourteen','Fifteen','Sixteen','Seventeen','Eighteen','Nineteen'][num%10]
    else: return huns(num)+tens(num)+ones(num)
def piecewiseMaker(funcstr,slicer):
    "_('2x', ':2') = '((1-abs(x-2)/(x-2))/2)(2x)'"
    if type(slicer)!=str or type(funcstr)!=str or slicer.count(':')!=1: return "Don't play games with me"
    mini,maxi=slicer.split(':')
    if slicer==':': out=""
    elif slicer[0]==':': out="((1-abs(x-%s)/(x-%s))/2)"%(maxi,maxi)
    elif slicer[-1]==':': out="((abs(x-%s)/(x-%s)+1)/2)"%(mini,mini)
    else: out="((1-abs((x-%s)*(x-%s))/((x-%s)*(x-%s)))/2)"%(mini,maxi,mini,maxi)
    out=out.replace('.0)',')').replace('-0.0','').replace('-0','').replace('--','+')      
    return out+'('+funcstr+')'