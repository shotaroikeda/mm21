#Modifiers list
#   netid    | GitHub
#   akmodi2  | modi95

from sets import Set

class Edge(object):

    def __init__(self, node1, node2):
        self.connects = Set([node1, node2])
