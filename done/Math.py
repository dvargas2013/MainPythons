Info ='''
---Math---
Formulaic, singular number functions are stored here

distanceFormula(x1,y1,x2,y2) - distance formula
angle - together with distance gives polar coord
angleForStar(spokes) - gets number of spokes and gives angle needed

discriminant(a,b,c) - calculates discriminant
quadraticVertex(a,b,c) - finds Vertex or turning point
sumAndProduct(a,b,c) - finds sum and product of roots
quadraticRoots(a,b,c) - finds roots of quadratic

polynom - object representing algebraic functions in string form
nomial - object representing algebraic functions in list form
BitString() - class that is a long. word = len(4bits). init to 0.

fact(num) - factorial (n!)
perm(n,r) - permuation (nPr)
comb(n,r) - combination (nCr)
'''
def showInfo():
    from done.String import smartPrint
    smartPrint(Info)
import math
def angle(x1,y1,x2,y2): return math.atan2(y2-y1,x2-x1)
def distanceFormula(x1,y1,x2,y2):
    "_(0, 0, 3, 4) = 5.0"
    return math.sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1))
def angleForStar(spokes):
    "_(5) = 72.0"
    return round(180*(spokes-2-spokes%2)/spokes,9)
def discriminant(a,b,c):
    "_(1, 2, 1) = 0"
    return b*b-4*a*c
def quadraticVertex(a,b,c):
    "_(1, 2, 1) = [-1.0, 0.0]"
    return [-b/2/a,c-b*b/4/a]
def sumAndProduct(a,b,c):
    "_(1, 2, 1) = [-2.0, 1.0]"
    return [-b/a,c/a]
def quadraticRoots(a,b,c):
    "_(1, 2, 1) = {-1.0}"
    d=math.sqrt(b*b-4*a*c)
    return {(d-b)/2/a,-(d+b)/2/a}

class nomial:
    "polynomial list class: add, substract, multiply, divide"
    #This is basically a list wrapper that can be used to represent polynomials
    def __init__(self,data):
        if type(data)==str or type(data)==polynom: self.data=nomial.lis(data)
        else: self.data=nomial.lis(polynom(data))
    def __call__(self,num): return sum(self[i]*num**(len(self)-1-i) for i in range(len(self)))
    def __add__(l1,l2): return nomial([l1[-i]+l2[-i] for i in range(max(len(l1),len(l2)),0,-1)])
    def __neg__(l1): return nomial([-i for i in l1])
    def __sub__(l1,l2): return l1+-l2
    def __mul__(l1, l2):
        l3=[0 for i in range(len(l1)+len(l2)-1)]
        for a in range(len(l1)):
            for b in range(len(l2)): l3[a+b]+=l1[a]*l2[b]
        return nomial(l3)
    def __truediv__(l1,l2):
        l3,mat=[-i/l2[0] for i in l2],[[0 for i in range(len(l1))] for i in range(len(l2))]
        for x in range(len(l1)):
            for y in range(len(l2)):
                if y+1==len(l2): mat[y][x]=l1[x]+sum([mat[i][x] for i in range(len(l2)-1)])
                elif len(l2)-2<x+y<len(l1): mat[y][x]=mat[len(l2)-1][x+y-len(l2)+1]*l3[len(l3)-1-y]
        return [mat[len(l2)-1][i]/l2[0] for i in range(len(l1))]
    def __floordiv__(l1, l2): return nomial((l1/l2)[:1-len(l2)])
    def __mod__(l1, l2): return nomial((l1/l2)[1-len(l2):])
    def __len__(self): return len(self.data)
    def __repr__(self): return ','.join([str(i) for i in self])
    def __iter__(self):
        for i in range(len(self)): yield self[i]
    def __getitem__(self,i):
        if type(i)==int: return nomial.tryInt(self.data[i])
        if type(i)==slice: return [self[i] for i in range(nomial.tryInt(i.start),nomial.tryInt(i.stop) or len(self),nomial.tryInt(i.step) or 1)]
    def lis(Term):
        "_('4x2+3') = [4, 0, 3]"
        Term=''.join(i for i in str(Term) if i.isalnum() or i in '.+-/*')
        Sym={i for i in Term if i.isalpha()}
        if len(Sym)==0: return [nomial.tryInt(Term)]
        if len(Sym)!=1: return []
        Sym=Sym.pop()
        Term=Term.replace('-','+-').replace('-'+Sym,'-1'+Sym)
        n,p=[],[]
        if Term[0]=='+': Term='0'+Term
        for string in Term.rsplit('+'):
            if string[-1]==Sym: string+='1'
            if string[0]==Sym: string='1'+string
            if string.find(Sym)==-1: string+=Sym+'0'
            n+=[nomial.tryInt(string.rsplit(Sym)[0])]
            p+=[nomial.tryInt(string.rsplit(Sym)[1])]
        dic=dict((i,0) for i in range(int(max(p)+1)))
        for i in range(len(p)): dic[p[i]]+=n[i]
        return [dic[i] for i in range(len(dic)-1,-1,-1)]
    def tryInt(get):
        try:
            get=float(get)
            if get==int(get): get=int(get)
            return get
        except: return 0
