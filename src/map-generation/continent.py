from node import Node
import random


class Continent():

    def __init__(self, graph, num_ISPs, cities_per_ISP):
        self.isp_list = []
        self.datacenter_list = []
        self.isps_city_list = []
        for _ in range(num_ISPs):
            isp = self.generate_ISP(graph, cities_per_ISP)
            datacenter = self.generate_datacenter(graph)

            self.isp_list.append(isp)
            self.datacenter_list.append(datacenter)

            graph.add_edge(isp, datacenter)
            if len(self.isp_list) != 1:
                graph.add_edge(isp, self.isp_list[-2])
                graph.add_edge(datacenter, self.datacenter_list[-2])
        if len(self.isp_list) > 1:
            graph.add_edge(self.isp_list[0], self.isp_list[-1])
            graph.add_edge(self.datacenter_list[0], self.datacenter_list[-1])

    def generate_ISP(self, graph, cities_per_ISP):
        isp = Node.get_ISP_node(graph)
        isp_city_list = []
        for _ in range(cities_per_ISP):
            isp_city_list.append(Node.get_large_city_node(graph))

        for city1 in isp_city_list:
            graph.add_edge(isp, city1)
            for city2 in isp_city_list:
                if city1.uid is not city2.uid:
                    graph.add_edge(city1, city2)
        self.isps_city_list.append(isp_city_list)

        return isp

    def generate_datacenter(self, graph):
        return Node.get_DC_node(graph)

    def connect_continent(self, graph, continent, num_recieving_isp, num_sending_isp, edges_per_isp):
        used_recieving_isp_list = []
        used_sending_isp_list = []
        while len(used_sending_isp_list) != num_sending_isp:
            sending_isp = self.get_random_isp()
            if sending_isp.uid not in used_sending_isp_list:
                used_sending_isp_list.append(sending_isp.uid)
                recieving_isp = continent.get_random_isp()
                while recieving_isp.uid in used_recieving_isp_list:
                    recieving_isp = continent.get_random_isp()
                for _ in range(edges_per_isp):
                    city1 = continent.get_random_city(recieving_isp)
                    city2 = self.get_random_city(sending_isp)
                    graph.add_edge(city1, city2)

    def get_random_isp(self):
        return self.isp_list[random.randint(0, len(self.isp_list) - 1)]

    def get_random_city(self, isp=None):
        if isp is None:
            isp = self.get_random_isp()
        isp_index = self.isp_list.index(isp)
        return self.isps_city_list[isp_index][random.randint(0, len(self.isps_city_list[isp_index]) - 1)]

    def __str__(self):
        s = ""
        for i in range(len(self.isp_list)):
            s += repr(self.isp_list[i])
            s += repr(self.isps_city_list[i]) + "\n"
        for i in range(len(self.datacenter_list)):
            s += repr(self.datacenter_list[i]) + "\n"
        return s
