'''Deals with anything string and cute string manipulations'''

def Input(s=None,end=''):
    """"Accept multiple input lines yields line by line
    
    Usage:
        
        # read across newlines passed in but end once the end string is on it's own line
        # if empty will end once an empty line is passed in
        for line in Input("Input statement","<end>"):
            <block>
    """
    if not s:
        for i in iter(input, end): yield i
    else: 
        for i in iter(lambda: input(s), end): yield i

def lisp(string):
    """Make your string have a lisp by replacing letter combinations with th"""
    return string.replace('sh','th').replace('st','th').replace('s','th').replace('Sh','Th').replace('St','Th').replace('S','Th')
def switch(mainstring,string1,string2,switch=' <(°•‹˚˚›•°)> '):
    """Swap every occurance of {string1} and {string2} in {mainstring} with each other
    
    Usage:
        switch('10101011','1','0') = '01010100'
    """
    if switch in mainstring: raise Exception("switch %s was in the mainstring. Please adjust switch so that it does not appear in mainstring"%switch)
    return mainstring.replace(string1,switch).replace(string2,string1).replace(switch,string2)
def findListInStr(string,lis):
    """Find the first string in a list that is a substring in {string}
    
    Usage:
        findListInStr('hello world word', ['word', 'world']) -> 'word'
    """
    for i in lis:
        if i in string: return i
    return False
def reverse(str_):
    """Reverse the String"""
    return str_[::-1] #''.join(reversed(str_))
def backwards(str_):
    """Reverse the String as well as horizontally rotate the characters"""
    from random import randrange
    def get(c):
        n=ord(c)-ord('A')
        if n<20 and not n<0:
            return "ɒdɔbɘᖷGʜIႱʞ⅃mnoqpЯƨƚ"[n] if randrange(2) else "AᙠƆᗡƎᖷGʜIႱʞ⅃MИOꟼỌЯƧT"[n]
        return c
    return ''.join(get(c) for c in reversed(str_.upper()))
def charShift(c,p):
    """Shifts the character's ord by {p} if it is an alphabetical character"""
    if c.isalpha(): return chr(ord(c)+p)
    return c
def font(s):
    """Changes the alaphabetical characters with their full-width-romaji equivalent"""
    return ''.join(charShift(c,ord('Ａ')-ord('A')) for c in s.title())
# TODO uptiny not working properly
def uptiny(s): return ''.join(charShift(c,ord('ᴬ')-ord('A')) for c in s.title())
def updown(str_):
    """Reverse the String as well as vertically rotate the characters"""
    def get(c):
        n=ord(c)-ord('a')
        if n<26 and not n<0: return 'ɐqɔpǝɟƃɥᴉɾʞlɯuodbɹsʇnʌʍxʎz'[n]
        return c
    return ''.join(get(c) for c in reversed(str_.lower()))
def strShuffle(str_):
    """Shuffle a whole string. Just shuffle it."""
    from random import shuffle
    a = list(str_)
    shuffle(a)
    return ''.join(a)
def _dyslexia1(str_):
    """Take a word and shuffle the letters not on the ends"""
    if len(str_)<4: return str_
    return str_[0] + strShuffle(str_[1:-1]) + str_[-1]
def dyslexia(str_):
    """Takes the words in string and shuffles their middles"""
    return ' '.join( _dyslexia1(i) for i in str_.split() )

def wrapPrint(str_,num=79):
    """Wraps the text to stay to a max line width of {num}"""
    newStr = ''
    lis = [i for i in str_.replace('\n',' \n ').split(' ') if len(i)!=0]
    line = ''
    for i in range(len(lis)):
        word = lis[i]
        if word == '\n':
            newStr+='\n'+line
            line=''
        elif len(line)==0: line=word
        elif len(line)+len(word)<num: line+=' '+word
        else:
            newStr+='\n'+line
            line=' '+word
    print(newStr)
smartPrint = wrapPrint

def removePrint(str_,size=79,around=None):
    """Prints out the ends of the string with '...' if anything was removed
    
    If {around} is defined, will try to find the substring.
    If substring is found, it will show the center around the substring and will delete before and after the window instead
    """
    if len(str_)>2*size: 
        if around:
            i = str_.find(around)
            if i!=-1:
                s = str_[:size]
                if 2*size<i: s+=' ... '
                s+= str_[i-size:i+size]
                if len(s)-i<2*size: s+=' ... '
                print(s+str_[-size:])
                return
        print(str_[:size]+' ... '+str_[-size:])
    else: print(str_)
