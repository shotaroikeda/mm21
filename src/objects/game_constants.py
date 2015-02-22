#NodeType enum (NodeType.Small = 1)
class NodeType:
    Small, Medium, Large, ISP, Datacenter = range(5)
# processing/networking power indexed by nodeType
processing = [100, 200, 500, 2000, 0]
networking = [100, 200, 500, 0, 2000]
