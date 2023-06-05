"""Solvers that take in a text-like input or require the use of a word-based dictionary"""

from collections import Counter
from functools import partial
from itertools import product
from re import compile
from string import ascii_lowercase

from done.String.Solver.chemistry import chemistry
from done.String.Solver.connect import connectWords

ascii_lowercase_set = set(ascii_lowercase)
masterDictionary = set()


def loadDictionary(dictionary_file='/usr/share/dict/web2'):
    masterDictionary.clear()
    with open(dictionary_file) as f:
        masterDictionary.update(set(f.read().split()))


def anagram(jumbled_word, dictionary_set=None):
    """Yields anagram matches that contain the letters in jumbled_word"""
    jumbled_word = jumbled_word.lower()
    letters = set(jumbled_word)
    if dictionary_set is None:
        dictionary_set = set(map(str.lower, masterDictionary))

    # letters that are not allowed
    hbl = compile("[%s]" % ''.join(ascii_lowercase_set.difference(letters)))

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


def clues22(pairs, dictionary_set=None):
    """rearrange substrings to create a word in the dictionary file

Usage:
    clues22(['he','ll','be','o']) -> list containing "hello" and "bell"
"""
    pairs = [i.lower() for i in pairs]
    if dictionary_set is None:
        dictionary_set = set(map(str.lower, masterDictionary))

    all_letters = ''.join(pairs)

    assemble_with_given_pairs = partial(assemble, pieces=pairs)
    yield from filter(assemble_with_given_pairs, anagram(all_letters, dictionary_set=dictionary_set))


def oneLetterFromEach(*strings, dictionary_set=None):
    """picks one letter from each string and rearranges it to make words

Usage:
    oneLetterFromEach(["t","hx","ea"]) -> ["the","het","hat","tax",...]
    """
    if dictionary_set is None:
        dictionary_set = set(map(str.lower, filter((lambda i: len(i) == len(strings)), masterDictionary)))

    for p in product(*strings):
        yield from anagram("".join(p), dictionary_set=dictionary_set)


def createWordsViaDeletion(big_word, dictionary=None):
    if dictionary is None:
        dictionary = sorted(map(str.lower, masterDictionary), reverse=True, key=len)

    big_word = "".join(i for i in big_word.lower() if i.isalpha())
    big_word_set = set(big_word)
    big_word_counter = Counter(big_word)

    def checkword():
        if not big_word_set.issuperset(word): return False
        c = Counter(word)
        if any(c[k] > i for k, i in big_word_counter.items()): return False
        i = 0
        for L in word:
            i = big_word.find(L, i)
            if i == -1: return False
        return True

    for word in dictionary:
        if checkword(): yield word
