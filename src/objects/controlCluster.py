import game_constants.py

class MapCluster( object ):
    def __init__(id, ownerId, nodeList):
        #int
        self.id = id
        self.processingPower = 0
        self.networkingPower = 0
  	self.ownerId = ownerId
        self.nodeList = []
    def add(self, node):
        #node is a MapNode
        return
    def remove(self, node):
        #node is a MapNode
    def union(self, other):
        #other is a MapCluster
        return
