from .Algorithms import Algorithm
from copy import deepcopy
import itertools
from .Dijktra import Graph
import random


class AvailGreedy(Algorithm):
    def run(self):
        CA = self.topo['CA']
        DC = self.topo['DC']
        EG = self.topo['EG']
        BW = self.topo['BW']
        AvN = self.topo['AvN']

        CR = self.req['CR']
        ACT = self.req['ACT']
        STB = self.req['STB']

        resource_demand = self.calResourceDemand()
        RB = resource_demand['RB']
        RC = resource_demand['RC']

        # ================== node mapping algorithm =========================================
        # sort requests according to number of virtual nodes
        req_num = {}
        for r in CR:
            req_num[r] = len(ACT[r]) + len(STB[r])
        CR.sort(key=lambda x: req_num[x], reverse=True)

        # for each request, try to place each virtual node on node with highest availability and enough resources first
        for r in CR:
            vir_nodes = ACT[r] + STB[r]
            # sort nodes according availability
            DC.sort(key=lambda x: AvN[x], reverse=True)
            # place virtual node on physical node
            visited_nodes = list()
            while vir_nodes:
                placeable = False
                # get one virtual node
                vir_node = vir_nodes[0]
                # check computing resources enough or not
                for d in DC:
                    if CA[d] >= RC[vir_node] and (d not in visited_nodes):
                        self.X[vir_node] = d
                        # decrease resources
                        CA[d] -= RC[vir_node]
                        placeable = True
                        vir_nodes.remove(vir_node)
                        if len(visited_nodes) <= 3:
                            visited_nodes.append(d)
                        break
                if not placeable:
                    print("unfeasible model")

        # =========================== link mapping algorithm ================================
        # obtain all virtual links
        virtual_links = self.get_virtual_links()
        # map virtual link to physical link
        self.shortest_path_link_map(virtual_links, RB)








