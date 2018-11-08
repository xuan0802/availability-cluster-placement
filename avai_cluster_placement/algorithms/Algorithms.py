from copy import copy, deepcopy
from .Dijktra import Graph
from avai_cluster_placement.constants import *

class Algorithm:
    def __init__(self, topo, req):
        self.topo = topo
        self.req = req
        self.X = {}
        self.U = {}

    # calculate resource demand for requests
    def calResourceDemand(self):
        CR = self.req['CR']
        ACT = self.req['ACT']
        STB = self.req['STB']
        RC_u = self.req['RC_u']
        RB_u = self.req['RB_u']
        RC = {}
        RB = {}

        for r in CR:
            if r[0:4] == 'reqA':
                for a in ACT[r]:
                    RC[a] = RC_u[r]
                for s in STB[r]:
                    RC[s] = RC_u[r]
                    RB[a, s] = RB_u[r]
            else:
                if r[0:4] == 'reqB':
                    for a in ACT[r]:
                        RC[a] = RC_u[r]
                    for s in STB[r]:
                        RC[s] = 0
                        for a in ACT[r]:
                            RC[s] += RC_u[r]
                            RB[s, a] = RB_u[r]
                else:
                    if r[0:4] == 'reqC':
                        for a in ACT[r]:
                            RC[a] = len(ACT) * RC_u[r]
                            for a_ in ACT[r]:
                                if (a != a_) and ((a, a_) not in RB) and ((a_, a) not in RB):
                                    RB[a, a_] = 2 * RB_u[r]
        return {'RB': RB, 'RC': RC}

    # calculate availability of a request
    def calculateAvai(self, r, placement, routing):
        ACT = self.req['ACT']
        STB = self.req['STB']
        DC = self.topo['DC']
        AvL = self.topo['AvL']
        AvN = self.topo['AvN']

        vir_nodes = ACT[r] + STB[r]
        function_avai = {}
        for d in DC:
            # temp used to store unavailability of all vir nodes
            temp = 1
            for v in vir_nodes:
                if placement[v] == d:
                    # if vir node is active
                    if v in ACT[r]:
                        temp *= (1 - Av_soft)
                    else:
                        # if vir node is standby, need to add link availability
                        if v in STB[r]:
                            # get all vir links to standby
                            vir_links_stb = self.get_virtual_links_one_stb(r, v)
                            # temp used to store unavailability of all links to standby
                            temp_ = 1
                            for vir_link in vir_links_stb:
                                # calculate availability for each vir link
                                Av_vir_link = 1
                                for e in routing[vir_link]:
                                    Av_vir_link *= AvL[e]
                                temp_ *= (1 - Av_vir_link)
                            # Availability of all virtual links to standby
                            Av_link_stb = 1 - temp_

                            temp *= (1 - Av_soft * Av_link_stb)
            # availability of all vir nodes
            function_avai[d] = 1 - temp
        temp = 1
        for d in DC:
            # add availability of physical node
            temp *= 1 - AvN[d] * function_avai[d]
        return 1 - temp

    # output: list of neighbors of a node
    def get_neighbors(self, edges, datacenters):
        neighbors = {}
        for n in datacenters:
            neighbors[n] = []
            for e in edges:
                if n in e:
                    for i in e:
                        if i != n:
                            neighbors[n].append(i)
        return neighbors

    # return a link given two nodes
    def get_link(self, n1, n2):
        if (n1, n2) in self.topo['EG']:
            return n1, n2
        else:
            return n2, n1

    # remove associated links of a node
    def remove_links(self, n, edges):
        edges_temp = deepcopy(edges)
        for e in edges_temp:
            if n in e:
                edges.remove(e)

    # obtain all virtual links
    def get_virtual_links(self):
        CR = self.req['CR']
        virtual_links = []
        for r in CR:
            virtual_links_req = self.get_virtual_links_one_req(r)
            for virtual_link in virtual_links_req:
                virtual_links.append(virtual_link)
        return virtual_links

    # obtain all virtual links
    def get_virtual_links_one_req(self, req):
        ACT = self.req['ACT']
        STB = self.req['STB']
        virtual_links_req = []

        if req[0:4] == 'reqA':
            for a in ACT[req]:
                for s in STB[req]:
                    virtual_links_req.append((a, s))
        else:
            if req[0:4] == 'reqB':
                for a in ACT[req]:
                    for s in STB[req]:
                        virtual_links_req.append((s, a))
            else:
                if req[0:4] == 'reqC':
                    for a in ACT[req]:
                        for a_ in ACT[req]:
                            if a != a_:
                                if (a_, a) not in virtual_links_req:
                                    virtual_links_req.append((a, a_))
        return virtual_links_req

    # obtain virtual links of one standby
    def get_virtual_links_one_stb(self, req, stb):
        ACT = self.req['ACT']

        virtual_links_stb = []
        if req[0:4] == 'reqA':
            for a in ACT[req]:
                    virtual_links_stb.append((a, stb))
        else:
            if req[0:4] == 'reqB':
                for a in ACT[req]:
                        virtual_links_stb.append((stb, a))
        return virtual_links_stb

    # print placement results
    def print_results(self):
        print(self.X)
        print(self.U)

    # get results
    def get_results(self):
        return {'placement': self.X, 'routing': self.U}

    # produce a path in the form of edges from a list of vertices
    def get_path_edges(self, vertex_path):
        edge_path = []
        for p in range(len(vertex_path) - 1):
            edge_path.append(self.get_link(vertex_path[p], vertex_path[p + 1]))
        return edge_path

    # find shortest path between two nodes
    def shortest_path_link_map(self, placement, vir_links, RB):
        EG = self.topo['EG']
        BW = self.topo['BW']

        routing_results = dict()
        # map virtual link to physical link
        for vir_link in vir_links:
            link_mappable = True
            # get the physical nodes
            phy_node_0 = placement[vir_link[0]]
            phy_node_1 = placement[vir_link[1]]
            if phy_node_0 == phy_node_1:
                routing_results[vir_link] = []
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
            routing_results[vir_link] = []
            # get path in terms of edges, not vertices
            edge_path = self.get_path_edges(path)
            # if path consists of physical links out of bandwidth, then unable to map
            for e in edge_path:
                if e in out_of_bw_phy_links:
                    link_mappable = False
                    print(out_of_bw_phy_links)

            if link_mappable:
                for e in edge_path:
                    routing_results[vir_link].append(e)
            else:
                print("can not map link")
        return routing_results

    # place and map one request on physical nodes
    def place_map_one_request(self, r, RC, RB, greedy_policy):
        CA = self.topo['CA']
        DC = self.topo['DC']
        EG = self.topo['EG']
        BW = self.topo['BW']
        AvN = self.topo['AvN']

        ACT = self.req['ACT']
        STB = self.req['STB']

        if greedy_policy == "bandwidth":
            # sort nodes according total bandwidth on all associated links
            bw_total = {}
            for d in DC:
                bw_temp = 0
                for e in EG:
                    if d in e:
                        bw_temp += BW[e]
                bw_total[d] = bw_temp
            DC.sort(key=lambda x: bw_total[x], reverse=True)
        else:
            if greedy_policy == "availability":
                # sort nodes according availability
                DC.sort(key=lambda x: AvN[x], reverse=True)

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
                print("Can not place request")
                print(r)
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
