import uuid


class Node(object):
        def __init__(self, nodeType):
                self.uid = uuid.uuid4()
                self.nodeType = nodeType
                self.connectedNodes = []

        def join_node(self, node):
                self.connectedNodes.append(node.nodeUid)
                node.connectedNodes.append(self.nodeUid)


def generate_graph(numPlayers, cityDensity, ispDensity, connectionDensity):
        clusterList = [list() for _ in range(numPlayers)]
        for cluster in clusterList:
                for _ in range(ispDensity):
                        isp = Node("isp")
                        cluster.append(isp)
                        ispList = []
                        for city in range(cityDensity):
                                cityList = []
                                city = Node('city')
                                isp.join_node(city)
                                for c in cityList():
                                        city.join_node(c)
                                cityList.append(city)
        # ToDo: links betwean cities, datacenter
        return clusterList



if __name__ == "__main__":
