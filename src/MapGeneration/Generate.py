import uuid
import pprint
import random
from mapNode import *
from Continent import *

class Map(object):

    def __init__(self, randSeed=10, nContinents=10, nClusters=30, sizeCluster=10):
        return