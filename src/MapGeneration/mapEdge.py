from sets import Set
class mapEdge(object):

    edgelist = []

    def __init__(self, node1, node2):
        self.connects = [node1, node2]
        mapEdge.edgelist.append(self)

    def __str__(self):
        str = "Edge:\n" + repr(self.connects[1]) + "\nConnects to \n" + repr(self.connects[2])