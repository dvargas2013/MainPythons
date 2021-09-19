from done import String


def test_translationtable():
    to_albhed = String.createTranslationTable('ypltavkrezgmshubxncdiwfqoj')
    from_albhed = String.createTranslationTable('ypltavkrezgmshubxncdiwfqoj', inverse=True)
    assert "hello".translate(to_albhed) == "rammu"
    assert "rammu".translate(from_albhed) == "hello"


def test_switch():
    assert String.switch('10101011', '1', '0') == '01010100'
