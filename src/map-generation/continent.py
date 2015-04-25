from node import Node
import random


class Continent():

    # Generates a continent
    # ARGS - Graph Object, Number of ISPs per continent, Number of cities per ISP

    def __init__(self, graph, num_ISPs, cities_per_ISP):
        # Init  
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

    # Generates a ISP and its cities
    # ARGS - Graph Object, Number of cities per ISP

    def generate_ISP(self, graph, cities_per_ISP):
        isp = Node.get_ISP_node(graph) #
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

    # Connect two continents given unique isps per continent
    def connect_continent(self, graph, continent, r_isp, s_isp, r_per_isp, s_per_isp):
        if s_isp > len(self.isp_list):
            raise Exception('Invalid number of edges for isp1')
        if r_isp > len(continent.isp_list):
            raise Exception('Invalid number of edges for isp2')

        used_isp_list_send = []
        used_isp_list_recv = []
        if r_isp > s_isp:
            while len(used_isp_list_send) != s_isp:
                isp1 = self.get_random_isp()
                while isp1.uid in used_isp_list_send:
                    isp1 = self.get_random_isp()
                isp2 = continent.get_random_isp()
                while isp2.uid in used_isp_list_recv:
                    isp2 = continent.get_random_isp()
                used_isp_list_send.append(isp1.uid)
                used_isp_list_recv.append(isp2.uid)
                self.connent_continent_isp(graph, continent, isp1, isp2, s_per_isp, r_per_isp)
            for _ in range(r_isp - s_isp):
                used_isp_list_send = random.shuffle(used_isp_list_send)
                isp1 = used_isp_list_send[0]
                isp2 = continent.get_random_isp()
                while isp2.uid not in used_isp_list_recv:
                    isp2 = continent.get_random_isp()
                used_isp_list_recv.append(isp2.uid)
                self.connent_continent_isp(graph, continent, isp1, isp2, s_per_isp, r_per_isp)
        else:
            while len(used_isp_list_recv) != r_isp:
                isp1 = self.get_random_isp()
                while isp1.uid in used_isp_list_send:
                    isp1 = self.get_random_isp()
                isp2 = continent.get_random_isp()
                while isp2.uid in used_isp_list_recv:
                    isp2 = continent.get_random_isp()
                used_isp_list_send.append(isp1.uid)
                used_isp_list_recv.append(isp2.uid)
                self.connent_continent_isp(graph, continent, isp1, isp2, s_per_isp, r_per_isp)
            for _ in range(s_isp - r_isp):
                used_isp_list_recv = random.shuffle(used_isp_list_recv)
                isp1 = used_isp_list_recv[0]
                isp2 = self.get_random_isp()
                while isp2.uid not in used_isp_list_send:
                    isp2 = self.get_random_isp()
                used_isp_list_send.append(isp2.uid)
                self.connent_continent_isp(graph, continent, isp2, isp1, s_per_isp, r_per_isp)

    # Connects two isps given a number of cities to connect for each isp
    def connent_continent_isp(self, graph, continent, isp1, isp2, unique_cities_isp1, unique_cities_isp2):
        if unique_cities_isp1 > len(self.isps_city_list[self.isp_list.index(isp1)]):
            raise Exception('Invalid number of edges for isp1')
        if unique_cities_isp2 > len(continent.isps_city_list[continent.isp_list.index(isp2)]):
            raise Exception('Invalid number of edges for isp2')

        used_city_list_isp1 = []
        used_city_list_isp2 = []
        if unique_cities_isp2 > unique_cities_isp1:
            while len(used_city_list_isp1) != unique_cities_isp1:
                city1 = self.get_random_city(isp1)
                while city1.uid in used_city_list_isp1:
                    city1 = self.get_random_city(isp1)
                city2 = continent.get_random_city(isp2)
                while city2.uid in used_city_list_isp2:
                    city2 = continent.get_random_city(isp2)
                used_city_list_isp1.append(city1.uid)
                used_city_list_isp2.append(city2.uid)
                graph.add_edge(city1, city2)
            for _ in range(unique_cities_isp2 - unique_cities_isp1):
                used_city_list_isp1 = random.shuffle(used_city_list_isp1)
                city1 = used_city_list_isp1[0]
                city2 = continent.get_random_city(isp2)
                while city2.uid in used_city_list_isp2:
                    city2 = continent.get_random_city(isp2)
                used_city_list_isp2.append(city2.uid)
                graph.add_edge(city1, city2)
        else:
            while len(used_city_list_isp2) != unique_cities_isp2:
                city2 = continent.get_random_city(isp2)
                while city2.uid in used_city_list_isp2:
                    city2 = continent.get_random_city(isp2)
                city1 = self.get_random_city(isp1)
                while city1.uid in used_city_list_isp1:
                    city1 = self.get_random_city(isp1)
                used_city_list_isp2.append(city2.uid)
                used_city_list_isp1.append(city1.uid)
                graph.add_edge(city2, city1)
            for _ in range(unique_cities_isp1 - unique_cities_isp2):
                used_city_list_isp2 = random.shuffle(used_city_list_isp2)
                city2 = used_city_list_isp2[0]
                city1 = self.get_random_city(isp1)
                while city1.uid in used_city_list_isp1:
                    city1 = self.get_random_city(isp1)
                used_city_list_isp1.append(city1.uid)
                graph.add_edge(city2, city1)

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
