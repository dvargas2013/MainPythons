"""Contains fun stuff you can do with my computer 'cause of skills

ProTip: a lot of the games can be hacked by typing giveup in em c;"""

from random import randint, randrange, shuffle, sample, choice

try:
    from .List import lcm
except ImportError:
    from List import lcm

def matrix(mini=-1, maxi=1):
    """print random integers between min and max... never stops"""
    while 1: print(randint(mini, maxi), end='')


def multiplication(digits1=2, digits2=2):
    """Give will ask you to multiply number of digit
    
Usage:
    _(2,3) = 2 digit number * 3 digit number = ?
    """
    while True:
        x = randrange(10 ** (digits1 - 1), 10 ** digits1)
        y = randrange(10 ** (digits2 - 1), 10 ** digits2)
        giveup = x * y
        while True:
            try:
                c = eval(input(str(x) + '*' + str(y) + '=?: '))
            except KeyboardInterrupt:
                return
            if c == giveup:
                print(c, 'is Correct')
                break
            else:
                print(c, 'is Wrong')


def pattern(multiplicand=10, multiplier=4, addend=4, hint_amount=3):
    """Gives a pattern that multiplies by a num then adds by another num repeatedly
Please only put in positive integers
Keyboard Interrupt to exit
"""
    if hint_amount < 3: hint_amount = 3
    lis = list(range(hint_amount + 1))
    while 1:
        giveup, dif, mul = 0, 0, 0
        while giveup == 0: giveup = randint(-multiplicand, multiplicand)
        while mul == 0: mul = randint(-multiplier, multiplier)
        while dif == 0: dif = randint(-addend, addend)
        lis[0] = giveup
        for b in range(hint_amount): giveup, lis[b + 1] = mul * giveup + dif, mul * giveup + dif
        q = giveup - 1
        while q != giveup:
            for b in range(hint_amount): print(lis[b])
            try:
                q = eval(input('Next number is: '))
            except KeyboardInterrupt:
                return
            if q == giveup:
                print(q, 'is correct')
            else:
                print(q, 'is wrong')


def physics():
    """Asks newtonian physics questions on acceleration, time, velocity and distance"""

    def problem(*stuff, info='', giveup=0):
        while 1:
            print(X.format(*stuff))
            try:
                loop = eval(input(info))
            except KeyboardInterrupt:
                return -1
            if loop != giveup:
                print("{} is Incorrect".format(loop))
            else:
                break
        print("{} is Correct\n=====NewProblem=====".format(loop))

    X = '\n{} {}\n{} {}\n{} {}'
    A, VI, T, D, VF = 'Acceleration:', 'Initial Speed:', 'Time:', 'Distance:', 'Final Speed:'
    while 1:
        a, vi, t, d, c = randint(1, 6), randrange(10), randint(1, 8), 5 * randrange(13), randrange(5)
        vf = randint(vi, 10)
        if c == 0:
            c = problem(VI, vi, T, t, A, a, info=D + ' ', giveup=vi * t + .5 * a * t ** 2)
        elif c == 1:
            c = problem(VF, vf, VI, vi, A, a, info=D + ' ', giveup=(vf * vf - vi * vi) / (2 * a))
        elif c == 2:
            c = problem(VI, vi, A, a, D, d, info=VF + ' ', giveup=(vi * vi + 2 * a * d) ** .5)
        elif c == 3:
            c = problem(VI, vi, A, a, T, t, info=VF + ' ', giveup=vi + a * t)
        else:
            c = problem(VF, vf, VI, vi, A, a, info=T + ' ', giveup=(vf - vi) / a)
        if c == -1: return


def thinker():
    """Logic game with remainders"""
    while 1:
        giveup, lis = randint(10, 99), list(range(2, 10))
        lis = sorted(sample(lis, 3))
        lis *= 2
        for i in range(3): lis[i + 3] = giveup % lis[i]
        n = lcm(lis[:3])
        print("A number between 9 and {} divided by {} {} and {} gives remainders {} {} and {}".format(
            n if n < 100 else 100, lis[0], lis[1], lis[2], lis[3], lis[4], lis[5]))
        giveup %= n
        n = 0
        while n != giveup:
            try:
                n = eval(input("What is the number? "))
            except KeyboardInterrupt:
                return
            if n == giveup:
                print(n, "is Correct")
            else:
                print(n, "is Incorrect")


