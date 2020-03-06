"""Solvers that take in a text-like input or require the use of a word-based dictionary"""
import re
from string import ascii_lowercase
from functools import partial
from . import String
import random

printAll = print_iterable = String.print_iterable

ascii_lowercase_set = set(ascii_lowercase)


def chemistry(text="Hello World", showall=False):
    """Given a sentence will try to recreate string with chemistry symbols"""

    # without j and q the algorithm would get stuck
    def splitTarget(target, word):
        target, word = target.lower(), word.lower()
        grow = ''
        for c in word:
            if target[:1] == c:
                grow += target[:1]
                target = target[1:]
        return grow, target

    def perfLvl(gem, aim):
        if len(gem) == 1: return 2
        for i in range(len(gem), 0, -1):
            if gem[:i].lower() == aim[:i].lower(): return 2 * i - 1
        return 0

    Gems = ['j*', 'q*', 'H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl',
            'Ar', 'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br',
            'Kr', 'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I',
            'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu',
            'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac',
            'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh',
            'Hs', 'Mt', 'Ds', 'Rg', 'Cn', 'Uut', 'Fl', 'Uup', 'Lv', 'Uus', 'Uuo']
    UseGems = dict()  # grab the gems that are possible to use

    def expandWord(word, target):
        first, last = splitTarget(target, word)
        tLetter = last[:1]
        if not tLetter: return
        save = dict((word + i, perfLvl(i, last)) for i in UseGems[tLetter])
        M = 1 if 2 in save.values() else 0
        return [i for i in save if save[i] > M]

    def yieldMaximums(words, target, M=.5, show=0):
        returnable = dict()
        for w in list(words):  # For every word in that list
            if show: print("\t" * (show - 1) + "LOOP " + repr(w))
            words = expandWord(w, target)  # Add symbols if you can
            if show and words: print("\t" * (show - 1) + str(words))
            if words:  # If words have been added go deeper
                words, M = yieldMaximums(words, target, M, 0 if not show else show + 1)
                returnable.update(dict((word, words[word]) for word in words if words[word] >= M))
            else:
                s = String.score(target, w)
                if s >= M:
                    M = s
                    returnable.update({w: s})
                    if show: print("\t" * (show - 1) + str({w: s}))
        for w in list(returnable.keys()):
            if returnable[w] != M: returnable.pop(w)
        if show and returnable: print("\t" * (show - 1) + "RETURN " + str(returnable))
        return returnable, M

    def chems(target, debug=0):
        save = yieldMaximums([''], target, show=debug)
        return list(save[0]), save[-1]

    for i in range(ord('a'), ord('z') + 1):
        i = chr(i)
        lis = UseGems.get(i, list())
        if not lis: UseGems[i] = [g for g in Gems if i in g[:1].lower()]
    string = ''
    for word in text.lower().split():
        word = ''.join(c for c in word if c.isalpha())
        chem, num = chems(word)
        if showall: print(num, chem)
        chem = random.choice(chem)
        string += chem + ' '
    return string


def anagram(jumbled_word, dictionary_file='/usr/share/dict/web2', dictionary_set=None):
    """Yields anagram matches that contain the letters in jumbled_word

if dictionary_set is defined, will not use the dictionary_file
anything yielded will be a word in the dictionary_file (lowercase, whitespace-split)
"""
    jumbled_word = jumbled_word.lower()
    letters = set(jumbled_word)
    if dictionary_set is None:
        with open(dictionary_file) as f:
            dictionary_set = set(f.read().lower().split())

    # letters that are not allowed
    hbl = re.compile("[%s]" % ''.join(ascii_lowercase_set.difference(letters)))

    # count the letters that are allowed
    count = dict((i, jumbled_word.count(i)) for i in letters)

    def less_than_count(test_string):
        """return true if test_string is allowed based on the amount of the letters it has"""
        return all(test_string.count(i) <= count.get(i, 0) for i in set(test_string))

    yield from sorted(sorted(filter(
        lambda x: (len(x) > 2 and not hbl.search(x) and less_than_count(x)),
        dictionary_set)), key=len)


