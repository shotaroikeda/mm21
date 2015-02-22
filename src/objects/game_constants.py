#NodeType enum (NodeType.Small = 1)
class NodeType:
    Small, Medium, Large, ISP, Datacenter = range(5)
# processing/networking power indexed by nodeType
processing = []
networking = []