class polynom:
    "polynomial string class: add, substract, multiply, divide"
    #This is basically a wrapper for the nomial class
    def __init__(self,data,Sym='x'):
        if type(data)==list or type(data)==nomial: self.data=polynom.term(data)
        else: self.data=polynom.term(nomial(data),Sym)
    def __call__(self,num): return nomial(self)(num)
    def __add__(s1,s2): return polynom(nomial(s1)+nomial(s2))
    def __neg__(s1): return polynom(-nomial(s1))
    def __sub__(s1,s2): return polynom(nomial(s1)-nomial(s2))
    def __mul__(s1,s2): return polynom(nomial(s1)*nomial(s2))
    def __truediv__(s1,s2): return str(s1//s2)+'+('+str(s1%s2)+')'
    def __floordiv__(s1,s2): return polynom(nomial(s1)//nomial(s2))
    def __mod__(s1,s2): return polynom(nomial(s1)%nomial(s2))
    def __repr__(self): return self.data
    def term(Lis,Sym='x'):
        "_([4, 0, 3]) = '4x2+3'"
        ret='+'.join(str(nomial.tryInt(Lis[i]))+Sym+str(len(Lis)-i-1) for i in range(len(Lis)))
        return ret.replace(Sym+'0','').replace(Sym+'1+',Sym+'+').replace('+1'+Sym,'+'+Sym).replace('-1'+Sym,'+'+Sym).replace('+-','-')
    
def fact(num):
    "_(4) = 24"
    if type(num)!=int or num<0: return 0
    ret=1
    for i in range(num): ret*=i+1
    return int(ret)
def perm(n,r):
    "_(4,2) = 12"
    if type(n*r)!=int or n*r<0 or r>n: return 0
    ret=1
    for i in range(n-r,n): ret*=i+1
    return int(ret)
def comb(n,r):
    "_(4,2) = 6"
    if type(n*r)!=int or n*r<0 or r>n: return 0
    r = min(r, n-r)
    return int(perm(n,r)//fact(r))

class BitString():
    def __init__(self):
        self.data = 0
        self.length = 0
    def add(self,num):
        num %= 16
        self.data <<= 4
        self.data +=  num
        self.length += 1
    def get(self,i):
        if i >= self.length or i < 0: i%=self.length
        return (self.data >> (4* (self.length - i - 1))) % 16
    def __iter__(self):
        for i in hex(self.data)[2:].strip('L'):
            yield ord(i)-ord('a')+10 if ord(i)>=ord('a') else int(i)
    def __str__(self): return hex(self.data)[2:].strip('L')
    def __repr__(self):
        return '.'.join(str(i) if i>9 else "0%s"%i for i in self)