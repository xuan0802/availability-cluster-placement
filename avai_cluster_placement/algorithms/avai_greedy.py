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
            while vir_nodes:
                placeable = False
                # get one virtual node
                vir_node = vir_nodes[0]
                vir_nodes.remove(vir_node)
                # check computing resources enough or not
                for d in DC:
                    if CA[d] >= RC[vir_node]:
                        self.X[vir_node] = d
                        # decrease resources
                        CA[d] -= RC[vir_node]
                        placeable = True
                        break
                if not placeable:
                    print("unfeasible model")

        # =========================== link mapping algorithm ================================
        # obtain all virtual links
        virtual_links = self.get_virtual_links()
        # map virtual link to physical link
        for vir_link in virtual_links:
            # get the physical nodes
            phy_node_0 = self.X[vir_link[0]]
            phy_node_1 = self.X[vir_link[1]]
            if phy_node_0 == phy_node_1:
                self.U[vir_link] = []
                continue

            # remove all physical links not enough bandwidth
            graph = Graph(EG)
            for link_ in EG:
                if BW[link_] <= RB[vir_link[0], vir_link[1]]:
                    graph.remove_edge(link_[0], link_[1])
                    graph.remove_edge(link_[1], link_[0])

            # run shortest path algorithm to find best path
            path = graph.dijkstra(phy_node_0, phy_node_1)

            # update results and decrease bandwidth resources
            self.U[vir_link] = []
            edge_path = self.get_path_edges(path)
            for e in edge_path:
                self.U[vir_link].append(e)
                BW[e] -= RB[vir_link]









