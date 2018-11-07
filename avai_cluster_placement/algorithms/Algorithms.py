from copy import copy, deepcopy
from .Dijktra import Graph


class Algorithm:
    def __init__(self, topo, req):
        self.topo = topo
        self.req = req
        self.X = {}
        self.U = {}

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
    def shortest_path_link_map(self, vir_links, RB):
        EG = self.topo['EG']
        BW = self.topo['BW']

        # map virtual link to physical link
        for vir_link in vir_links:
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

