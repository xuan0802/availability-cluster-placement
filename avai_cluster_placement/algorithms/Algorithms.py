from copy import copy, deepcopy


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
        ACT = self.req['ACT']
        STB = self.req['STB']
        virtual_links = []
        for r in CR:
            if r[0:4] == 'reqA':
                for a in ACT[r]:
                    for s in STB[r]:
                        virtual_links.append((a, s))
            else:
                if r[0:4] == 'reqB':
                    for a in ACT[r]:
                        for s in STB[r]:
                            virtual_links.append((s, a))
                else:
                    if r[0:4] == 'reqC':
                        for a in ACT[r]:
                            for a_ in ACT[r]:
                                if a != a_:
                                    if (a_, a) not in virtual_links:
                                        virtual_links.append((a, a_))
        return virtual_links

    # obtain all virtual links
    def get_virtual_links_one_req(self, req):
        ACT = self.req['ACT']
        STB = self.req['STB']
        virtual_links = []

        if req[0:4] == 'reqA':
            for a in ACT[req]:
                for s in STB[req]:
                    virtual_links.append((a, s))
        else:
            if req[0:4] == 'reqB':
                for a in ACT[req]:
                    for s in STB[req]:
                        virtual_links.append((s, a))
            else:
                if req[0:4] == 'reqC':
                    for a in ACT[req]:
                        for a_ in ACT[req]:
                            if a != a_:
                                if (a_, a) not in virtual_links:
                                    virtual_links.append((a, a_))
        return virtual_links

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



