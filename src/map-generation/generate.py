from continent import Continent
from graph import Graph
import networkx as nx
import matplotlib.pyplot as plt


def generate(graph, num_continents, isp_per_continents, cities_per_isp):
    continent_list = []
    for i in range(num_continents):
        continent_list.append(Continent(graph, isp_per_continents, cities_per_isp))
        if i != 0:
            continent_list[i].connect_continent(graph, continent_list[i - 1], 2, 2, 2)


def convert_to_json(graph, continent_list):
    json = {}
    for continent in continent_list:
        pass

if __name__ == "__main__":
    graph = Graph()
    G = nx.Graph()
    json = generate(graph, 2, 2, 3)
    for vertex in graph.vertex_list:
        G.add_node(vertex.uid)
    for edge in graph.edge_list:
        G.add_edge(list(edge)[0], list(edge)[1])
    nx.draw(G)
    plt.savefig("path.png")