def assemble(word, pieces):
    """returns whether word can be assembled from the pieces (no repeats)"""
    if len(word) == 0: return True
    for piece in pieces:
        if word.startswith(piece):  # for every piece that starts correctly
            temp = list(pieces)
            temp.remove(piece)
            # if the next part can be assembled with the remaining pieces
            if assemble(word[len(piece):], temp): return True
    return False


def clues22(pairs, dictionary_file='/usr/share/dict/web2'):
    """rearrange substrings to create a word in the dictionary file

Usage:
    clues22(['he','ll','be','o']) -> list containing "hello" and "bell"
"""
    pairs = [i.lower() for i in pairs]
    with open(dictionary_file) as f:
        dictionary = set(f.read().lower().split())
    all_letters = ''.join(pairs)

    assemble_with_given_pairs = partial(assemble, pairs=pairs)
    yield from filter(assemble_with_given_pairs, anagram(all_letters, dictionary_set=dictionary))


def oneLetterFromEach(*strings, dictionary_file='/usr/share/dict/web2'):
    """picks one letter from each string and rearranges it to make words

Usage:
    oneLetterFromEach(["t","hx","ea"]) -> ["the","het","hat","tax",...]
    """
    from itertools import product

    with open(dictionary_file) as f:
        dictionary = set(i for i in f.read().lower().split() if len(i) == len(strings))

    for p in product(strings):
        yield from anagram("".join(p), dictionary_set=dictionary)


def offByOne(word1, word2):
    """Measure how many letters off the strings are
returns true if you could change a single symbol to get the other one
or if you could add or remove a symbol to get the other one"""
    n = abs(len(word1) - len(word2))
    if n > 1: return False
    for w1, w2 in zip(word1, word2):
        if n > 1: return False
        if w1 != w2: n += 1
    return n == 1


def connectWords(word1, word2, dictionary_file='/usr/share/dict/web2'):
    """changes 1 letter at a time until word1 becomes word2"""
    if len(word1) != len(word2): return
    length = len(word1)
    word1 = word1.lower()
    word2 = word2.lower()
    from heapq import heappop, heappush

    with open(dictionary_file) as f:
        unvisited = set(i for i in f.read().lower().split() if len(i) == length)

    def getNeighbors(word, remove=0):
        """finds words in the unvisited list as long as they're off by 1 letter"""
        for w in list(unvisited):
            if offByOne(w, word):
                if remove: unvisited.remove(w)
                yield w

    queue = [(1, w, [word1]) for w in getNeighbors(word1, remove=1)]
    goals = set(getNeighbors(word2))
    m = len(unvisited)
    if not len(queue) or not len(goals): return
    while len(unvisited) != 0 and len(queue) != 0:
        dist, word, rest = heappop(queue)
        if dist > m: continue
        if word in goals:
            yield rest + [word, word2]
            m = dist
        else:
            for neigh in getNeighbors(word, remove=1):
                heappush(queue, (dist + 1, neigh, rest + [word]))


def db_test(alphabet='acbef', length=5):
    """Test for the DeBruijn generator"""
    from List import window
    seq = DeBruijn(alphabet, length)
    seq += seq[:length]
    store = set(window(seq, length))
    assert len(store) == len(set(alphabet)) ** length  # Check that all possible arrangements of length were added
    print("Assertion Passed")


def DeBruijn(alphabet, length):
    """Given an alphabet and substring length construct a DeBruijn Sequence"""
    alphabet = ''.join(sorted(set(alphabet)))
    allen = len(alphabet)

    wordx = int(allen ** (length - 1))  # calculate the multiplier for the alphabet

    def word(i):
        """gets a letter from the alphabet based on the index provided"""
        return alphabet[i // wordx]  # 111222333

    def mapper(n):
        """maps corresponding items into lyndon cycles"""
        return n // wordx + (n % wordx) * allen

    def db():
        visited = [False] * (allen * wordx)
        for i in range(allen * wordx):
            if visited[i]:
                continue  # If a cycle has visited this node then it's not the lexicographic rotation minimum
            lyndon = word(i)
            j = mapper(i)
            while j != i:
                visited[j] = True
                lyndon += word(j)
                j = mapper(j)
            yield lyndon

    return ''.join(db())