safePrint = removePrint

def score(sA,sB):
    """Compare the two strings and give it a score between 0 and 1"""
    sA, sB = sA.lower(), sB.lower()
    aa, bb = len(sA), len(sB)
    if not aa and not bb: return 0
    window = max(aa,bb) // 2 - 1
    if window < 0: window = 0
    aFlags, bFlags = [0]*aa, [0]*bb
    common = 0
    for i, aChar in enumerate(sA):
        lo = i-window if i>window else 0
        hi = i+window+1 if i+window < bb else bb
        for j in range(lo,hi):
            if not bFlags[j] and sB[j]==aChar:
                aFlags[i] = bFlags[j] = True
                common += 1
                break
    if not common: return 0
    k = trans = 0
    for i, aFlag in enumerate(aFlags):
        if aFlag:
            for j in range(k,bb):
                if bFlags[j]: 
                    k = j+1
                    break
            if sA[i]!=sB[j]: trans+=1
    trans /= 2
    common = float(common)
    return ( common/aa + common/bb + (common-trans)/common ) / 3 

def findOccurance(string,sub,i):
    """"Find the {i}-th occurance of the substring in the string
    
    Usage:
        findOccurange('bla bla di bla','la',3) -> 12
    """
    ind = -1
    while i>0:
        ind = string.find(sub,ind+1)
        i-=1
        if ind==-1: return -1
    return ind
def isRep(a,b):
    """"Figure out if the string is just the second string repeated a bunch
    
    Usage:
        isRep('44554455445','4455') -> True"""
    mult = len(a)//len(b)
    if mult < 2: return False
    b = b*(mult+1)
    return a[:len(b)]==b[:len(a)]
def endRepFind(str_):
    """Find the last bit of the string that is a repetition
    
    Usage: 
        endRepFind('123445544554455') = '4455'
    """
    def find(s):
        """Takes first symbol and goes through all occurances until it finds repeating section"""
        found = s.find(s[0],1)
        while found != -1:
            section = s[:found]
            if isRep(s,section): return section
            found = s.find(s[0],found+1)
        return False
    #Removes first symbol until left with repeating part
    for i in range(len(str_)):
        stop = find(str_[i:])
        if stop: return stop
    return ''

def showInfo(thing,search=''):
    """Shows some information about the object passed in
    
    - if iterable: print elements containing search
    - if function: print args
    - else showInfo(dir(thing), search) #dir is iterable
    """
    try: #If iterable
        for i in thing:
            if search in str(i):
                print(i)
        return
    except: pass
    # Not Iterable
    from inspect import getargspec
    try:
        print(getargspec(thing)) #If function
        return
    except: pass
    #Not Callable
    for i in dir(thing): #Dir is always iterable
        try:
            if search in i: print("%s : %s"%(i,getattr(thing,i)))
        except: pass # IDK what kind of errors getattr can throw but just dont

