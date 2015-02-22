import game_constants

class MapNode( object ):
    def __init__(self, id, adjacent, nodetype):
        #int
        self.id = id
        self.processingPower = game_constants.processing[nodeType]
        self.networkingPower = game_constants.networking[nodeType]
        self.ownerid = None
        self.softwareLevel = 0
        #int[]
        self.adjacentIds = adjacent[:]
        self.rootkits = []
        #bool
        self.isDdosed = False
        self.isIPSed = False
        #dict<int, int>
        self.infiltration = dict()
    def connect(self, other):
        #other is a mapNode
        return
    def doIPS(self):
        return
    def doDDOS(self):
        return
    def upgrade(self):
        return
    def clean(self):
        return
    def scan(self):
        return
    def rootkit(self, player):
        return
    def portScan(self):
        return

