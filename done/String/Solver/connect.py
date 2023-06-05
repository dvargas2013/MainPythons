from heapq import heappop, heappush


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


def connectWords(word1, word2, dictionary_set=None):
    """changes 1 letter at a time until word1 becomes word2"""
    if len(word1) != len(word2): return

    if dictionary_set is None:
        from done.String.Solver import masterDictionary
        dictionary_set = set(map(str.lower, masterDictionary))

    length = len(word1)
    word1 = word1.lower()
    word2 = word2.lower()

    unvisited = set(map(str.lower, filter((lambda i: len(i) == length), dictionary_set)))

    def getNeighbors(w2, remove=0):
        """finds words in the unvisited list as long as they're off by 1 letter"""
        for w in list(unvisited):
            if offByOne(w, w2):
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
