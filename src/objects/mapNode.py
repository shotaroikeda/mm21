import game_constants

class MapNode( object ):
    def __init__(self, id, adjacent, nodetype):
        #int
        self.id = id
        self.processingPower = game_constants.processing[nodeType]
        self.networkingPower = game_constants.networking[nodeType]
        self.ownerId = None
        self.softwareLevel = 0
        #int[]
        self.adjacentIds = adjacent
        self.rootkitIds = []
        #bool
        self.isDDOSed = False
        self.isIPSed = False
        #dict<int, int>
        self.infiltration = dict()
    def connect(self, other):
        #other is a mapNode
        if other.id in self.adjacentIds:
            raise Exception("Nodes are already connected.")
        self.adjacentIds.push(other.id)
        other.adjacentIds.push(self.id)
        return
    def doControl(self, playerId):
        if playerId == self.ownerId:
            for k in infiltration.iterkeys():
                infiltration[k] = max(infiltration[k] - 1, 0)
        else:
            infiltration[playerId] = infiltration.get(playerId, 0) + 1
            if infiltration[playerId] > 50: # TODO change this number
                self.own(playerId)
        return
    def doIPS(self):
        self.isIPSed = True
        return
    def doDDOS(self):
        self.isDDOSed = True
        return
    def upgrade(self):
        self.softwareLevel += 1
        return
    def clean(self):
        self.rootkitIds = []
        return
    def scan(self):
        return self.rootkitIds
    def rootkit(self, playerId):
        if playerId in self.rootkitIds:
            raise Exception("This player has a rootkit here already!")
        self.rootkitIds.push(playerId)
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
