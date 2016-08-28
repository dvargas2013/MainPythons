'''Deals with the things that need solving in the world

Basically if you are tempted to use a brute force algorithm for something it's probably in here.
my pride and joys are the sudoku solver and the 24 game solver.
there are others but they are really obscure problems and puzzles.
'''

def solve(*Nums,lookup=24):
    "_(1,2,3,4,lookup=30) yields '3*(2*(4+1))'"
    from itertools import permutations,product
    def mather(n):
        if n==1: return set(['.'])
        out = set()
        for x in mather(n-1):
            i = x.find('+')
            while i!=-1:
                out.add(x[:i]+'.+'+x[i:])
                i = x.find('+',i+1)
            out.add(x+'.+')
        return out
    def shrink(level,newOp):
        if type(level)!=str: return level
        def oldOp(lvl):
            count = 0
            for i in lvl:
                if i=='(': count+=1
                if i==')': count-=1
                if count==1 and not i.isdecimal() and i not in '()': return i
            return '%'
        if newOp in '+-' or (oldOp(level) in '*/' and newOp in '*/'): return level[1:-1]
        return level
    def change(nums,ops,s):
        stack,prevOps = [],[]
        for i in s:
            if i=='.': stack.append(nums.pop(0))
            else:
                newOp=ops.pop(0); st1=stack.pop(-1); st2=stack.pop(-1)
                st1=shrink(st1,newOp)
                st2=shrink(st2,newOp)
                stack.append('(%s%s%s)'%(st1,newOp,st2))
                prevOps.append(newOp)
        return stack.pop(0)[1:-1]
    for nums in permutations(Nums):
        save = set()
        for ops in product('+-*/',repeat=len(nums)-1):
            for i in set(mather(len(nums))):
                s = change(list(nums),list(ops),i)
                try:
                    if eval(s)==lookup and s not in save:
                        yield s
                        save.add(s)
                except ZeroDivisionError: pass
    return "None"
def sudoku(stringrid):
    from done.List import cross
    #These are static vars
    rows,cols='ABCDEFGHI','123456789'
    squares=cross(rows,cols) #Every boxy (denoted by s)
    units=dict((s,[u for u in [cross(rows, c) for c in cols]+[cross(r, cols) for r in rows]+[cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
                     if s in u]) for s in squares) #s:[Column, Row, Square] (all three units denoted by u=s[])
    peers=dict((s,set(sum(units[s],[]))-set([s])) for s in squares) #s:union(u1,u2,u3)
    #This is the state
    values=dict((s,cols) for s in squares) #s:'123456789' (denoted by d)
    #Prepare for Ultra-Recursive Definitions
    def parse(stringrid): #change values to match grid
        for s,d in dict(zip(squares,[c for c in stringrid if c in cols+'0.'])).items():
            if d in cols and not assign(values,s,d): return 0
        return values
    def assign(v,s,d): #eliminate all the values!=d from values[s]
        if all(eliminate(v,s,d2) for d2 in v[s].replace(d,'')): return v
        return 0
    def eliminate(v,s,d): #eliminate d from values[s]
        if d not in v[s]: return v #already eliminated
        v[s]=v[s].replace(d,'')
        #if s only has 1 value: eliminate value from peers.
        if len(v[s])==0: return 0
        elif len(v[s])==1:
            if not all(eliminate(v,s2,v[s]) for s2 in peers[s]): return 0
        #if u has only 1 square for value d, then assign d.
        for u in units[s]: 
            dplaces = [s for s in u if d in v[s]]
            if len(dplaces)==0: return 0
            elif len(dplaces)==1:
                if not assign(v,dplaces[0],d): return 0
        return v
    def search(v): #try all possible values
        if v==0: return 0
        if all(len(v[s])==1 for s in squares): return v
        s=min((len(v[s]),s) for s in squares if len(v[s])>1)[1] #choose square s with least values
        #it has to be one of those d so pick one and search again
        for d in v[s]:
            i=search(assign(v.copy(),s,d))
            if i: return i
    values=search(parse(stringrid))
    if not values: return "No Solution for this Grid"
    out='\n'
    for r,c in squares:
        out+=values[r+c]
        if c in '36': out+='|'
        elif c=='9' :
            out+='\n'
            if r in 'CF': out+='-----------\n'
    print(out)
def numRemainders(divisors,remainders):
    "_(sorted({3,8,3,7}),list([2,4,2])) = 74"
    divisors=sorted(set(divisors)); remainders=list(remainders)
    if len(divisors)!=len(remainders) or any(r!=r%d for d,r in zip(divisors,remainders)): return False
    from done.List import lcm
    LCM=lcm(list(divisors))
    from functools import reduce
    return reduce(set.intersection, (set(range(r,LCM,d)) for d,r in zip(divisors,remainders)))
    
def respart(num,lis,sort=True):
    "_(50, [4, 7]) yields '6*7+2*4'"
    if sort: lis=[i for i in sorted(lis,reverse=True) if i>0]
    for i in range(num//lis[0]+1):
        new = num-i*lis[0]
        if new==0: yield '{}*{}'.format(i,lis[0]) 
        elif new>0 and len(lis)>1:
            for piece in respart(new,lis[1:],False):
                if i==0: yield piece
                elif i==1: yield '{} + '.format(lis[0]) + piece
                else: yield '{}*{} + '.format(i,lis[0]) + piece
    
def addOrSub(string,num):
    "Adds +, -, or nothing between every number and evals to num"
    if not (string.isnumeric() and type(num)==int): return "Why are you here?"  
    from itertools import product
    n=len(string)
    for stry in product('+ -',repeat=n-1):
        stry+=(' ',)
        math=''.join(string[i]+stry[i] for i in range(n)).replace(' ','')
        if eval(math)==num: print(stry.count('+')+stry.count('-'),math)