def chain(words,letters):
    """Create pronounceable words
    
    Usage:
        chain(5,5) = 5 allcaps five-letter words seperated with spaces
    """
    from random import randrange
    #          A   B  C  D  E    F  G  H  I  J K L    M  N  O  P     Q R  S  T   U     V W  X Y  Z
    matr={' ':[116,47,35,26,20 , 38,20,72,63,6,6,27 , 43,24,63,25  , 2,17,78,167,15  , 6,67,1,16,1],
          'A':[1,32,39,15,1    , 10,18,1,16,1,10,77 , 18,172,2,31  , 1,101,67,124,12 , 24,7,1,27,1],
          'B':[8,0,0,0,58      , 0,0,0,6,2,0,21     , 1,0,1,0      , 0,6,5,0,5       , 0,0,0,19,0],
          'C':[44,0,12,0,55    , 1,0,46,15,0,8,16   , 0,0,59,1     , 0,7,1,38,16     , 0,1,0,0,0],
          'D':[45,18,4,10,39   , 12,2,3,57,1,0,7    , 9,5,37,7     , 1,10,32,39,8    , 4,9,0,6,0],
          'E':[131,11,64,107,39, 23,20,15,40,1,2,46 , 43,120,46,32 , 14,154,145,80,7 , 16,41,17,17,0],
          'F':[21,2,9,1,25     , 14,1,6,21,1,0,10   , 3,2,38,3     , 0,4,8,42,11     , 1,4,0,1,0],
          'G':[11,2,1,1,32     , 3,1,16,10,0,0,4    , 1,3,23,1     , 0,21,7,13,8     , 0,2,0,1,0],
          'H':[84,1,2,1,251    , 2,0,5,72,0,0,3     , 1,2,46,1     , 0,8,3,22,2      , 0,7,0,1,0],
          'I':[18,7,55,16,37   , 27,10,0,0,0,8,39   , 32,169,63    , 3,0,21,106,88,0 , 14,1,1,0,4],
          'J':[1,0,0,0,2       , 0,0,0,0,0,0,0      , 0,0,4,0,0    , 0,0,0,4         , 0,0,0,0,0],
          'K':[0,0,0,0,28      , 0,0,0,8,0,0,0      , 0,3,3,0      , 0,0,2,1,0       , 0,3,0,3,0],
          'L':[34,7,8,28,72    , 5,1,0,57,1,3,55    , 4,1,28,2     , 2,2,12,19,8     , 2,5,0,47,0],
          'M':[56,9,1,2,48     , 0,0,1,26,0,0,0     , 5,3,28,16    , 0,0,6,6,13      , 0,2,0,3,0],
          'N':[54,7,31,118,64  , 8,75,9,37,3,3,10   , 7,9,65,7     , 0,5,51,110,12   , 4,15,1,14,0],
          'O':[9,18,18,16,3    , 94,3,3,13,0,5,17   , 44,145,23,29 , 0,113,37,53,96  , 13,36,0,4,2],
          'P':[21,1,0,0,40     , 0,0,7,8,0,0,29     , 0,0,28,26    , 0,42,3,14,7     , 0,1,0,2,0],
          'Q':[0,0,0,0,0       , 0,0,0,0,0,0,0      , 0,0,0,0      , 0,0,0,0,20      , 0,0,0,0,0],
          'R':[57,4,14,16,148  , 6,6,3,77,1,11,12   , 15,12,54,8   , 0,18,39,63,6    , 5,10,0,17,0],
          'S':[75,13,21,6,84   , 13,6,30,42,0,2,6   , 14,19,71,24  , 2,6,41,121,30   , 2,27,0,4,0],
          'T':[56,14,6,9,94    , 5,1,315,128,0,0,12 , 14,8,111,8   , 0,30,32,53,22   , 4,16,0,21,0],
          'U':[18,5,17,11,11   , 1,12,2,5,0,0,28    , 9,33,2,17    , 0,49,42,45,0    , 0,0,1,1,1],
          'V':[15,0,0,0,53     , 0,0,0,19,0,0,0     , 0,0,6,0      , 0,0,0,0,0       , 0,0,0,0,0],
          'W':[32,0,3,4,30     , 1,0,48,37,0,0,4    , 1,10,17,2    , 0,1,3,6,1       , 1,2,0,0,0],
          'X':[3,0,5,0,1       , 0,0,0,4,0,0,0      , 0,0,1,4      , 0,0,0,1,1       , 0,0,0,0,0],
          'Y':[11,11,10,4,12   , 3,5,5,18,0,0,6     , 4,3,28,7     , 0,5,17,21,1     , 3,14,0,0,0],
          'Z':[1,0,0,0,5       , 0,0,0,2,0,0,1      , 0,0,0,0      , 0,0,0,0,0       , 0,0,0,0,1]
          } #Magic following letter probability matrix
    def findlet(lis,num): #Return index of where num lands
        for k in range(26): 
            if sum(lis[:k+1]) > num: return chr(k+65)
    word=''
    for i in range(words*(letters+1)):
        if i%(letters+1)==0: word+=' '
        else: word+=findlet(matr[word[i-1]],randrange(sum(matr[word[i-1]])))
    return word[1:].title()

def loremIpsum(n=60,a=2,b=12):
    """Makes random words from length {a} to {b} until {n} are made"""
    from random import randint
    return ' '.join(chain(1,random.randint(a,b)) for i in range(n))



