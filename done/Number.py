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