def number_guesser1():
    """find the row ur number is in twice. i will figure out the number"""
    print("Pick a number between 1-25 and pick row numbers.\nPrepare to have your 'mind' 'read'\n")
    print(
        'row1: 06 11 01 21 16\nrow2: 12 07 02 22 17\nrow3: 23 13 08 18 03\nrow4: 19 14 09 04 24\nrow5: 10 05 20 15 25')
    a = int(input('row number of location of your number: '))
    print(
        'row1: 05 02 04 03 01\nrow2: 09 07 08 06 10\nrow3: 13 12 11 15 14\nrow4: 20 17 19 16 18\nrow5: 22 25 21 24 23')
    b = int(input('new row number of location of your number: '))
    print('{0} and {2} were your rows. \n{0}-5={1}; {2}*5={3}; \n{1}+{3}='.format(a, a - 5, b, b * 5))
    return a - 5 + b * 5


def number_guesser2():
    """i will generate 5 lists. just say whether ur number is in there or not"""
    print("Pick an integer between 1-32 and say yes or no if it's in the list.\nPrepare to have your 'mind' 'read'\n")
    a = 0
    for n in [1 << N for N in range(5)]:
        print(" ".join(str(i) for i in range(1, 32) if i & n))
        while 1:
            s = input("Does your number appear in this list? ")
            if s: s = s[0].lower()
            if s == "y":
                a += n
                print("YES")
                break
            elif s == "n":
                print("NO")
                break
            else:
                print("I didn't understand that. Please respond with yes or no.")
    print("Your Number Is: %s" % a)


def number_guesser3():
    """open up a calculator and do the thing"""
    print("pick a positive integer. any will do")
    input("press enter when you've chosen...")

    print("multiply it by 18")
    input("press enter when you've multiplied...")

    print("remove a non zero digit to be your secret digit")
    print("gimme all the other numbers left")
    print("example: if your number is 1571, and you pick the digit 1, gimme '715' in any order")

    print(f"your secret number is {9 - sum(map(int, input(': '))) % 9}")