def chemistry(longString="Hello World",showall=False):
    """Given a sentence will try to recreate string with chemistry symbols"""
    # without j and q the algorithm would get stuck
    def splitTarget(target,word):
        target,word = target.lower(),word.lower()
        grow = ''
        for c in word:
            if target[:1]==c: 
                grow += target[:1]
                target = target[1:]
        return grow,target
    def perfLvl(gem,gemAim):
        if len(gem) == 1: return 2
        for i in range(len(gem),0,-1):
            if gem[:i].lower() == gemAim[:i].lower(): return 2*i-1
        return 0
    Gems = ['j*','q*','H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn', 'Uut', 'Fl', 'Uup', 'Lv', 'Uus', 'Uuo']
    UseGems = dict() # grab the gems that are possible to use
    def expandWord(word,target):
        first,last = splitTarget(target,word)
        tLetter = last[:1]
        if not tLetter: return
        save = dict( ( word+i , perfLvl(i,last) ) for i in UseGems[tLetter] )
        M = 1 if 2 in save.values() else 0
        return [ i for i in save if save[i] > M ]
    def yieldMaximums(words,target,M=.5,show=0): 
        returnable = dict()
        for w in list(words): #For every word in that list
            if show: print("\t"*(show-1)+"LOOP "+repr(w))
            words = expandWord(w,target) #Add symbols if you can
            if show and words: print("\t"*(show-1)+str(words))
            if words: #If words have been added go deeper
                words,M = yieldMaximums(words,target,M, 0 if not show else show+1 ) 
                returnable.update( dict( (word , words[word]) for word in words if words[word]>=M) )
            else: 
                s = score(target,w)
                if s>=M:
                    M = s
                    returnable.update( { w : s } )
                    if show: print("\t"*(show-1)+str({w:s}))
        for w in list(returnable.keys()):
            if returnable[w]!=M: returnable.pop(w)
        if show and returnable: print("\t"*(show-1)+"RETURN "+str(returnable))
        return returnable,M
    def chems(target,debug=0):
        save = yieldMaximums([''],target,show=debug)
        return list(save[0]),save[-1]
    
    for i in range(ord('a'),ord('z')+1):
        i = chr(i)
        lis = UseGems.get(i,list())
        if not lis: UseGems[i] = [g for g in Gems if i in g[:1].lower()]
    from random import randrange
    string = ''
    for word in longString.lower().split():
        word = ''.join(c for c in word if c.isalpha())
        chem,num = chems(word)
        if showall: print(num, chem)
        chem = chem[randrange(len(chem))]
        string += chem + ' '
    return string



def anagram(jumbledWord,dictionaryFile = '/usr/share/dict/web2'):
    """Unshuffles the word given by comparing it to words in a file with words inside"""
    import re
    jumbledWord = jumbledWord.lower()
    wordset = set(jumbledWord)
    with open(dictionaryFile) as f: dictionary = set(f.read().lower().split())
    # letters that are not allowed
    hbl=re.compile("[%s]"%''.join(set('abcdefghijklmnopqrtsuvwxyz').difference(wordset)))
    # count the letters that are allowed
    count=dict((i,jumbledWord.count(i)) for i in wordset)
    dictionary = sorted(sorted([x for x in dictionary if not hbl.search(x) and len(x)>2 and all(x.count(i)<=count.get(i,0) for i in set(x))]),key=lambda x:len(x))
    for i in dictionary: print(i)

def clues22(pairs,dictionaryFile = '/usr/share/dict/web2'):
    """rearrange substrings to create a word in the dictionary file
    
    Usage:
        clues22(['he','ll','be','o']) -> list containing "hello" and "bell"
    """
    def assemble(word,pairs):
        if len(word)==0: return True
        possible = [i for i in pairs if word.startswith(i)]
        if len(possible)==0: return False
        for trypair in possible:
            temp = list(pairs)
            temp.remove(trypair)
            if assemble(word[len(trypair):], temp): return True
        return False
    import re
    pairs = [i.lower() for i in pairs]
    with open(dictionaryFile) as f: dictionary = set(f.read().lower().split())
    allletters=''.join(pairs)
    hbl=re.compile("[%s]"%''.join(set('abcdefghijklmnopqrtsuvwxyz').difference(set(''.join(pairs)))))
    count=dict((i,allletters.count(i)) for i in set(allletters))
    dictionary = sorted(sorted([x for x in dictionary if not hbl.search(x) and len(x)>2 and all(x.count(i)<=count.get(i,0) for i in set(x)) and assemble(x,pairs)]),key=lambda x:len(x))
    for i in dictionary: print(i)
