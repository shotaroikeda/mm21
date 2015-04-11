from mapNode import *

'''
Building a continent:

_Params
    Number of ISPs
    DataCenter density
    City density (per ISP)

_Building
    Start by building ISP Clusters with the required amount of city density.
    Create DataCenters using the datacenter_density param.
    Make an assignemnt call to assign ISP Clusters with DataCenters

Join ISP Clusters
    Join call on ISP Clusters
    HACK: May need interconnection density parameters

'''

class Continent(object):

    def __init__(self, isp_dc_ratio=1.5, cluster_count=30, cluster_density=10, rseed=10):