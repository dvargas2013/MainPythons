'''Searching functions dealing with singular number space - Prioritized for human readability'''

def simplifyRadical(index,radicand):
    "_(2, 18) = 3*√(2)"
    loop,test=int((radicand/2)**(1/index))+2,.5
    while test!=int(test):
        loop-=1
        test=radicand/loop**index
    return str(loop)+'*√('+str(int(test))+')'
#a=2mn, b=m2−n2, c=m2+n2,
def pythagoreanTriplets(integer):
    "_(3) = [3, 4, 5]; _(5) = [5, 12, 13]"
    if integer%2==1: return [integer,(integer*integer-1)//2,(integer*integer+1)//2]
    else: return [integer,(integer*integer//4-1),(integer*integer//4+1)]
def isPrime(n):
    if int(n) != n: return False
    if n==2 or n==3: return True
    if n<2 or n%2==0: return False
    if n<9: return True
    if n%3==0: return False
    for f in range(5,int(n**.5)+6,6):
        if n%f == 0: return False
        if n%(f+2) == 0: return False
    return True
from math import ceil
def nextPrime(integer):
    "_(5) = 5, _(15) = 17"
    if integer<2: return 2
    if integer<3: return 3
    integer=int(ceil(integer))
    if integer%2==0: integer+=1
    while not isPrime(integer): integer+=2
    return integer
def primeFactorize(integer):
    "_(15) = ['3^1', '5^1']"
    primes,lis=1,[]
    while integer!=1:
        primes=nextPrime(primes+1)
        if integer**.5<primes: primes=integer
        power=0
        while integer%primes==0:
            power+=1
            integer//=primes
        if power>0: lis+=['%s^%s'%(int(primes),power)]
    return lis
def theFactorsOf(integer):
    "_(15) = ['1+15=16', '3+5=8']"
    loop,lis=1,[]
    while loop<int(integer**.5)+1:
        if integer%loop==0: lis+=['%s+%s=%s'%(loop,integer//loop,loop+integer//loop)]
        loop+=1
    return lis
def changeBase(lists,oldbase,newbase):
    "_([1,0,1],2,10) = ([5], 'base', 10)"
    from math import log
    n=len(lists)-1
    summ=sum(lists[loop]*oldbase**(n-loop) for loop in range(n+1))
    stop=int(log(summ,newbase))+1
    list_=[i for i in range(stop)]
    for loop in range(stop):
        n=newbase**(stop-loop-1)
        list_[loop]=summ//n
        summ-=list_[loop]*n
    return list_,'base',newbase
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