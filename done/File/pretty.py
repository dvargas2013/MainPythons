from typing import Mapping, Iterable

from done.File import write


class TGF:
    def __init__(self, dic: Mapping[str, Iterable[str]]):
        # sorted set of all names used (whether in keys or values)
        self.nodes = sorted(set.union(*map(set, dic.values()), set(dic.keys())))

        # index in the sorted list
        self.node_to_tgf_index = {n: i for i, n in enumerate(self.nodes)}

        # tuples of the mapping in the dictionary using the indexes rather than the names
        self.ordered_nodes = []

        for i, js in dic.items():
            x = self.node_to_tgf_index[i]
            self.ordered_nodes.extend((x, self.node_to_tgf_index[j])
                                      for j in js)

    def __str__(self):
        # the string format has 1-based indexing
        return "\n".join((
            *(f"{i} {n}" for i, n in enumerate(self.nodes, start=1)),
            "#",
            *(f"{i + 1} {j + 1}" for i, j in self.ordered_nodes)))

    @property
    def ordered_node_mapping(self):
        return iter((self.nodes[i], self.nodes[j]) for i, j in self.ordered_nodes)

    def to_dict(self):
        from done.List import CollisionDictOfSets
        return dict(CollisionDictOfSets(self.ordered_node_mapping))


def write_dict_to_tgf(dic: Mapping[str, Iterable[str]], file):
    return write(str(TGF(dic)), file)


def stringify(s):
    if type(s) == dict:
        s = "{\n\t%s\n}" % ',\n\t'.join("%s:\t%s" % (repr(i), repr(j)) for i, j in s.items())
    elif type(s) == list:
        s = "[\n\t%s\n]" % ',\n\t'.join(repr(i) for i in s)
    elif type(s) == tuple:
        s = "(\n\t%s\n)" % ',\n\t'.join(repr(i) for i in s)
    elif type(s) == set:
        s = "{\n\t%s\n}" % ',\n\t'.join(repr(i) for i in s)

    return s
