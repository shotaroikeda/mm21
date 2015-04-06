

class mapNode(object):

    def __init__(self, nodeType):
        self.nodeType = nodeType  #
        self.connected_nodes = [] #list of edges
        self.isplcID = None
        self.continent = None
        self.uid = id(self)

    def add_edge(self, edge):
        self.connected_nodes.append(edge)

    def __str__(self):
        st = str(self.uid) + "\n"
        st += self.nodeType + " | " + str(self.isplcID) + " | " + repr(self.continent) + "\n"
        st += str(self.connected_nodes)
        return st

    def __repr__(self):
        st = str(self.uid) + " | "
        st += self.nodeType + " | " + str(self.isplcID) + " | " + repr(self.continent) + " | "
        return st