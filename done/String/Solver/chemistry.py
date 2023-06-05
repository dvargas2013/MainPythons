# without j and q the algorithm would get stuck
from random import choice

from done.String import score

Gems = ['j*', 'q*', 'H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl',
        'Ar', 'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br',
        'Kr', 'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I',
        'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu',
        'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac',
        'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh',
        'Hs', 'Mt', 'Ds', 'Rg', 'Cn', 'Uut', 'Fl', 'Uup', 'Lv', 'Uus', 'Uuo']
UseGems = dict()  # grab the gems that are possible to use
for i in range(ord('a'), ord('z') + 1):
    i = chr(i)
    lis = UseGems.get(i, list())
    if not lis: UseGems[i] = [g for g in Gems if i in g[:1].lower()]


def splitTarget(target, w2):
    target, w2 = target.lower(), w2.lower()
    grow = ''
    for c in w2:
        if target[:1] == c:
            grow += target[:1]
            target = target[1:]
    return grow, target


def perfLvl(gem, aim):
    if len(gem) == 1: return 2
    return next((2 * x - 1 for x in range(len(gem), 0, -1) if gem[:x].lower() == aim[:x].lower()), 0)


def expandWord(w2, target):
    first, last = splitTarget(target, w2)
    t_letter = last[:1]
    if not t_letter: return
    save = {w2 + _i: perfLvl(_i, last) for _i in UseGems[t_letter]}
    _max = 1 if 2 in save.values() else 0
    return [_i for _i in save if save[_i] > _max]


def yieldMaximums(words, target, _max=.5):
    returnable = {}
    for w in list(words):  # For every word in that list
        words = expandWord(w, target)  # Add symbols if you can
        if words:  # If words have been added go deeper
            words, _max = yieldMaximums(words, target, _max)
            returnable.update({w2: words[w2] for w2 in words if words[w2] >= _max})
        else:
            s = score(target, w)
            if s >= _max:
                _max = s
                returnable[w] = s
    for w in list(returnable.keys()):
        if returnable[w] != _max: returnable.pop(w)
    return returnable, _max


def chemistry(text="Hello World", show_all=False):
    """Given a sentence will try to recreate string with chemistry symbols"""
    string = ''
    for word in text.lower().split():
        word = ''.join(c for c in word if c.isalpha())
        save = yieldMaximums([''], word)
        chem, num = list(save[0]), save[-1]
        if show_all: print(num, chem)
        chem = choice(chem)
        string += chem + ' '
    return string
