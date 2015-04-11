from mapNode import *



class ISPCluster(object):
    cluster_dict = {}
    #creats an ISP Cluster of size sizeCluster
    def __init__(self, isp, dc_list, isp_dc_ratio=1.5, cluster_density=10, rseed=10):
        key_isp = isp
        return