from .Algorithms import Algorithm
from avai_cluster_placement.constants import *
from copy import deepcopy


class BWGreedy(Algorithm):
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
        req_size = {}
        for r in CR:
            req_size[r] = len(ACT[r]) + len(STB[r])
        CR.sort(key=lambda x: req_size[x], reverse=True)

        # for each request, try to place each virtual node on node having highest bandwidth on all links
        for r in CR:
            # sort nodes according total bandwidth on all associated links
            bw_total = {}
            for d in DC:
                bw_temp = 0
                for e in EG:
                    if d in e:
                        bw_temp += BW[e]
                bw_total[d] = bw_temp
            DC.sort(key=lambda x: bw_total[x], reverse=True)

            # place virtual nodes on physical nodes
            H = 2
            while H <= len(ACT[r] + STB[r]):
                vir_nodes = ACT[r] + STB[r]
                visited_nodes = list()
                req_place_result = dict()
                req_routing_result = dict()
                while vir_nodes:
                    req_placed = False
                    # get one virtual node
                    vir_node = vir_nodes[0]
                    # check computing resources enough or not
                    for d in DC:
                        if CA[d] >= RC[vir_node] and (d not in visited_nodes):
                            req_place_result[vir_node] = d
                            vir_nodes.remove(vir_node)
                            if len(visited_nodes) <= H:
                                visited_nodes.append(d)
                            break
                    if not vir_nodes:
                        req_placed = True

                if not req_placed:
                    print("unfeasible model")
                else:
                    # map virtual links on physical links
                    virtual_links = self.get_virtual_links_one_req(r)
                    req_routing_result = self.shortest_path_link_map(req_place_result, virtual_links, RB)

                # check availability of placement for one request
                Av_r = self.calculateAvai(r, req_place_result, req_routing_result)
                if Av_r >= Av_min and req_placed:
                    # do real placement and routing, decrease real resources
                    for vir_node in req_place_result.keys():
                        self.X[vir_node] = req_place_result[vir_node]
                        CA[req_place_result[vir_node]] -= RC[vir_node]
                    for vir_link in req_routing_result.keys():
                        self.U[vir_link] = deepcopy(req_routing_result[vir_link])
                        for e in req_routing_result[vir_link]:
                            BW[e] -= RB[vir_link]
                    break
                else:
                    # increase level of distribution by changing H
                    H += 1