def oneLetterFromEach(listring,dictionaryFile = '/usr/share/dict/web2'):
    """picks one letter from each string and rearranges it to make words
    
    Usage:
        oneLetterFromEach(["t","hx","ea"]) -> ["the","het","hat","tax",...]
    """
    import re
    import itertools
    
    with open(dictionaryFile) as f: dictionary = set(i for i in f.read().lower().split() if len(i) == len(listring))
    def Anagram(jmbl, d = dictionary):
        jmbl = jmbl.lower()
        letters = set(jmbl)
        # letters that are not allowed
        hbl=re.compile("[%s]"%''.join(set('abcdefghijklmnopqrtsuvwxyz').difference(letters)))
        # count the letters that are allowed
        count=dict((i,jmbl.count(i)) for i in letters)
        yield from sorted(sorted([x for x in dictionary if not hbl.search(x) and len(x)>2 and all(x.count(i)<=count.get(i,0) for i in set(x))]),key=lambda x:len(x))
    for p in itertools.product(*listring):
        ngrm = "".join(p)
        yield from Anagram(ngrm)
def connectWords(word1,word2,dictionaryFile='/usr/share/dict/web2'):
    """changes 1 letter at a time until word1 becomes word2"""
    if len(word1) != len(word2): return
    l = len(word1)
    word1 = word1.lower()
    word2 = word2.lower()
    from heapq import heappop, heappush
    def offByOne(w1,w2):
        # n measures how many letters are off
        n = abs(len(w1)-len(w2))
        for i in range(min(len(w1),len(w2))):
            if n > 1: return False
            if w1[i] != w2[i]: n += 1
        return n == 1
    def getNeighbors(word,dictionarySet,remove=0):
        for w in list(dictionarySet):
            if offByOne(w,word):
                if remove: dictionarySet.remove(w)
                yield w
    with open(dictionaryFile) as f: unvisited = set(i for i in f.read().lower().split() if len(i) == l)
    queue = [(1,w,[word1]) for w in getNeighbors(word1,unvisited,remove=1)]
    goals = set(getNeighbors(word2,unvisited))
    m = len(unvisited)
    if not len(queue) or not len(goals): return
    while len(unvisited) != 0 and len(queue) != 0:
        dist,word,rest = heappop(queue)
        if dist > m: continue
        if word in goals:
            yield rest+[word,word2]
            m = dist
        else:
            for neigh in getNeighbors(word,unvisited,remove=1): heappush(queue,(dist+1,neigh,rest+[word]))

class Node():
    def __init__(self, name, parent):
        super(Node, self).__init__()
        self.name = name
        self.parent = parent
        self.children = []
        if type(parent)==Node: parent.children.append(self)
    def str(self,ln): return (('+   '*(ln-1) + '+---') if ln>0 else '') + self.name +('\n' if len(self.children) else '')+ '\n'.join(i.str(ln+1) for i in self.children)
    def __str__(self): return self.str(0)
def tree(raw='{0 of 1 of 2, -1 of 0 of 1 of 2}'):
    """Parses Applescript's 'entire contents' text to show what is contained in what
    
    Example:
        tree("{list of page of window of screen, text of list of page of window of screen}") -> Node
        print(_) ->
            screen
            +---window
            +   +---page
            +   +   +---list
            +   +   +   +---text
    """
    def splitYield(st):
        a,b = 0,1
        com = 0
        while com!=-1:
            com = st.find(",",b)
            quote = st.find('"',b)
            if quote!=-1 and quote<com:
                b = st.find('"',quote+1)+1
                continue
            b = com+1
            if com<0: b = len(st)+1
            yield st[a:b-1]
            a = b
    bigDic = {'': Node('*top',None)}
    raw = raw .strip('{').strip('}')
    for line in splitYield(raw):
        line = line.split(' of ')
        prevS = ''
        prevN = ''
        while len(line)>0:
            name = line.pop(-1).strip(' ')
            search = name+' of '+prevS
            bigDic[search] = bigDic.get(search, False)
            if not bigDic[search]: bigDic[search] = Node(name,bigDic[prevS])
            prevS = search
            prevN = name
    if len(bigDic[''].children)==1: return bigDic[''].children[0]
    return bigDic['']

