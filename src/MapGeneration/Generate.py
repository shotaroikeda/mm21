import uuid
import pprint
import random
from mapNode import *
from Continent import *

class Map(object):

    def __init__(self, isp_dc_ratio=1.5, continent_count=10, cluster_count=30, cluster_density=10, rseed=10):
        return