from done import String
from done.String import Solver as StringSolver


def test_translationtable():
    to_albhed = String.createTranslationTable('ypltavkrezgmshubxncdiwfqoj')
    from_albhed = String.createTranslationTable('ypltavkrezgmshubxncdiwfqoj', inverse=True)
    assert "hello".translate(to_albhed) == "rammu"
    assert "rammu".translate(from_albhed) == "hello"


def test_switch():
    assert String.switch('10101011', '1', '0') == '01010100'


def test_DeBruijn(alphabet='acbef', length=5):
    from done.String.Generators import DeBruijn
    from done.List import window
    seq = DeBruijn(alphabet, length)
    seq += seq[:length]
    store = set(map("".join, window(seq, length)))
    assert len(store) == len(set(alphabet)) ** length  # Check that all possible arrangements of length were added


def test_clues22():
    assert set(StringSolver.clues22(
        ['he', 'll', 'be', 'o'],
        dictionary_set={"hello", "bell", "helbe", "one"})) == {"hello", "bell"}


def test_anagram():
    assert set(StringSolver.anagram("elhol", {"hello", "hole", "ball"})) == {"hole", "hello"}


def test_oneLetterFromEach():
    s = set(StringSolver.oneLetterFromEach("t", "hx", "ea",
                                           dictionary_set={"the", "hex", "het", "hit", "hat", "tan", "tax"}))
    assert len(s.intersection({"the", "het", "hat", "tax"})) == 4


def test_connectwords(monkeypatch):
    L = list(StringSolver.connectWords("hello", "bells", dictionary_set={'hello', 'helly', 'belly', 'bells'}))
    assert len(L) == 1
    assert len(L[0]) == 4
