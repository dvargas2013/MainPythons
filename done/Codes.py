'''Just a bunch of Codes'''

def binary(s,toBin=True):
    """Change string into binary bytes (actually still a string)
    
    If you change toBin to false it will turn a binary string (actually a string with the chars '1' and '0' in it) into a string again
    """
    if toBin: return ' '.join( '{:0>8}'.format(bin(ord(i)).lstrip('0b')) for i in s )
    else: return ''.join(chr(int(i,2)) for i in s.split())
def eggnog(str_):
    """Reverses string and adds spaces at the second last letter of words
    
    Example:
        eggnog('daniel is cool') -> 'lo oc sileinad'
        eggnog('lo oc sileinad') -> 'daniel is cool'
    """
    s = str_.split()
    return ''.join(reversed(s[0]+''.join('%s %s'%(word[:2],word[2:]) for word in s[1:]))).strip()
def crosc(string):
    """Preforms a substitution code
    
    Exmaple:
        crosc('daniel') = 'wymoup'
        crosc('wymoup') = 'daniel'
    """
    dicti={'a':'y','b':'z','c':'x','d':'w','e':'u','f':'v','g':'t','h':'s',
           'i':'o','j':'r','k':'q','l':'p','m':'n','n':'m','o':'i','p':'l',
           'q':'k','r':'j','s':'h','t':'g','u':'e','v':'f','w':'d','x':'c',
           'y':'a','z':'b','A':'Y','B':'Z','C':'X','D':'W','E':'U','F':'V',
           'G':'T','H':'S','I':'O','J':'R','K':'Q','L':'P','M':'N','N':'M',
           'O':'I','P':'L','Q':'K','R':'J','S':'H','T':'G','U':'E','V':'F',
           'W':'D','X':'C','Y':'A','Z':'B',' ':' '}
    return ''.join(dicti.get(i,i) for i in string)
def crazyness(string, inverse=True):
    """Preforms a substition code - known as option code
    
    Example:
        crazyness('daniel',inverse=False) = '∂å˜ˆ´¬'
        crazyness('∂å˜ˆ´¬') = 'daniel'
    """
    dicti={'a':'å','b':'∫','c':'ç','d':'∂','e':'´','f':'ƒ','g':'©','h':'˙',
           'i':'ˆ','j':'∆','k':'˚','l':'¬','m':'µ','n':'˜','o':'ø','p':'π',
           'q':'œ','r':'®','s':'ß','t':'†','u':'¨','v':'√','w':'∑','x':'≈',
           'y':'¥','z':'Ω','A':'Å','B':'ı','C':'Ç','D':'Î','E':'´','F':'Ï',
           'G':'˝','H':'Ó','I':'ˆ','J':'Ô','K':'','L':'Ò','M':'Â','N':'˜',
           'O':'Ø','P':'∏','Q':'Œ','R':'‰','S':'Í','T':'ˇ','U':'¨','V':'◊',
           'W':'„','X':'˛','Y':'Á','Z':'ı',' ':' '}
    back = {j:i for i,j in dicti.items()}
    if inverse: return ''.join(back.get(i,i) for i in string)
    return ''.join(dicti.get(i,i) for i in string)
def piglatin(str_,inverse=False):
    """You know piglatin. Don't make me explain it.
    
    Exmaple:
        piglatin('You are an apple') = 'ouYay reaay naay ppleaay'
        piglatin('ouYay reaay naay ppleaay', inverse=True) = 'You are an apple'
    """
    if inverse: return ' '.join(i[-3]+i[:-3] for i in str_.split())
    return ' '.join("%s%say"%(i[1:],i[0]) for i in str_.split())
def morse(string):
    """Morse Code. You know.
    
    Exmaple: 
        morse('dan') = '-..  .-  -.'
        antimorse('-..  .-  -.') = 'dan'
    """
    dicti={'a':'.-','b':'-...','c':'-.-.','d':'-..','e':'.','f':'..-.',
           'g':'--.','h':'....','i':'..','j':'.---','k':'-.-','l':'.-..',
           'm':'--','n':'-.','o':'---','p':'.--.','q':'--.-','r':'.-.',
           's':'...','t':'-','u':'..-','v':'...-','w':'.--','x':'-..-',
           'y':'-.--','z':'--..',' ':'/'}
    return '  '.join(dicti.get(i,i) for i in string.lower())
def antimorse(string):
    """Morse Code. You know.
    
    Exmaple: 
        antimorse('-..  .-  -.') = 'dan'
        morse('dan') = '-..  .-  -.'
    """
    string=string.replace('…','...').replace('—','--')
    dicti,new={'-..':'d', '-.-.':'c', '...':'s', '..-':'u', '-.--':'y',
       '-...':'b', '-..-':'x', '...-':'v', '-.':'n', '--.-':'q',
       '--..':'z', '-':'t', '/': ' ', '.': 'e', '--': 'm', '.-..': 'l',
       '.-.': 'r', '.---': 'j', '.--.': 'p', '.--': 'w', '....': 'h',
       '.-': 'a', '..': 'i', '..-.': 'f', '---': 'o', '--.': 'g', '-.-': 'k'},''
    for i in string.split():
        try: new+=dicti.get(i,i)
        except: new+='%'
    return new
def numword(string,inverse=False):
    """letters to numbers. and back.
    
    Example:
        numword('daniel') --> '4.1.14.9.5.12'
        numword('4.1.14.9.5.12', inverse=True) = 'daniel'
    """
    if inverse: return ' '.join(''.join(chr(96+int(a or '-64')) for a in i.split('.')) for i in string.split('....'))
    return '....'.join('.'.join(str(ord(a)-96) for a in i) for i in string.split(' '))
def bobulate(string):
    """Adds 'a' and 'b' and the previous letter for each character in string
    
    Example:
        bobulate('daniel') = 'dabadanabinaebileb'
    """
    def iso(string):
        if string in 'aeiouy': return 'b'
        return 'a'
    ret=''
    for stry in string.lower().split(' '):
        ret+=stry[0]+iso(stry[0])+iso(iso(stry[0]))
        for i in range(1,len(stry)):
            ret+=stry[i]
            if iso(stry[i])==iso(stry[i-1]): ret+=iso(stry[i-1])+stry[i-1]
            else: ret+=stry[i-1]+iso(stry[i-1])
        ret+=' '
    return ret[:-1]
def unbobulate(string):
    """Inverse of bobulate. Just takes every 3rd letter.
    
    Example:
        unbobulate('dabadanab') = ('dan', True)
    """
    out=' '.join(stry[::3] for stry in string.split())
    return out,bobulate(out)==string
def cypher(string,num):
    """Ceaser cypher
    
    Example:
        _('daniel',1) = 'ebojfm'
    """
    def change(a):
        if a.islower(): c=97
        elif a.isupper(): c=65
        else: return a
        return chr((ord(a)-c+num)%26+c)
    return ''.join(change(a) for a in string)