def zombie():
    """Survive the zombie apocalypse"""
    print('In order to choose a path use keyboard then click enter')
    name = input("What is your partner's name? ")
    # Scene 1:
    print("\nIt's the zombie apocalypse, only you and %s survive" % name)
    if input("Choose your weapon (1-Chainsaw)(2-Sniper Rifle): ")[0] in '1cC':  # Chain
        print("\nYou go out with %s and give them one of your chainsaws, you start killing zombies." % name)
        if input("What side is %s on? (1-Left)(2-Right): " % name)[0] != \
                input("Which way do you slice? (1-Left to Right)(2-Right to Left): ")[0]:  # Slice
            return print("""
You killed {0} by slicing towards them.
Without {0}'s help you hopelessly surrender your brains to the zombies""".format(name))
    else:  # Rifle
        print("""
You and %s have rifles, you are making head-shots, you remember you are hungry, you see a hamburger""" % name)
        if input("Do you go get the hamburger? (1-Yes)(2-No): ")[0] in '1yY':  # Eat
            return print("""
You tell {0} to cover you while you go outside and eat
The burger of doom makes you into a zombie, so {0} kills you thinking you are a zombie""".format(name))
        else:  # No eat
            print("\nYou and %s run out of bullets" % name)
            if input("What do you do? (1-Stand Still)(2-Hit zombies with gun)(3-Falcon Punch zombies): ")[0] in '1sS':
                print("""
Miraculously the zombies are moving so fast that they run into the opposite wall
The wall collapses and kills all the zombies""")
            else:  # Fail
                return print("\nYou and %s fight bravely but you cannot simply kill zombies without a weapon")
    # Scene 2:
    print("\nYou and %s killed all the zombies in sight" % name)
    if input("What do you do now? (1-Find food)(2-Sleep): ")[0] in '1fF':  # Food
        print("\nYou go outside and see a burger just sitting there")
        if input("Do you eat the burger? (1-Yes)(2-No): ")[0] in '1yY':  # eat
            return print("""
If you don't know this: the burger is tainted, anyone that eats it becomes a zombie
you can guess what %s did when they saw a random zombie""" % name)
        else:  # no eat
            print("\nYou keep walking and see water")
            if input("Do you want the water? (1-Yes)(2-No): ")[0] in '1yY':
                print("\nYou want the water but it is just a mirage, disappointed you go to a weapons store")
            else:
                print("\nYou give up the search for food and go to a weapons shop")
    else:  # Sleep
        print("You and %s go to sleep, you hear something approaching" % name)
        input("What do you think it is? (1-Dog)(2-Zombie): ")
        print("\nWRONG. Kinda. It's a zomdog.")
        if input("What do you want to do with it? (1-Kill it)(2-Develop a cure): ")[0] in '2dD':  # Cure
            return print(
                "\nYou are not smart enough to develop cure, and the dog killed you while you weren't paying attention")
        else:
            print("\nGood you killed the cute zomdog, so with your life you go to a weapon")
    # Scene 3:
    print("""
You realize that because the zombies are technically humans
they will soon learn to use tools (Like chainsaws)""")
    if input("What do you do? (1-Fight)(2-Kill Yourself): ")[0] in '2kK':  # Suicide
        return print("\nYou kill yourself successfully and %s dies of depression" % name)
    else:  # Fight
        print("\nIn the weapon place you find new weapons")
        _ = input("What weapon do you want? (1-Katana)(2-Automatic Weapons)(3-Soda Cans): ")[0]
        if _ in '1kK':  # Katana
            return print("\nSeems like you forgot that the zombies would learn to use chainsaws. chainsaws>swords")
        elif _ in '2aA':  # Guns
            return print("\nYou take your guns and like always guns ran out of bullets and there is no escape")
        else:  # Soda
            print('\nWith the chainsaw zombies approaching you look at the soda that says "Shake and Throw"')
            if input("Do you listen to the soda? (1-Yes)(2-No): ")[0] in '2nN':  # No Soda
                return print("Are you crazy!? Being indecisive in a war gets you killed by chainsaw zombies")
            else:
                print(
                    '''You shake the soda and throw it releasing an explosion that seems impossible for soda to contain
The soda seems to be melting the dead flesh of the zombies
Soon after this incident you decide to create a carbonated bomb.
You and %s kill all the zombies in the world. Yay!''' % name)


