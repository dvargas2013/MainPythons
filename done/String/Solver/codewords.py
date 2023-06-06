"""
the goal is identifying positions on a 5x5 board embedded in a word
at most 10 points in a 5x5 board

my first idea is using %5 with the letters
so willow would extract: 23 9 12 12 15 23 and then 4 5 3 3 1 4
maybe I want to combine em from the outsides so: 4,4 5,1 3,3
"""

from done.String.Solver import loadDictionary
from done.List import CollisionDictOfLists, batch


def pairs(letters):
    return set(map(tuple, batch((letters[:-1] if len(letters) % 2 else letters), 2)))


def convert(word):
    return tuple(sorted(pairs([1 + (ord(c) - ord('a') + 1) % 5 for c in word])))


def convert_words(dictionary_set=None):
    if dictionary_set is None:
        from done.String.Solver import masterDictionary
        dictionary_set = set(map(str.lower, masterDictionary))

    dictionary_set = set(word.lower() for word in dictionary_set if len(word) > 1)

    return dict(CollisionDictOfLists((convert(word), word) for word in dictionary_set))


def words_to_finder(words):
    return dict(CollisionDictOfLists((_tuple, _list) for _list in words for _tuple in _list))


def incorporate_bomb(find, bomb):
    find = find.copy()  # shallow copy is enough
    v = set(find.pop(bomb))
    for k in find:
        # assumes that only shallow copy was made, so you need to make a new list
        find[k] = [i for i in find[k] if i not in v]
    return find


def keyify(i, j):
    if type(i[0]) != tuple:
        i = i,
    if type(j[0]) != tuple:
        j = j,
    return tuple(sorted((*i, *j)))


def optimal_coding(codepoints, find):
    find = {cp: set(find[cp]) for cp in codepoints}
    if not find: return {}

    find2 = {}
    for i in find:
        for j in find:
            if i is j: continue
            find2[keyify(i, j)] = find[i] & find[j]
    if not find2: return find

    find3 = {}
    for i in find2:
        for j in find:
            if j in i: continue
            find3[keyify(i, j)] = find2[i] & find[j]
    if not find3: return find2

    while True:
        find2 = find3
        find3 = {}
        for i in find2:
            for j in find:
                if j in i: continue
                x = find2[i] & find[j]
                if x:
                    find3[keyify(i, j)] = x
        if not find3: return find2


if __name__ == '__main__':
    loadDictionary("../../usrsharedictweb2")
    _words = convert_words()
    _find = words_to_finder(_words)

    import random

    r = lambda: random.randint(1, 5)
    N = 10
    oc = {(r(), r()) for _ in range(N)}
    print(oc)
    _find2 = optimal_coding(oc, _find)
    if len(_find2) == 1:
        only_find_key, only_find_val = next(iter(_find2.items()))
        print(only_find_key)
        _ = any(map(print, sorted(_words[only_find_key], key=lambda x: len(x))))
    else:
        ks = sorted(_find2, key=lambda x: len(_find2[x]))
        for k in ks:
            print(k, len(_find2[k]))
        find_key = next(iter(ks))
        _ = any(map(print, sorted(_words[find_key], key=lambda x: len(x))))
