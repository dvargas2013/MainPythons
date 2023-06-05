import os.path

from done import File
from done.File import pretty


def test_homeDirectory():
    assert os.path.exists(File.getHome())


def test_same():
    for file1, file2 in zip(
            File.files(os.path.abspath('.'), relative=False),
            File.files('.')):
        assert File.same(file1, file2)


def test_cwdas():
    here = os.getcwd()
    with File.cwd_as(".."):
        assert here != os.getcwd()
    assert here == os.getcwd()


def singleTGF_test(a, b):
    assert a.nodes == b.nodes
    assert sorted(a.ordered_nodes) == sorted(b.ordered_nodes)
    assert sorted(a.ordered_node_mapping) == sorted(b.ordered_node_mapping)
    assert a.to_dict() == b.to_dict()


def test_TGF():
    a = pretty.TGF({"a": ["b", "c"]})
    b = pretty.TGF({"a": {"b", "c"}})
    singleTGF_test(a, b)

    from string import ascii_lowercase
    from random import sample

    nodes = list(ascii_lowercase)
    for connections in range(1, 10):
        network = {n: sample(ascii_lowercase, k=connections) for n in nodes}
        network_with_set = {n: set(j) for n, j in network.items()}

        singleTGF_test(pretty.TGF(network), pretty.TGF(network_with_set))
