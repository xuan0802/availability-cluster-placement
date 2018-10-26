from .Algorithms import Algorithm
from copy import deepcopy
import itertools
from .ShortestTree import ShortestTree


class TARE(Algorithm):
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

        # ================== algorithm ==============================================
        # sort requests according to number of virtual nodes
        req_num = {}
        for r in CR:
            req_num[r] = len(ACT[r]) + len(STB[r])
        CR.sort(key=lambda x: req_num[x], reverse=True)

        # for each request, try to find the best matched topology first
        for r in CR:
            req_placed = False
            # determine request topology and request size
            if r[0:4] == 'reqA' or r[0:4] == 'reqB':
                topo_type = 'star'
            else:
                if r[0:4] == 'reqC':
                    topo_type = 'mesh'

            # if topology is star
            if topo_type == 'star':
                EG_ = deepcopy(EG)
                DC_ = deepcopy(DC)
                # determine center virtual node and edge virtual nodes
                if r[0:4] == 'reqA':
                    center_vir_node = ACT[r][0]
                    edge_vir_nodes = STB[r]
                else:
                    if r[0:4] == 'reqB':
                        center_vir_node = STB[r][0]
                        edge_vir_nodes = ACT[r]

                # remove nodes and links which do not satisfy computing and bandwidth resource requirements
                for e in EG_:
                    if BW[e] < RB[center_vir_node, edge_vir_nodes[0]]:
                        EG_.remove(e)
                neighbors = self.get_neighbors(EG_, DC_)
                for d in DC_:
                    # remove nodes which do not have usable links
                    if not neighbors[d]:
                        DC_.remove(d)
                    # remove nodes and associated links which do not have enough resources
                    if CA[d] < RC[edge_vir_nodes[0]]:
                        DC_.remove(d)
                        self.remove_links(d, EG_)

                # calculate the rank, rank = number of usable links
                neighbors = self.get_neighbors(EG_, DC_)
                phy_node_rank = {}
                for d in DC_:
                    phy_node_rank[d] = len(neighbors[d])

                # sort nodes according to rank
                DC_.sort(key=lambda x: phy_node_rank[x], reverse=True)
                # map request to physical node with highest rank first
                for d in DC_:
                    # if physical node has enough resources to host center virtual node
                    if CA[d] >= RC[center_vir_node]:
                        # do placement for center node
                        self.X[center_vir_node] = d
                        CA[d] -= RC[center_vir_node]
                        # make a shortest tree with availability
                        shortestTree = ShortestTree(DC_, EG_, d, AvN)
                        tree_root = shortestTree.build_shortest_tree()
                        # place virtual nodes in turn on physical nodes of shortest tree
                        # place_nodes used to check node already placed
                        placed_nodes = list()
                        placed_nodes.append(d)
                        k = 1
                        # place until the end of tree
                        while k <= shortestTree.max_height:
                            tree_nodes = list()
                            shortestTree.get_k_level_nodes(tree_root, k, tree_nodes)
                            # sort nodes at same level according availability
                            tree_nodes.sort(key=lambda x: AvN[x.name], reverse=True)
                            # start placement
                            for tree_node in tree_nodes:
                                if edge_vir_nodes:
                                    if tree_node.name not in placed_nodes:
                                        edge_vir_node = edge_vir_nodes.pop(0)
                                        vir_link = (center_vir_node, edge_vir_node)
                                        reverse_path = list()
                                        shortestTree.traverse_back(tree_node, reverse_path)
                                        reverse_path_edges = self.get_path_edges(reverse_path)
                                        if CA[tree_node.name] >= RC[edge_vir_node] and all(BW[e] >=
                                                                                           RB[vir_link]
                                                                                           for e in
                                                                                           reverse_path_edges):
                                            self.X[edge_vir_node] = tree_node.name
                                            placed_nodes.append(tree_node.name)
                                            CA[tree_node.name] -= RC[edge_vir_node]
                                            self.U[vir_link] = list()
                                            for e in reverse_path_edges:
                                                BW[e] -= RB[vir_link]
                                                self.U[vir_link].append(e)
                                        else:
                                            continue
                                    else:
                                        continue
                                else:
                                    break

                            # if not placed all edge virtual nodes
                            if edge_vir_nodes:
                                k += 1
                                req_placed = True
                            # if all edge virtual nodes placed
                            else:
                                req_placed = True
                                break

                    if req_placed:
                        break
                    else:
                        print(r)
                        print(edge_vir_nodes)
                        print("can not place")

            else:
                if topo_type == 'mesh':
                    # determine node number
                    node_num = len(ACT[r]) + len(STB[r])

                    # create a list of possible combinations
                    combination_list = list(itertools.combinations(DC, node_num))

                    peer_nodes = ACT[r] + STB[r]
                    real_link_num = {}
                    for comb in combination_list:
                        comb_real_link_num = 0
                        comb_pos_link_list = list(itertools.combinations(comb, 2))
                        for i in comb_pos_link_list:
                            if any(elem in EG for elem in list(itertools.permutations(i, 2))):
                                comb_real_link_num = comb_real_link_num + 1
                        real_link_num[comb] = comb_real_link_num
                    combination_list.sort(key=lambda x: real_link_num[x], reverse=True)
                    for comb in combination_list:
                        if min(CA[i] for i in comb) > RC[peer_nodes[0]]:
                            for i in range(len(comb)):
                                self.X[peer_nodes[i]] = comb[i]
                                CA[comb[i]] = CA[comb[i]] - RC[peer_nodes[0]]
                            placeable = True
                            break
                    if placeable:
                        continue
                    else:
                        print("can not place")