class Markov():
    """Create a Markov Chain of words linked in triplets"""
    from random import randint,choice
    def __init__(self, words):
        self.words = words.strip().split()
        self.cache = dict()
        for w1, w2, w3 in self.triples():
            key = (w1, w2)
            if key in self.cache: self.cache[key].append(w3)
            else: self.cache[key] = [w3]
    def triples(self):
        if len(self.words) < 3: return
        for i in range(len(self.words) - 2):
            yield (self.words[i], self.words[i+1], self.words[i+2])
    def generate(self, size=25):
        seed = Markov.randint(0, len(self.words)-3)
        seed_word, next_word = self.words[seed], self.words[seed+1]
        w1, w2 = seed_word, next_word
        gen_words = []
        for i in range(size):
            gen_words.append(w1)
            try: w1, w2 = w2, Markov.choice(self.cache[(w1, w2)])
            except: 
                gen_words.append(w2)
                return ' '.join(gen_words) + " "+ self.generate(size-i-2)
        gen_words.append(w2)
        return ' '.join(gen_words)

def pretty(width=80,height=20):
    """Prints a rectangle of stars in the Terminal"""
    from time import sleep
    width = 3*width//8
    stars = '． . ☆ . ＋ . 。 . ． . . ． 。 ﾟ 。 , ☆ ﾟ . ＋ 。 ﾟ , 。 . 。 , . 。 ﾟ 。 ﾟ . + 。 ﾟ * 。 . , 。 ﾟ + . 。 * 。 ﾟ . . . ． … , 。 ＋ ﾟ 。 。 ﾟ . ﾟ 。 , ☆ * 。 ﾟ . o , 。 . ＋ ﾟ 。 。 ﾟ . ﾟ 。 , ☆ * 。 ﾟ .'
    f = Markov(stars)
    endspace = " "*(width//8)
    while 1:
        for i in range(height): print(f.generate(width)+endspace)
        print("\033[F"*height,end="\r")
        sleep(.32)
def SequenceAlignment(s1,s2,DownSigma=0,RightSigma=0,Match=1,MisMatch=0):
    """Preforms Global Sequence Alignment on the two strings"""
    n,m = len(s1),len(s2); S = [[0 for j in range(m+1)] for i in range(n+1)]; S[0][0] = (0,0)
    for j in range(1,m+1): S[0][j] = (S[0][j-1][0] + RightSigma,2) #Right Sigma
    for i in range(1,n+1): S[i][0] = (S[i-1][0][0] + DownSigma,1) #Down  Sigma
    for j in range(1,m+1):
        for i in range(1,n+1):
            S[i][j] = max(
                (S[i-1][j-1][0]+(Match if s1[i-1]==s2[j-1] else MisMatch), 3), #Diagonal
                (S[i-1][j][0]+DownSigma, 1),#Down  Sigma
                (S[i][j-1][0]+RightSigma, 2),#Right Sigma
            )
    i,j = n,m; ss1,ss2 = "",""; score,direction = S[i][j]
    while direction:
        if   direction == 1: #Down
            ss1=s1[i-1]+ss1; ss2="-"    +ss2; i -= 1
        elif direction == 2: #Rite
            ss1="-"    +ss1; ss2=s2[j-1]+ss2;         j -= 1
        elif direction == 3: #Diag
            ss1=s1[i-1]+ss1; ss2=s2[j-1]+ss2; i -= 1; j -= 1
        score,direction = S[i][j]
    return ss1,ss2



def db_test():
    al = 'acbef'
    l = 5
    seq = DeBruijn(al,l)
    seqseq = seq+seq
    store = set()
    for i in range(len(seq)):
        word = seqseq[i:i+l]
        if word in store: break
        store.add(word)
    assert len(store) == len(set(al))**l # Check that all possible arrangements of length l were added
    print("Assertion Passed")
def DeBruijn(alphabet, length):
    ''' Given an alphabet and substring length construct a DeBruijn Sequence '''
    alphabet = ''.join(sorted(set(alphabet)))
    allen = len(alphabet)

    wordx = int(allen**(length-1)) #calculate the multiplier for the alphabet
    word = lambda i: alphabet[i//wordx] # 111222333

    # maps corresponding items into lyndon cycles
    mapper = lambda n: n//wordx+(n%wordx)*allen

    def db():
        visited = list(False for i in range(allen*wordx))
        for i in range(allen*wordx):
            if visited[i]: continue # If a cycle has visited this node then it is not the lexicographic minimum of its rotations
            lyndon = word(i)
            j = mapper(i)
            while j!=i:
                visited[j] = True
                lyndon += word(j)
                j = mapper(j)
            yield lyndon
    return ''.join(db())