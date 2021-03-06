from .Algorithms import Algorithm


class ComGreedy(Algorithm):
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

        # sort requests according to number of virtual nodes
        req_size = {}
        for r in CR:
            req_size[r] = len(ACT[r]) + len(STB[r])
        CR.sort(key=lambda x: req_size[x], reverse=True)

        # for each request, try to place each virtual node on node having highest bandwidth on all links
        for r in CR:
            self.RP_SP_one_request(r, RC, RB, "computing")
