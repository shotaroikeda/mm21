import uuid
import pprint
import random

p = pprint.PrettyPrinter()


class CityCluster(object):
        def __init__(self, city_density, connection_density):
                self.nodes = []
                for i in range(city_density):
                        city = Node('city')
                        # Rule 1: connect city to all cities in cluster.
                        for c in self.nodes:
                                city.join_node(c)
                        self.nodes.append(city)



class ISPCluster(object):
        def __init__(self, city_density, isp_density, data_center_density, connection_density):
                self.node_list = []
                self.isp_list = []
                self.data_center_list = []
                self.city_list = []
                self.city_cluster_list = []

                for _ in range(isp_density):
                        isp = Node("isp")
                        self.isp_list.append(isp)
                        city_cluster = CityCluster(
                                city_density,
                                connection_density)
                        # Rule 2: IPS connects to all citys in it's city cluster
                        for city in city_cluster.nodes:
                                city.connect(isp)

                        self.node_list.extend(city_cluster.nodes)
                        self.city_list.extend(city_cluster.nodes)
                        self.city_cluster_list.append(city_cluster)

                for _ in range(data_center_density):
                        data_center = Node("data_center")
                        self.data_center_list.append(data_center)
                        # Rule 3: Data center connects to up to two ISPs
                        random.choice(self.isp_list).connect(data_center)
                        random.choice(self.isp_list).connect(data_center)

                # Rule 4: Each city cluster has atlest 2 link form it's citis to other cities
                for cityCluster in self.city_cluster_list:
                        random.choice(cityCluster.nodes).connect(
                                self.rand_city_cluster_not_in(cityCluster))
                        random.choice(cityCluster.nodes).connect(
                                self.rand_city_cluster_not_in(cityCluster))
                self.node_list.extend(self.isp_list)
                self.node_list.extend(self.data_center_list)

        def rand_city_cluster_not_in(self, exclude_city_cluster=None):
                city_cluster = exclude_city_cluster
                assert len(self.city_cluster_list) > 1
                while (city_cluster is exclude_city_cluster):
                        city_cluster = random.choice(self.city_cluster_list)
                return random.choice(city_cluster.nodes)

        def __str__(self):
                return p.pformat(self.node_list)

        def __repr__(self):
                return str(self)



class Node(object):
        def __init__(self, nodeType= "undefind"):
                self.uid = uuid.uuid4()
                self.nodeType = nodeType
                self.connected_nodes = []

        def join_node(self, node):
                if not self.is_connected(node):
                        self.connected_nodes.append(node.uid)
                        node.connected_nodes.append(self.uid)

        def connect(self, node):
                self.join_node(node)

        def is_connected(self, node):
                if self in node.connected_nodes:
                        return node in self.connected_nodes

        def __repr__(self):
                return p.pformat("{}.{}".format(self.nodeType, self.uid))


def generate_graph(num_players, city_density, isp_density, connection_density):
        isp_cluster_list = [ISPCluster(
                city_density,
                isp_density,
                2,
                connection_density
        )for _ in range(num_players)]
        for isp_c in isp_cluster_list:
                for i in range(0, connection_density):
                        inst_a = random.choice(isp_c.isp_list)
                        inst_b = rand_isp_cluster_not_in(isp_cluster_list,
                                                         isp_c)
                        inst_a.connect(inst_b)


        # ToDo: links betwean cities, datacenter
        return isp_cluster_list

def rand_isp_cluster_not_in(ispCluster, exclude_isp_cluster=None):
        isp_cluster = exclude_isp_cluster
        while (isp_cluster is exclude_isp_cluster):
                isp_cluster = random.choice(ispCluster)
        return random.choice(isp_cluster.isp_list)


if __name__ == "__main__":
        p = pprint.PrettyPrinter()
        graph = generate_graph(2, 2, 2, 3)
        p.pprint(graph)
