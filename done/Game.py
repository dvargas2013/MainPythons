'''Contains fun stuff you can do with my computer 'cause of skills'''
from random import randint,randrange,sample
from done.List import lcm

def matrix(mini,maxi):
    """print random integers between min and max... never stops"""
    while 1: print(randint(mini,maxi),end='')

def multgame(digitAmount1,digitAmount2):
    """Give will ask you to multiply number of digit
    
    Usage:
        _(2,3) = 2 digit number * 3 digit number = ?
    """
    while 1:
        x,y=randrange(10**(digitAmount1-1),10**digitAmount1),randrange(10**(digitAmount2-1),10**digitAmount2)
        c=x*y-1
        while c!=x*y:
            c=eval(input(str(x)+'*'+str(y)+'=?: '))
            if c==x*y: print(c,'is Correct')
            else: print(c,'is Wrong')


def pattgame(multiplicand,multiplier,addend,hintamount):
    """Gives a pattern that multiplies by a num then adds by another num repeatedly"""
    if hintamount<3: hintamount=3
    lis=list(range(hintamount+1))
    while 1:
        ri,dif,mul=0,0,0
        while ri==0: ri=randint(-multiplicand,multiplicand)
        while mul==0: mul=randint(-multiplier,multiplier)
        while dif==0: dif=randint(-addend,addend)
        lis[0]=ri
        for b in range(hintamount): ri,lis[b+1]=mul*ri+dif,mul*ri+dif
        q=ri-1
        while q!=ri:
            for b in range(hintamount): print(lis[b])
            q=eval(input('Next number is: '))
            if q==ri: print(q,'is correct')
            else: print(q,'is wrong')



def problem(*stuff,info='',aim=0):
    loop=aim+1
    while 1:
        print(X.format(*stuff))
        loop=eval(input(info))
        if loop!=aim: print("{} is Incorrect".format(loop))
        else: break
    print("{} is Correct\n=====NewProblem=====".format(loop))
def physics():
    """Asks newtonian physics questions on acceleration, time, velocity and distance"""
    X='\n{} {}\n{} {}\n{} {}'
    A,VI,T,D,VF='Acceleration:','Initial Speed:','Time:','Distance:','Final Speed:'
    while 1:
        a,vi,t,d,c=randint(1,6),randrange(10),randint(1,8),5*randrange(13),randrange(5)
        vf=randint(vi,10)
        if c==0: problem(VI,vi,T,t,A,a,info=D+' ',aim=vi*t+.5*a*t**2)
        elif c==1: problem(VF,vf,VI,vi,A,a,info=D+' ',aim=(vf*vf-vi*vi)/(2*a))
        elif c==2: problem(VI,vi,A,a,D,d,info=VF+' ',aim=(vi*vi+2*a*d)**.5)
        elif c==3: problem(VI,vi,A,a,T,t,info=VF+' ',aim=vi+a*t)
        else: problem(VF,vf,VI,vi,A,a,info=T+' ',aim=(vf-vi)/a)



def thinker():
    """Logic game with remainders"""
    while 1:
        deta,lis=randint(10,99),list(range(2,10))
        lis=sample(lis,3); lis.sort(); lis*=2
        for i in range(3): lis[i+3]=deta%lis[i]
        n=lcm(lis[:3])
        print("A number between 9 and {} divided by {} {} and {} gives remainders {} {} and {}".format(n if n<100 else 100,lis[0],lis[1],lis[2],lis[3],lis[4],lis[5]))
        deta%=n
        n=0
        while n!=deta:
            n=eval(input("What is the number? "))
            if n==deta: print(n,"is Correct")
            else: print(n, "is Incorrect")

def mindread():
    """Pick a number between 1-25 and pick row numbers. Prepare to have your 'mind' 'read'"""
    print('row1: 06 11 01 21 16\nrow2: 12 07 02 22 17\nrow3: 23 13 08 18 03\nrow4: 19 14 09 04 24\nrow5: 10 05 20 15 25')
    a=eval(input('row number of location of your number: '))
    print('row1: 05 02 04 03 01\nrow2: 09 07 08 06 10\nrow3: 13 12 11 15 14\nrow4: 20 17 19 16 18\nrow5: 22 25 21 24 23')
    b=eval(input('new row number of location of your number: '))
    print('{0} and {2} were your rows. \n{0}-5={1}; {2}*5={3}; \n{1}+{3}='.format(a,a-5,b,b*5))
    return a-5+b*5

