"""Deals with anything string and cute string manipulations"""

import random
from string import ascii_lowercase, ascii_letters

from done.List import window


def multiple_replace(string, replace_array):
    """preforms string.replace() multiple times with the replace_array"""
    for src, dst in replace_array:
        string = string.replace(src, dst)
    return string


def createTranslationTable(string_mapping, inverse=False):
    """Given what every lowercase letter maps to. will make a str.translate() matrix

if len == 52, I'll map string.ascii_letters to those
if len == 26, I'll map string.ascii_lowercase to those and map ascii_uppercase to those.upper()
if len == 13 (i.e. [n-z] shuffled), I'll map [a-m] to those and figure out how to map the other letters

if inverse is set, will do everything the same but will preform the final table making as the inverse of the original
note: if you create with [n-z] shuffled, it will already be its own inverse

usage:
    albhed = createTranslationTable('ypltavkrezgmshubxncdiwfqoj', inverse=True)
    "rammu".translate(albhed) == "hello"
"""
    if len(string_mapping) == 13:
        first13 = ascii_lowercase[:13]
        last13 = ascii_lowercase[-13:]
        string_mapping += last13.translate(str.maketrans(string_mapping, first13))
    if len(string_mapping) == 26:
        string_mapping += string_mapping.upper()
    if len(string_mapping) == 52:
        sm = string_mapping[::-1]
        al = ascii_letters[::-1]
        if inverse:
            return str.maketrans(sm, al)
        else:
            return str.maketrans(al, sm)


def yield_all_characters(code_point=0):
    """starting at \x00 go up while under chr(0x110000)"""
    for code_point in range(code_point, 0x110000):
        yield chr(code_point)
        code_point += 1


def switch(text, string1, string2, starting_code_point=32):
    """Swap every occurrence of {string1} and {string2} in {mainstring} with each other
    
Usage:
    switch('10101011','1','0') = '01010100'
    """
    all_the_symbols = set(text)
    for swap_val in yield_all_characters(starting_code_point):
        if swap_val not in all_the_symbols:
            return text.replace(string1, swap_val).replace(string2, string1).replace(swap_val, string2)


def reverse(str_):
    """Reverse the String"""
    return str_[::-1]  # ''.join(reversed(str_))


def score(str1, str2):
    """Compare the two strings and give it a score between 0 and 1"""
    if str1 == str2 == "": return 0
    str1 = str1.lower()
    str2 = str2.lower()
    str1_len = len(str1)
    str2_len = len(str2)
    str1_flags = [0] * str1_len
    str2_flags = [0] * str2_len

    w_size = max(str1_len, str2_len) // 2 - 1
    if w_size < 0: w_size = 0

    common = 0
    for i, str1_char in enumerate(str1):  # for every char in str1
        for j in range(max(i - w_size, 0), min(i + w_size + 1, str2_len)):  # check a range in str2
            if not str2_flags[j] and str2[j] == str1_char:  # for matches to str1
                str1_flags[i] = str2_flags[j] = True
                common += 1
                break
    if common == 0: return 0

    k = trans = 0  # measures the amount of 'crossings' of flagged chars
    for i, aFlag in enumerate(str1_flags):
        if aFlag:  # for all flagged chars in str1
            for j in range(k, str2_len):
                if str2_flags[j]:  # for all flagged chars in str2 (that we haven't re-checked yet)
                    k = j + 1
                    if str1[i] != str2[j]: trans += 1
                    break
    trans /= 2  # crossings are counted twice so divide by 2
    common = float(common)
    return (common / str1_len + common / str2_len + (common - trans) / common) / 3


class Markov:
    """Create a Markov Chain of words linked in triplets"""

    def __init__(self, words):
        self.cache = dict()
        for w1, w2, w3 in window(words.strip().split(), 3):
            key = (w1, w2)
            if key in self.cache:
                self.cache[key].append(w3)
            else:
                self.cache[key] = [w3]

    def generate(self, size=25):
        """generate a random sentence with size words using the markov chain"""
        seed_word, next_word = random.choice(list(self.cache.keys()))
        w1, w2 = seed_word, next_word
        gen_words = []
        for i in range(size):
            gen_words.append(w1)
            try:
                w1, w2 = w2, random.choice(self.cache[(w1, w2)])
            except KeyError:
                gen_words.append(w2)
                return ' '.join(gen_words) + " " + self.generate(size - i - 2)
        gen_words.append(w2)
        return ' '.join(gen_words)


def SequenceAlignment(s1, s2, DownSigma=0, RightSigma=0, Match=1, MisMatch=0):
    """Preforms Global Sequence Alignment on the two strings"""
    n, m = len(s1), len(s2)
    S = [[tuple()] * (m + 1) for _ in range(n + 1)]
    S[0][0] = (0, 0)
    for j in range(1, m + 1): S[0][j] = (S[0][j - 1][0] + RightSigma, 2)  # Right Sigma
    for i in range(1, n + 1): S[i][0] = (S[i - 1][0][0] + DownSigma, 1)  # Down  Sigma
    for j in range(1, m + 1):
        for i in range(1, n + 1):
            S[i][j] = max(
                (S[i - 1][j - 1][0] + (Match if s1[i - 1] == s2[j - 1] else MisMatch), 3),  # Diagonal
                (S[i - 1][j][0] + DownSigma, 1),  # Down  Sigma
                (S[i][j - 1][0] + RightSigma, 2),  # Right Sigma
            )
    i, j = n, m
    ss1, ss2 = "", ""
    _, direction = S[i][j]
    while direction:
        if direction == 1:  # Down
            ss1 = s1[i - 1] + ss1
            ss2 = "-" + ss2
            i -= 1
        elif direction == 2:  # Rite
            ss1 = "-" + ss1
            ss2 = s2[j - 1] + ss2
            j -= 1
        elif direction == 3:  # Diag
            ss1 = s1[i - 1] + ss1
            ss2 = s2[j - 1] + ss2
            i -= 1
            j -= 1
        _, direction = S[i][j]
    return ss1, ss2
