"""Just a bunch of Codes"""

from done.String import multiple_replace, createTranslationTable


def unbinary(text):
    """Change string of ones and zeroes into the actual string"""
    return ''.join(chr(int(i, 2)) for i in text.split())


def binary(text, to_binary=True):
    """Change string into binary bytes (actually still a string)
    
If to_binary is false, it will turn a binary string into a string again
(binary string is an actual string with the chars '1' and '0' in it)
"""
    if to_binary:
        return ' '.join('{:0>8}'.format(bin(ord(i)).lstrip('0b')) for i in text)
    else:
        return unbinary(text)


def eggnog(text):
    """Reverses string and adds spaces at the second last letter of words
    
Example:
    eggnog('daniel is cool') -> 'lo oc sileinad'
    eggnog('lo oc sileinad') -> 'daniel is cool'
    """
    s = text.split()
    return ''.join(reversed(s[0] + ''.join(f'{word[:2]} {word[2:]}' for word in s[1:]))).strip()


crosc_translation = createTranslationTable('yzxwuvtsorqpn')


def crosc(text):
    """Preforms a substitution code
    
Example:
    crosc('daniel') = 'wymoup'
    crosc('wymoup') = 'daniel'
"""
    return text.translate(crosc_translation)


craziness_translation = createTranslationTable('å∫ç∂´ƒ©˙ˆ∆˚¬µ˜øπœ®ß†¨√∑≈¥ΩÅıÇÎ´Ï˝ÓˆÔÒÂ˜Ø∏Œ‰Íˇ¨◊„˛Áı')
craziness_inverse = createTranslationTable('å∫ç∂´ƒ©˙ˆ∆˚¬µ˜øπœ®ß†¨√∑≈¥ΩÅıÇÎ´Ï˝ÓˆÔÒÂ˜Ø∏Œ‰Íˇ¨◊„˛Áı', inverse=True)


def craziness(text, inverse=True):
    """Preforms a substitution code - known as option code
    
Example:
    craziness('daniel',inverse=False) = '∂å˜ˆ´¬'
    craziness('∂å˜ˆ´¬') = 'daniel'
"""
    return text.translate(craziness_inverse if inverse else craziness_translation)


morse_dictionary = {'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..', 'e': '.', 'f': '..-.',
                    'g': '--.', 'h': '....', 'i': '..', 'j': '.---', 'k': '-.-', 'l': '.-..',
                    'm': '--', 'n': '-.', 'o': '---', 'p': '.--.', 'q': '--.-', 'r': '.-.',
                    's': '...', 't': '-', 'u': '..-', 'v': '...-', 'w': '.--', 'x': '-..-',
                    'y': '-.--', 'z': '--..', ' ': '/'}
morse_dictionary.update({(v, k) for k, v in morse_dictionary.items()})


def morse(text):
    """Morse Code. You know.
    
Example:
    morse('dan') = '-..  .-  -.'
    anti_morse('-..  .-  -.') = 'dan'
"""
    # preforms loop character by character
    return '  '.join(morse_dictionary.get(i, i) for i in text.lower())


def anti_morse(text):
    """Morse Code. You know.
    
Example:
    anti_morse('-..  .-  -.') = 'dan'
    morse('dan') = '-..  .-  -.'
"""
    text = text.replace('…', '...').replace('—', '--')
    # preforms loop word by word
    return ''.join(morse_dictionary.get(i, i) for i in text.split())


def _let_to_num(let):
    """let is a letter character [a-z][A-Z]"""
    return str(ord(let.lower()) - 96)


def _num_to_let(num):
    """errors appear as spaces"""
    return chr(96 + int(num or '-64'))


def num_letters(text, backToWords=False, letterSep=".", wordSep="...."):
    """letters to numbers. and back.
    
Example:
    _('daniel') --> '4.1.14.9.5.12'
    _('4.1.14.9.5.12', inverse=True) = 'daniel'
"""
    if backToWords:
        return ' '.join(''.join(_num_to_let(let) for let in word.split(letterSep)) for word in text.split(wordSep))
    return wordSep.join(letterSep.join(_let_to_num(let) for let in word) for word in text.split(' '))


numword = num_letters


def cypher(text, num):
    """Caesar cypher

    Example:
        _('daniel',1) = 'ebojfm'
    """

    def change(a):
        """return the cyphered text for 1 character"""
        if a.islower():
            c = 97
        elif a.isupper():
            c = 65
        else:
            return a
        return chr((ord(a) - c + num) % 26 + c)

    return ''.join(change(a) for a in text)


updown_translation = createTranslationTable('ɐqɔpǝɟƃɥᴉɾʞlɯuodbɹsʇnʌʍxʎz' * 2)
downup_translation = createTranslationTable('ɐqɔpǝɟƃɥᴉɾʞlɯuodbɹsʇnʌʍxʎz' * 2, inverse=True)


def downup(str_):
    """turns updown text back into text"""
    return str_.translate(downup_translation)[::-1]


def updown(str_):
    """Reverse the String as well as vertically rotate the characters"""
    return str_.translate(updown_translation)[::-1]


def lisp(string):
    """Make your string have a lisp by replacing letter combinations with th"""
    return multiple_replace(string, [('sh', 'th'), ('st', 'th'), ('s', 'th'), ('Sh', 'Th'), ('St', 'Th'), ('S', 'Th')])
