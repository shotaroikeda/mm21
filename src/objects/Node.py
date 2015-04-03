#Modifiers list
#   netid    | GitHub
#   akmodi2  | modi95

import game_constants

class Node(object):

    def __init__(self, id=0, nodeType='Map', lvl=0,):
        self.id = id
        self.network_power = game_constants.NodeType.networking[lvl][nodeType]
        self.processor_power = game_constants.NodeType.processing[lvl][nodeType]
        self.lvl = lvl
        self.rootKits = []
        self.edges = []

