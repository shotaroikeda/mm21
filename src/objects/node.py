"""
Holds data about a specific node on the map
"""

import game_constants
class Node(object):
    def __init__(self, id, adjacent, nodetype):
        # int
        self.id = id
        self.processingPower = game_constants.processing[nodeType]
        self.networkingPower = game_constants.networking[nodeType]
        self.ownerId = None
        self.softwareLevel = 0
        # int[]
        self.adjacentIds = adjacent
        self.rootkitIds = []
        # bool
        self.isDDOSed = False
        self.isIPSed = False
        # dict<int, int>
        self.infiltration = dict()

    def connect(self, other):
        # other is a mapNode
        if other.id in self.adjacentIds:
            raise Exception("Nodes are already connected.")
        self.adjacentIds.append(other.id)
        other.adjacentIds.append(self.id)
        return

    def canMoveThrough(self, playerId):
        if playerId in self.rootkitIds:
            return True
        return self.ownerId == playerId

    def own(self, playerId):
        if playerId == self.ownerId:
            raise Exception("This player owns this node already.")
        self.ownerId = playerId
        self.rootkitIds = []
        self.infiltration = []
        return