def zombie():
    """Survive the zombieapocalypse"""
    print('In order to choose a path use keyboard then click enter')
    name=input("What is your partner's name? ")
    #Scene 1:
    print("\nIt's the zombieapocalypse, only you and %s survive"%name)
    if input("Choose your weapon (1-Chainsaw)(2-Sniper Rifle): ")[0] in '1cC': #Chain
        print("\nYou go out with %s and give them one of your chainsaws, you start killing zombies."%name)
        side=input("What side is %s on? (1-Left)(2-Right): "%name)
        slic=input("Which way do you slice? (1-Left to Right)(2-Right to Left): ")
        if side[0]!=slic[0]: #Slice
            print("\nYou killed {0} by slicing towards them.\nWithout {0}'s help you hopelessly surrender your brains to the zombies".format(name))
            return
    else: #Rifle
        print("\nYou and %s have rifles, you are making headshots, you remember you are hungry, you see a hamburger"%name)
        if input("Do you go get the hamburger? (1-Yes)(2-No): ")[0] in '1yY': #Eat
            print("\nYou tell {0} to cover you while you go outside and eat\nThe burger of doom makes you into a zombie, so {0} kills you thinking you are a zombie".format(s))
            return
        else: #No eat
            print("\nYou and %s run out of bullets"%name)
            if input("What do you do? (1-Stand Still)(2-Hit zombies with gun)(3-Falcon Pawnch zombies): ")[0] in '1sS':
                print("\nMiraculously the zombies are moving so fast that they run into the opposite wall\nThe wall collapses and kills all the zombies")
            else: #Fail
                print("\nYou and %s fight bravely but you cannot simply kill zombies without a weapon")
                return
    #Scene 2: 
    print("\nYou and %s killed all the zombies in sight"%name)
    wachado=input("What do you do now? (1-Find food)(2-Sleep): ")
    if wachado[0] in '1fF': #Food
        print("\nYou go outside and see a burger just sitting there")
        eaty=input("Do you eat the burger? (1-Yes)(2-No): ")
        if eaty[0] in '1yY': #eaty
            print("\nIf you don't know this: the burger is tainted, anyone that eats it becomes a zombie\nyou can guess what %s did when he saw a random zombie"%name)
            return
        else: #no eaty
            print("\nYou keep walking and see water")
            if input("Do you want the water? (1-Yes)(2-No): ")[0] in '1yY':
                print("\nYou want the water but it is just a mirage, disappointed you go to a weapons store")
            else: print("\nYou give up the search for food and go to a weapons shop")
    else: #Sleep
        print("You and %s go to sleep, you hear something approaching"%name)
        input("What do you think it is? (1-Dog)(2-Zombie): ")
        print("\nWRONG. Kinda. It's a zomdog.")
        if input("What do you want to do with it? (1-Kill it)(2-Develop a cure): ")[0] in '2dD': #Cure
            print("\nYou are not smart enough to develop cure, and the dog killed you while you weren't paying attention")
            return
        else: print("\nGood you killed the cute zomdog, so with your life you go to a weapon")
    #Scene 3:
    print("\nYou realize that because the zombies are technically humans\nthey will soon learn to use tools (Like chainsaws)")
    if input("What do you do? (1-Fight)(2-Kill Yourself): ")[0] in '2kK': #Suicide
        print("\nYou kill yourself succesfully and %s dies of depression"%name)
        return
    else: #Fight
        print("\nIn the weapon place you find new weapons")
        wep2 = input("What weapon do you want? (1-Katana)(2-Automatic Weapons)(3-Soda Cans): ")[0]
        if wep2 in '1kK': #Katana
            print("\nSeems like you forgot that the zombies would learn to use chainsaws. chainsaws>swords")
            return
        elif wep2 in '2aA': #Guns
            print("\nYou take your guns and like always guns ran out of bullets and there is no escape")
            return
        else: #Soda
            print('\nWith the chainsaw zombies approching you look at the soda that says "Shake and Throw"')
            if input("Do you listen to the soda? (1-Yes)(2-No): ")[0] in '2nN': #No Soda
                print("Are you crazy being indecisive in a war gets you killed by chainsaw zombies")
                return
            else: print('''You shake the soda and throw it releasing an explosion that seems impossible for soda to contain
The soda seems to be melting the dead flesh of the zombies
Soon after this incident you decide to create a carbonated bomb.
You and %s kill all the zombies in the world. Yay!'''%name)