def ultimate_rps(rounds=5):
    """Play of game of ultimate rock paper scissors
    
    Usage:
        ultrps(5) --> 5 rounds of ultimate rock paper scissors
    """
    armytable = [[0, 1, -1, 1, -1],
                 [-1, 0, 1, -1, 1],
                 [1, -1, 0, 1, -1],
                 [-1, 1, -1, 0, 1],
                 [1, -1, 1, -1, 0]]
    sub = {'': ['nature', 'characters', 'tools', 'animals', 'monsters'],
           'characters': ['sciencey', 'heroic', 'piratey'],
           'nature': ['hot', 'cold', 'wet'],
           'monsters': ['deathlike', 'mythological', 'legendary'],
           'animals': ['cute', 'horned', 'scaly'],
           'tools': ['sharp', 'artful', 'strong'],
           'sciencey': ['kirk', 'jekyll', 'spock'],
           'heroic': ['gandalf', 'green lantern', 'wonder woman'],
           'piratey': ['hook', 'black beard', 'jack sparrow'],
           'hot': ['meteor', 'lava', 'fire'],
           'cold': ['hail', 'blizzard', 'ice'],
           'wet': ['hurricane', 'tsunami', 'water'],
           'deathlike': ['reaper', 'zombie', 'vampire'],
           'mythological': ['hydra', 'basilisk', 'cerberus'],
           'legendary': ['centaur', 'werewolf', 'minotaur'],
           'cute': ['rabbit', 'gerbil', 'mouse'],
           'horned': ['rhino', 'unicorn', 'elephant'],
           'scaly': ['dinosaur', 'snake', 'lizard'],
           'sharp': ['knife', 'sword', 'scissor'],
           'artful': ['pen', 'marker', 'paper'],
           'strong': ['pistol', 'grenade', 'rock']}
    tries, wins, compwins = 0, 0, 0
    print("Use Quit to end game in a pinch")
    army = ''
    for i in range(rounds):
        while 1:
            armies = sub.get(army, sub[''])
            for army in armies: print(army.capitalize(), end=' ' * 5 + '\n')
            lis = [army[1:3] for army in armies] + ["ui"]
            out = input('pick an army: ')[1:3]
            while not (out in lis): out = input('Typing error: try again: ')[1:3]
            if out.lower() == 'ui': return
            ar_my, comp_arm = lis.index(out), randrange(len(armies))
            army, comparm = armies[ar_my], armies[comp_arm]
            print('You picked', army)
            print('Comp randomly picked', comparm)
            num = armytable[ar_my][comp_arm]
            if num == 1:
                print('%s beats %s; you win' % (army, comparm))
                wins += 1
            elif num == -1:
                print('%s beats %s; you lose' % (comparm, army))
                compwins += 1
            if num != 0:
                print()
                break
            else:
                print("Let's try again")
    return "You won {:.1%} of the games".format(wins / rounds)


class Murder:
    """stores my static final variables for murder_game"""
    BODY, WEAPON, ROOM = range(3)
    names = ['alex', 'ann', 'bill', 'bob', 'cindy', 'cris', 'eve', 'eric', 'flora', 'gary', 'joe', 'jane', 'jesus',
             'kim', 'liza', 'ned', 'pat', 'ryan', 'robin', 'sam', 'scott', 'ted']
    weapons = ['allergy', 'axe', 'bag', 'banana', 'bat', 'bible', 'dart', 'gun', 'hands', 'knife', 'pillow', 'poison',
               'rope', 'scissors', 'shoe', 'sword', 'syringe', 'vase']
    rooms = ['attic', 'basement', 'bathroom', 'bedroom', 'cellar', 'diningroom', 'garage', 'guestroom', 'hallway',
             'kitchen', 'laundry', 'library', 'livingroom', 'playroom', 'shed', 'wardrobe', 'yard']
    maximum_size = min(map(len, (names, weapons, rooms)))


