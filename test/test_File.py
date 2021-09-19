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
