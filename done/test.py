#!/usr/bin/env python3

''' Tests for the Done Files
Just in case some random edit Breaks something one day
'''

def inversable(func, s, invr=None, ne=str.__ne__, name=""):
    if not name: name = str(func).split()[1]
    if not invr: invr = func
    try: a = func(s)
    except Exception as e:
        print("%s Failed: Function throws Error: "%name)
        print("\tInput: %s"%s)
        print("\t%s"%e)
        return 0
    try: b = invr(a)
    except Exception as e:
        print("%s Failed: Inverse throws Error: "%name)
        print("\tInput: %s"%s)
        print("\tOutput: %s"%a)
        print("\t%s"%e)
        return 0
    if ne(s, b):
        print("%s Failed: Not Equal"%name)
        print("\tInput: %s"%s)
        print("\tOutput: %s"%a)
        print("\tInverse Output: %s"%b)
        return 0
    return 1

def Codes():
    import done.Codes as Codes
    from random import sample
    
    succ = 1
    
    from random import randint
    spacesnotpreserved = lambda a,b: ''.join(a.split()) != ''.join(b.split())
    capitalnotpreserved = lambda a,b: a.lower() != b.lower()
    A = "1234 567890 qwertyuio pasdfghjklz xcvbnm QWERTYU IOPASD FGHJKLZX CVBNM"
    
    for i in range(100):
        # No double spaces pls
        s = ' '.join(''.join(sample(A,len(A)//2)).split())
        
        succ&=inversable(Codes.crosc,s)
        succ&=inversable(Codes.crazyness,s)
        
        succ&=inversable(Codes.binary,s,
        invr=lambda x: Codes.binary(x,toBin=0))
        
        succ&=inversable(Codes.numword,s,
        invr=lambda x: Codes.numword(x,inverse=1))
        
        succ&=inversable(Codes.piglatin,s,
        invr=lambda x: Codes.piglatin(x,inverse=1))
        
        succ&=inversable(Codes.eggnog,s,
        ne=spacesnotpreserved)
        
        succ&=inversable(Codes.morse,s,
        invr=Codes.antimorse,
        ne=capitalnotpreserved)
        
        succ&=inversable(Codes.bobulate,s,
        invr=lambda x: Codes.unbobulate(x)[0],
        ne=capitalnotpreserved)
        
        d = randint(0,50)
        succ&=inversable(lambda x: Codes.cypher(x,d),s,
        lambda x: Codes.cypher(x,-d),
        name='Codes.cypher')

    print("Codes.py "+("Passed" if succ else "did not Pass"))

def File():
    import done.File as File
    succ = 1
    if not File.exists(File.getHome()):
        succ = 0
        print("Desktop doesn't exist?")
    # TODO how to test files(), folders(), listFormats(), hideInMaze(), linkDirectory(), Delete(), smartBackup(), renamer(), delPyCache(), getSizes(), resize(), siteLook(), siteRead(), read(), write(), reImport(), dARename(), ZipGui(), unzip()

    print("File.py "+("Passed" if succ else "did not Pass"))

def Game():
    import done.Game as Game
    succ = 1
    
    import sys
    from io import StringIO
    
    def GameTester(func, send = "giveup\ngiveup\n15\n12\n"):
        succ = 1
        sys.stdin = StringIO(send)
        sys.stdout = StringIO()
        try: func()
        except Exception as e:
            succ = 0
            sys.stdout = sys.__stdout__
            print(str(func).split()[1]+" doesnt work. Exception: "+str(e))
        return succ
    
    succ&=GameTester(Game.multgame)
    succ&=GameTester(Game.pattgame)
    succ&=GameTester(Game.physics)
    succ&=GameTester(Game.thinker)
    succ&=GameTester(Game.mindread,send = "3\n4\n")
    succ&=GameTester(Game.zombie,"1\n1\n1\n1\n1\n2\n2\n1\n3\n1\n")
    succ&=GameTester(Game.ultrps,"nat\nhot\nmet\nqui\n")
    succ&=GameTester(Game.murdergame,"q\n")
    
    sys.stdout = sys.__stdout__
    sys.stdin = sys.__stdin__
    
    print("Game.py "+("Passed" if succ else "did not Pass"))

def List():
    import done.List as List
    from random import randint
    succ = 1
    
    # TODO poisson, Dev, freqDev, probDev, hypergeometric
    for j in range(50):
        l = [randint(-100,100)]
        for i in range(9):
            l.append(randint(-100,100))
            l.append(2*l[0]-l[-1])
        if l[0] != List.median(l):
            succ = 0
            print("List.median Failed:")
            print("Input: %s"%l)
            print('Output: %s'%List.median(l))
    
    #TODO gcd,lcm,show,cross,combine
    
    for i in range(100):
        succ&=inversable(List.dct,[randint(-100,100),randint(-100,100),randint(-100,100),randint(-100,100)],
        invr=List.idct,ne=list.__ne__)
    
    print("List.py "+("Passed" if succ else "did not Pass"))

def Math():
    # import done.Math as Math
    # succ = 1

    # TODO angle, angleForStar, nomial/polynom, BitString, factorial, permutation, combination

    # print("Math.py "+("Passed" if succ else "did not Pass"))
    pass

def Number():
    # import done.Number as Number
    # succ = 1

    # TODO simplifyRadical, pyTrip, pythagoreanTriplets,factorsOf, isPrime, nextPrime, primeFactorize, theFactorsOf, BaseInteger, changeBase, toBaseTen, fromBaseTen, numToStr, piecewiseMaker

    # print("Number.py "+("Passed" if succ else "did not Pass"))
    pass

def Solver():
    import done.Solver as Solver
    from random import randint, sample
    from done.List import lcm
    succ = 1

    # TODO solve, sudoku
    
    for j in range(50):
        giveup=randint(10,99)
        lis=sample([2,3,5,7,11],3)
        lis.sort()
        li = list(range(len(lis)))
        for i in range(3): li[i]=giveup%lis[i]
        n=lcm(lis)
        giveup%=n
        n=Solver.numRemainders(lis,li)
        if giveup not in n:
            succ = 0
            print("Solver.numRemainder Failed:")
            print("\tInput: %s,%s"%(lis,li))
            print("\tOutput: %s"%n)
            print("\tActual Output: %s"%giveup)
    
    # TODO respart, addOrSub

    print("Solver.py "+("Passed" if succ else "did not Pass"))
    pass

def String():
    # import done.String as String
    # succ = 1

    # TODO Input, lisp, switch, findListInStr, reverse, backwards, charShift, font, uptiny, updown, strShuffle, dyslexia, wrapPrint, removePrint, score, findOccurance, isRep, endRedFind, showInfo, chain, loremIpsum, chemistry, anagram, clues22, tree, Markov, pretty, SequenceAlignment, DeBruijn

    # print("String.py "+("Passed" if succ else "did not Pass"))
    pass

def Time():
    # import done.Time as Time
    # succ = 1

    # TODO Time, bisectHrMnHands, DayOfTheWeek, stopwatch, countdown

    # print("Time.py "+("Passed" if succ else "did not Pass"))
    pass


def main():
    Codes()
    File()
    Game()
    List()
    Math()
    Number()
    Solver()
    String()
    Time()

if __name__ == '__main__':
    main()