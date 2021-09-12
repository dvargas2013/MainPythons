from done import File

def test_File_homeDirectory():
    assert File.exists(File.getHome())

# TODO how to test done.File
