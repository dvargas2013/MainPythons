def print_iterable(iterable):
    """prints a line for every item in iterable"""
    for line in iterable:
        print(line)


printAll = print_iterable


def wrapPrint(str_, num=79):
    """Wraps the text to stay to a max line width of {num}"""
    lis = [i for i in str_.replace('\n', ' \n ').split(' ') if len(i) != 0]
    line = ''
    for i in range(len(lis)):
        word = lis[i]
        if word == '\n':
            print('\n' + line, end="")
            line = ''
        elif len(line) == 0:
            line = word
        elif len(line) + len(word) < num:
            line += ' ' + word
        else:
            print('\n' + line, end="")
            line = ' ' + word
    print()


smartPrint = wrapPrint


def removePrint(str_, size=79, around=None):
    """Prints out the ends of the string with '...' if anything was removed

If {around} is defined, will try to find the substring.
If substring is found, it will show the center around the substring
and will delete before and after the window instead
"""
    if len(str_) > 2 * size:
        if around:
            i = str_.find(around)
            if i != -1:
                s = str_[:size]
                if 2 * size < i: s += ' ... '
                s += str_[i - size:i + size]
                if len(s) - i < 2 * size: s += ' ... '
                print(s + str_[-size:])
                return
        print(str_[:size] + ' ... ' + str_[-size:])
    else:
        print(str_)


safePrint = removePrint


class Node:
    """Node that can create a tree that displays children in the following way when str() is called:

NodeParent
+---Child1
+   +---SubChild1.1
+   +---SubChild1.2
+---Child2
+   +---SubChild2.1
"""

    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.children = []
        if type(parent) == Node:
            parent.children.append(self)

    def __build_string(self, ln=0):
        """recursive call to display the tree"""
        if ln > 0:
            pre = '+   ' * (ln - 1) + '+---' + self.name
        else:
            pre = self.name

        if len(self.children):
            return pre + ''.join("\n" + i.__build_string(ln + 1) for i in self.children)

        return pre

    def __str__(self):
        return self.__build_string()


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
        a, b = 0, 1
        com = 0
        while com != -1:
            com = st.find(",", b)
            quote = st.find('"', b)
            if quote != -1 and quote < com:
                b = st.find('"', quote + 1) + 1
                continue
            b = com + 1
            if com < 0: b = len(st) + 1
            yield st[a:b - 1]
            a = b

    bigDic = {'': Node('*top', None)}
    raw = raw.strip('{').strip('}')
    for line in splitYield(raw):
        line = line.split(' of ')
        prevS = ''
        while len(line) > 0:
            name = line.pop(-1).strip(' ')
            search = name + ' of ' + prevS
            bigDic[search] = bigDic.get(search, False)
            if not bigDic[search]: bigDic[search] = Node(name, bigDic[prevS])
            prevS = search
    if len(bigDic[''].children) == 1: return bigDic[''].children[0]
    return bigDic['']


def pretty(width=80, height=20):
    """Prints a rectangle of stars in the Terminal"""
    from time import sleep
    from done.String.Generators import MarkovStars
    width = 3 * width // 8
    endspace = " " * (width // 8)
    while 1:
        for _ in range(height): print(' '.join(MarkovStars.generate(width // 2)) + endspace)
        print("\033[F" * height, end="\r")
        sleep(.32)