def ultrps(rounds):
    """Play of game of ultimate rock paper scissors
    
    Usage:
        ultrps(5) --> 5 rounds of ultimate rock paper scissors
    """
    armytable=[[ 0, 1,-1, 1,-1],
               [-1, 0, 1,-1, 1],
               [ 1,-1, 0, 1,-1],
               [-1, 1,-1, 0, 1],
               [ 1,-1, 1,-1, 0]]
    sub={'':['nature','characters','tools','animals','monsters'],
         'characters':['sciencey','heroic','piratey'],
         'nature':['hot','cold','wet'],
         'monsters':['deathlike','mythological','legendary'],
         'animals':['cute','horned','scaly'],
         'tools':['sharp','artful','strong'],
         'sciencey':['kirk','jekyll','spock'],
         'heroic':['gandalf','green lantern','wonder woman'],
         'piratey':['hook','black beard','jack sparrow'],
         'hot':['meteor','lava','fire'],
         'cold':['hail','blizzard','ice'],
         'wet':['hurricane','tsunami','water'],
         'deathlike':['reaper','zombie','vampire'],
         'mythological':['hydra','basilisk','cerberus'],
         'legendary':['centaur','werewolf','minotaur'],
         'cute':['rabbit','gerbil','mouse'],
         'horned':['rhino','unicorn','elephant'],
         'scaly':['dinosaur','snake','lizard'],
         'sharp':['knife','sword','scissor'],
         'artful':['pen','marker','paper'],
         'strong':['pistol','grenade','rock']}
    tries,wins,compwins=0,0,0
    for i in range(rounds):
        while 1:
            if tries%3==0: army=''
            tries+=1
            armies = sub[army]
            for i in armies: print(i.capitalize(),end=' '*5+'\n')
            lis=[i[1:3] for i in armies]
            out=input('pick an army: ')[1:3]
            while not (out in lis): out=input('Typing error: try again: ')[1:3]
            ar_my,comp_arm = lis.index(out),randrange(len(armies)) 
            army,comparm = armies[ar_my],armies[comp_arm]
            print('You picked', army)
            print('Comp randomly picked', comparm)
            num = armytable[ar_my][comp_arm]
            if num==1:
                print('%s beats %s; you win'%(army,comparm))
                wins+=1
            elif num==-1:
                print('%s beats %s; you lose'%(comparm,army))
                compwins+=1
            if num!=0:
                print()
                break
            else: print("Let's try again")
    return "You won {:.1%} of the games".format(wins/rounds)



class R:
    _all = ['ppl','wps','rms']
    num = 22
    ppl = ['alex','ann','bill','bob','cindy','cris','eve','eric','flora','gary','joe','jane','jesus','kim','liza','ned','pat','ryan','robin','sam','scott','ted']
    wps = ['allergy','axe','bag','banana','bat','bible','dart','gun','hands','knife','pillow','poison','rope','scissors','shoe','sword','syringe','vase']
    rms = ['attic','basement','bathroom','bedroom','cellar','diningroom','garage','guestroom','hallway','kitchen','laundry','library','livingroom','playroom','shed','wardrobe','yard']
    def __init__(self,num):
        from random import sample
        R.num = num
        R.ppl = sample(R.ppl,num)
        R.wps = sample(R.wps,num)
        R.rms = sample(R.rms,num)
    def get(s):
        if s in R._all: return eval('R.'+s)
        return False
    def items():
        for i in R._all: yield i,R.get(i)
    def randPpl(): return R.ppl[randrange(R.num)]
    def randWps(): return R.wps[randrange(R.num)]
    def randRms(): return R.rms[randrange(R.num)]
    def search(s):
        for i,j in R.items():
            for ss in j:
                if s[:4]==ss[:4]: return i,ss
def info():
    "Print all the good junk"
    print('''There are XxX Dead People
All you know is they only had XxX rooms and XxX weapons available
Make theories about the bodies, weapons, and rooms to get hints.
Ex: Bedroom Bob Eve Vase means you are looking at the Bedroom
For clues about if Bob was killed by Eve with a Vase there.
All people are victims. Not all rooms and weapons are used. 
'''.replace('XxX',str(R.num)))
    for s in ['People','Weapons','Rooms']: print((s+":").ljust(20),end=' ')
    for n in range(R.num):
        print('')
        for i,j in R.items(): print(j[n].ljust(20).title(),end=' ')
    print('')
