from .Algorithms import Algorithm
from copy import deepcopy
import itertools
from .Dijktra import Graph
from random import choice


class Bandwidth_Greedy(Algorithm):
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

        # for each request, try to place each virtual node on node having highest bandwidth on all links
        for r in CR:
            vir_nodes = ACT[r] + STB[r]
            # place virtual node on physical node
            visited_nodes = list()
            # sort nodes according total bandwidth on all associated links
            bw_total = {}
            for d in DC:
                bw_temp = 0
                for e in EG:
                    if d in e:
                        bw_temp += BW[e]
                bw_total[d] = bw_temp
            DC.sort(key=lambda x: bw_total[x], reverse=True)
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
                        visited_nodes.append(d)
                        break
                if not placeable:
                    print("unfeasible model")

        # =========================== link mapping algorithm ================================
        # obtain all virtual links
        virtual_links = self.get_virtual_links()
        # map virtual link to physical link
        for vir_link in virtual_links:
            link_mappable = True
            # get the physical nodes
            phy_node_0 = self.X[vir_link[0]]
            phy_node_1 = self.X[vir_link[1]]
            if phy_node_0 == phy_node_1:
                self.U[vir_link] = []
                continue

            # remove all physical links not enough bandwidth
            graph = Graph(EG)
            out_of_bw_phy_links = []
            for phy_link in EG:
                if BW[phy_link] <= RB[vir_link[0], vir_link[1]]:
                    graph.update_edge(phy_link[0], phy_link[1], cost=100)
                    out_of_bw_phy_links.append(phy_link)

            # run shortest path algorithm to find best path
            path = graph.dijkstra(phy_node_0, phy_node_1)

            # update results and decrease bandwidth resources
            self.U[vir_link] = []
            # get path in terms of edges, not vertices
            edge_path = self.get_path_edges(path)
            # if path consists of physical links out of bandwidth, then unable to map
            for e in edge_path:
                if e in out_of_bw_phy_links:
                    link_mappable = False
                    print(out_of_bw_phy_links)

            if link_mappable:
                # update routing results, and decrease resources
                for e in edge_path:
                    self.U[vir_link].append(e)
                    BW[e] -= RB[vir_link]
            else:
                print("can not map link")








