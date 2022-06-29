import os

from done import File

def test_homeDirectory():
    assert File.exists(File.getHome())

def test_same():
    for file1, file2 in zip(
            File.files(File.abspath('.'), relative=False),
            File.files('.')):
        assert File.same(file1, file2)

def test_cwdas():
    here = os.getcwd()
    with File.cwd_as(".."):
        assert here != os.getcwd()
    assert here == os.getcwd()

def test_TGF():
    # TODO find simple way to make random networks to test TGF constraints
    a = File.TGF({"a": ["b", "c"]})
    b = File.TGF({"a": {"b", "c"}})
    assert a.nodes == b.nodes
    assert a.ordered_nodes == b.ordered_nodes
    assert list(a.ordered_nodemapping) == list(b.ordered_nodemapping)

    assert str(a) == str(b)
    assert a.to_dict() == b.to_dict()
