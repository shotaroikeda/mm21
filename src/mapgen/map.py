from continent import Continent
from graph import Graph
# import networkx as nx
# import matplotlib.pyplot as plt


class Map():

    def __init__(self, num_continents, isp_per_continents, cities_per_isp):
        self.continent_list = []
        self.graph = Graph()
        for i in range(num_continents):
            self.continent_list.append(Continent(self.graph, isp_per_continents, cities_per_isp))
            if i != 0:
                self.continent_list[i].connect_continent(self.graph, self.continent_list[i - 1], 2, 2, 2, 2)

    def convert_to_json(self):
        json = {}
        json['nodes'] = []
        json['edges'] = []
        json['continents'] = []
        for vertex in self.graph.vertex_list:
            vertex_json = {'id': vertex.uid, 'type': vertex.node_type, 'adjacent-nodes': []}
            for edge in vertex.connected_nodes:
                if list(edge)[0] == vertex.uid:
                    vertex_json['adjacent-nodes'].append(list(edge)[1])
                else:
                    vertex_json['adjacent-nodes'].append(list(edge)[0])
            json['nodes'].append(vertex_json)
        for edge in self.graph.edge_list:
            json['edges'].append(edge)
        for continent in self.continent_list:
            json_continent = {'isps': [], 'datacenters': []}
            for isp in range(len(continent.isp_list)):
                json_continent['isps'].append({'id': continent.isp_list[isp].uid, 'cities': continent.isps_city_list[isp]})
            for dc in continent.datacenter_list:
                json_continent['datacenters'].append({'id': dc.uid})
            json['continents'].append(json_continent)

        return json

    def draw_graph(self):
        G = nx.Graph()
        for vertex in self.graph.vertex_list:
            G.add_node(vertex.uid)
        for edge in self.graph.edge_list:
            G.add_edge(list(edge)[0], list(edge)[1])
        nx.draw(G)
        plt.savefig("path.png")