def murder(amount_of_choice=4):
    """Play this logic game of murder"""
    amount_of_choice = min(Murder.maximum_size, amount_of_choice)

    def sample_stuff(x):
        """from the big list of stuff. picks some at random"""
        return [i.title() for i in sample(x, amount_of_choice)]

    names, weapons, rooms = map(sample_stuff, (Murder.names, Murder.weapons, Murder.rooms))
    get_type = {**{n: Murder.BODY for n in names},
                **{w: Murder.WEAPON for w in weapons},
                **{r: Murder.ROOM for r in rooms}}
    answers = [(i, choice(weapons), choice(rooms), choice(names)) for i in set(names)]
    victims = names.copy()

    print("Type 'quit' to stop game-loop\n")
    print("There are {0} Dead People\n"
          "All you know is they only had {0} rooms and {0} weapons available".format(amount_of_choice))
    print('''Make theories about the bodies, weapons, and rooms to get hints.
Ex: Bedroom Bob Eve Vase means you are looking at the Bedroom
For clues about if Bob was killed by Eve with a Vase there.
All bodies are involved in exactly 1 murder
but rooms and weapons might have been used multiple times.
In those cases, clues will be merged. Good luck separating them.\n''')
    print('{:20}{:20}{:20}'.format('People:', 'Weapons:', 'Rooms:'))
    for name, weapon, room in zip(names, weapons, rooms):
        print('{:20}{:20}{:20}'.format(name, weapon, room))

    def parse():
        """take in user input and return proper data"""
        while True:
            get_input = input('General statement: ').title().strip()
            if get_input.startswith('Q'): return
            get_input = [i for i in get_input.split() if i in get_type]
            if len(get_input):
                break
            else:
                print("Bad Input: use at least 1 person, weapon, or room")

        type_of_first = get_type[get_input[0]]
        p1 = p2 = None
        wep = choice(weapons)
        rom = choice(rooms)

        # if you do too many of something, it'll end up with the first one
        for noun in reversed(get_input):
            type_of_noun = get_type[noun]
            if type_of_noun == Murder.BODY:
                p1, p2 = noun, p1
            elif type_of_noun == Murder.ROOM:
                rom = noun
            elif type_of_noun == Murder.WEAPON:
                wep = noun

        if p1 is None:
            p1 = choice(victims)
            p2 = choice(victims)
        elif p2 is None:
            p2 = p1  # if p1 is set, you intended to search for suicide

        print('=' * 25 + ' Theory ' + '=' * 25)

        if type_of_first == Murder.BODY:
            print(f'Theory While Looking @{p1}: killed by {p2} with {wep} in {rom}')
        elif type_of_first == Murder.ROOM:
            print(f'Theory While Looking @{rom}: {p1} killed by {p2} with {wep}')
        elif type_of_first == Murder.WEAPON:
            print(f'Theory While Looking @{wep}: {p1} killed by {p2} in {rom}')
        else:
            return

        return p1, wep, rom, p2, type_of_first

    saved = []

    def construct_hint():
        """create a hint from user input"""
        guess_victim, guess_weapon, guess_room, guess_murderer, search_type = inputs
        search = inputs[search_type]  # parse out the search_type (aka the thing ur searching for clues)

        def answers_that_contain():
            """given the thing we're looking at, give us all the things that happened with it"""
            type_of_search = get_type[search]

            for answer in answers:
                if answer[type_of_search] == search:
                    yield answer

        possible_clues = list(answers_that_contain())

        if len(possible_clues) == 0:
            if search_type == Murder.BODY:  # no body is clean ... this means that you already figure out what happened
                print(f'You already figured out what happened to {guess_victim}.')
            else:
                _ = {Murder.WEAPON: "with it", Murder.ROOM: "here"}[search_type]
                print(f'{search} is clean. No murder happened {_}.')
                (rooms if search_type == Murder.ROOM else weapons).remove(search)
            return

        def get_scores():
            """get how many were correct for each of the clue stacks"""
            for xp1, xw, xr, xp2 in possible_clues:
                yield (guess_victim == xp1) + (guess_weapon == xw) + (guess_room == xr) + (guess_murderer == xp2) - 1

        scores = list(get_scores())

        # score can either be 0, 1, 2, or 3
        # if its 0 or 3, you don't need extra info
        # if its 1 correct, use get_correct
        # if its 2 correct, use get_wrong

        def get_correct():
            """get the clue that is not the search and is correct"""
            for z, i, j in zip(("Victim", "Weapon", "Room", "Killer"),
                               (guess_victim, guess_weapon, guess_room, guess_murderer),
                               clue):
                if i == j != search:
                    return z, i

        def get_wrong():
            """get the clue that is incorrect"""
            for z, i, j in zip(("Victim", "Weapon", "Room", "Killer"),
                               (guess_victim, guess_weapon, guess_room, guess_murderer),
                               clue):
                if i != j:
                    return z, i

        def correct_guess():
            """print information that you guessed correctly"""
            print('=' * 23 + ' You got it ' + '=' * 23)
            print(f'{guess_victim} was killed by {guess_murderer} with {guess_weapon} in {guess_room}')
            victims.remove(guess_victim)
            answers.remove(clue)
            saved.append(clue)
            print(f'Only {len(answers)} more Murders to solve')

        if len(possible_clues) == 1:
            clue = possible_clues[0]
            score = scores[0]

            if score == 3:
                if search_type == Murder.ROOM:
                    rooms.remove(search)
                elif search_type == Murder.WEAPON:
                    weapons.remove(search)
                return correct_guess()
            elif score == 0:
                print("You don't know what happened. But you do know that you got the clue completely wrong")
            elif score == 1:
                kind, word = get_correct()
                print(f"You had a good hunch that {word} was the {kind}. The other two were wrong tho.")
            else:  # elif score == 2:
                kind, word = get_wrong()
                print(f"Almost tracked everything down. However, {word} wasn't the {kind}")
            return

        # if you're down here its cause len > 1 and search_type > 0
        if search_type == Murder.BODY:
            raise Exception("search_type (BODY) cannot have multiple murders")

        _ = {Murder.WEAPON: "with this", Murder.ROOM: "here"}[search_type]
        print(f'{len(possible_clues)} different murders happened {_}.')

        if len(possible_clues) == len(answers):
            it = (rooms if search_type == Murder.ROOM else weapons)
            it.clear()  # i would use it = [search] but that shadows the variable and i cant use globals either
            it.append(search)

        if any(sc == 3 for sc in scores):
            for sc, clue in zip(scores, possible_clues):
                if sc == 3:
                    return correct_guess()

        def get_multi():
            """for each thing you guessed, try to find matches between all clues"""
            a = b = c = d = 0
            for w, x, y, z in possible_clues:
                a += (w == guess_victim)
                b += (x == guess_weapon)
                c += (y == guess_room)
                d += (z == guess_murderer)
            return a, b, c, d

        victim_mc, weapon_mc, room_mc, murderer_mc = multi_score = get_multi()
        assert multi_score[search_type] == len(possible_clues)

        print(f"While inspecting {search} you realized that: ")

        def murderer_clue():
            """creates clue associated with murderer guessed, in relationship to the search thing"""
            if murderer_mc:
                in_or_with = "in" if search_type == Murder.ROOM else "with"
                _ = "once" if murderer_mc == 1 else f"{murderer_mc} times"
                print(f"\t{guess_murderer} killed {in_or_with} {search} {_}")
            else:
                _ = {Murder.WEAPON: "didn't use", Murder.ROOM: "didn't kill in"}[search_type]
                print(f"\t{guess_murderer} {_} {search}")

        def victim_clue():
            """creates clue associated with victim guessed, in relationship to the search thing"""
            if search_type == Murder.WEAPON:
                _ = "" if victim_mc else "nt"
                print(f"\t{guess_weapon} was{_} used on {guess_victim}")
            else:  # elif search_type == Murder.ROOM
                _ = "died" if victim_mc else "didn't die"
                print(f"\t{guess_victim} {_} in {guess_room}")

        def not_search_clue():
            """creates clue associated with the other thing guessed, in relationship to the search thing"""
            not_search_type = Murder.WEAPON if search_type == Murder.ROOM else Murder.ROOM
            not_search = inputs[not_search_type]
            not_search_mc = multi_score[not_search_type]

            if not_search_mc == 0:
                _ = "in" if not_search_type == Murder.ROOM else "with"
                print(f"\t{search} was never used {_} {not_search}")
            elif weapon_mc == room_mc:
                print(f"\t{not_search} was used every time {search} was used")
            else:
                _ = "once" if not_search_mc == 1 else f"{not_search_mc} times"
                print(f"\t{search} was used in {not_search} {_}")

        clue_generators = [murderer_clue, victim_clue, not_search_clue]
        shuffle(clue_generators)
        for clue_gen in clue_generators:
            clue_gen()

    loop = 0
    while len(answers) > 0:

        try:
            inputs = parse()
        except KeyboardInterrupt:
            break
        if inputs is None: break
        construct_hint()
        loop += 1
    s = "" if loop == 1 else "s"
    print(f'It took you {loop} hint{s} to solve')
    print('=' * 17 + ' Murders are as follows ' + '=' * 17)
    for victim, murderer, weapon, room in answers + saved:
        print(f'{victim} was killed by {murderer} with {weapon} in {room}')