#A little input thing that lets you write thing and it'll translate into 4 vars
def parse():
    "Analyses what you input according to the stuff you gave returns parsed input"
    def firstTag(tag,counter):
        for i in range(len(counter)):
            if tag==counter[i][0]:
                counter[i] = counter[i][1]
                return counter[i]
    print('='*25+' Theory '+'='*25) 
    counter = []
    while len(counter)==0:
        state=input('General statement: ').lower().strip()
        for i in state.split():
            parsed = R.search(i)
            if parsed: counter.append(parsed)   
        if len(counter)==0: print('BadInput')
    first = counter[0]
    a = firstTag('ppl',counter) or R.randPpl();b = firstTag('ppl',counter) or a
    c = firstTag('wps',counter) or R.randWps();d = firstTag('rms',counter) or R.randRms()
    if first[0]=='ppl'  : print('Theory While Looking @%s: killed by %s with %s in %s'%(first[-1].title(),b.title(),c.title(),d.title()))
    elif first[0]=='rms': print('Theory While Looking @%s: %s killed by %s with %s'%(first[-1].title(),a.title(),b.title(),c.title()))
    elif first[0]=='wps': print('Theory While Looking @%s: %s killed by %s in %s'%(first[-1].title(),a.title(),b.title(),d.title()))
    return a,b,c,d,first
def contain(first,answers):
    "gives one of answers containing the element given"
    try:
        where = R._all.index(first[0])+1
        if where<2: where-=1
    except: return [((None,None,None,None),-1)]
    ind = 0
    out = list()
    for i in answers:
        if i[where]==first[-1]: out.append((i,ind))
        ind += 1
    if len(out)==0: return [((None,None,None,None),-1)]
    return out
def hint(Ans,choice):
    "Returns dic of wrong ones"
    ans = Ans[0][0]
    if all(i==None for i in ans):
        try: print('%s is clean. No murder happened %s.'%(choice[-1][-1].title(),{'wps': 'with it', 'rms': 'here'}[choice[-1][0]]))
        except KeyError: print('You already figured out what happened to %s.'%choice[-1][-1].title()) #If on ppl that means you did it already
        return 0,((None,None),)
    types = {'wps': [0,1,3], 'rms': [0,1,2], 'ppl': [1,2,3]}
    correct = 0
    wrongs = []
    for i in types[choice[-1][0]]:
        if ans[i] == choice[i]: correct += 1
        else: wrongs.append((ans[i],i,choice[i]))
    if correct==3:
        print('='*23+' You got it '+'='*23)
        print('%s killed by %s with %s in %s'%tuple(i.title() for i in ans))
    else:
        if len(Ans)>1: print('%s murders happened %s. The more obvious one makes your theory have'%(len(Ans),{'wps': 'with this', 'rms': 'in here'}[choice[-1][0]]))
        print('%s of them are correct'%correct,end=' ')
        if correct!=0:
            from random import randrange
            a = randrange(len(wrongs))
            print('and %s is wrong as %s'%(wrongs[a][-1].title(),['Victim','Killer','Weapon','Room'][wrongs[a][1]]))
        else: print()
    return correct,wrongs
def murdergame(num=4):
    """Play this logic game of muhda (murder)"""
    R(num)
    answers = list((i,R.randPpl(),R.randWps(),R.randRms()) for i in set(R.ppl))
    saved = []
    info()
    cor = 0
    loop = 0
    try:
        while len(answers)>0:
            choice = parse()
            ans = contain(choice[-1],answers)
            cor,wrong = hint(ans,choice)
            loop += 1
            if cor==3:
                saved.append(answers.pop(ans[0][-1]))
                if len(answers)>0: print('Only %s more to go'%len(answers))
    except KeyboardInterrupt: pass
    print('It took you',loop,'hint%s'%('s' if loop!=1 else ''),'to solve')
    print('='*17+' Murders are as follows '+'='*17)
    for a,b,c,d in answers+saved: print('%s killed by %s with %s in %s'%(a.title(),b.title(),c.title(),d.title()))