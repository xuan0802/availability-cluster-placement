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
                # create lists to iterate while removing elements inside
                EG_rep = deepcopy(EG_)
                DC_rep = deepcopy(DC_)

                for e in EG_rep:
                    if BW[e] < RB[center_vir_node, edge_vir_nodes[0]]:
                        EG_.remove(e)
                for d in DC_rep:
                    # remove nodes and associated links which do not have enough resources
                    if CA[d] < RC[edge_vir_nodes[0]]:
                        DC_.remove(d)
                        self.remove_links(d, EG_)
                neighbors = self.get_neighbors(EG_, DC_)
                DC_rep = deepcopy(DC_)
                for d in DC_rep:
                    # remove nodes which do not have usable links
                    if not neighbors[d]:
                        DC_.remove(d)

                # calculate the rank, rank = number of usable links
                neighbors = self.get_neighbors(EG_, DC_)

                phy_node_rank = {}
                for d in DC_:
                    phy_node_rank[d] = len(neighbors[d])

                # sort nodes according to rank
                DC_.sort(key=lambda x: phy_node_rank[x], reverse=True)
                # map request to physical node with highest rank first
                for d in DC_:
                    # place_nodes used to check node already placed
                    placed_nodes = list()
                    # req_place_result, req_routing_result used to store temporarily placement for one results
                    req_place_result = dict()
                    req_routing_result = dict()
                    edge_vir_nodes_ = deepcopy(edge_vir_nodes)
                    # variables to store temporarily resources
                    CA_ = deepcopy(CA)
                    BW_ = deepcopy(BW)
                    # if physical node has enough resources to host center virtual node
                    if CA_[d] >= RC[center_vir_node]:
                        # make a shortest tree with availability
                        shortestTree = ShortestTree(DC, EG, d, AvN)
                        tree_root = shortestTree.build_shortest_tree()
                        # place virtual nodes in turn on physical nodes of shortest tree
                        # temporarily store results
                        req_place_result[center_vir_node] = d
                        CA_[d] -= RC[center_vir_node]
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
                                if edge_vir_nodes_:
                                    if tree_node.name not in placed_nodes:
                                        edge_vir_node = edge_vir_nodes_[0]
                                        vir_link = (center_vir_node, edge_vir_node)
                                        reverse_path = list()
                                        shortestTree.traverse_back(tree_node, reverse_path)
                                        reverse_path_edges = self.get_path_edges(reverse_path)
                                        if CA[tree_node.name] >= RC[edge_vir_node] and all(BW[e] >=
                                                                                           RB[vir_link]
                                                                                           for e in
                                                                                           reverse_path_edges):
                                            # if resources satisfy, do temporary placement, decrease resources
                                            req_place_result[edge_vir_node] = tree_node.name
                                            placed_nodes.append(tree_node.name)
                                            CA_[tree_node.name] -= RC[edge_vir_node]
                                            req_routing_result[vir_link] = list()
                                            for e in reverse_path_edges:
                                                BW_[e] -= RB[vir_link]
                                                req_routing_result[vir_link].append(e)
                                            # remove edge node from place list
                                            edge_vir_nodes_.pop(0)
                                        else:
                                            continue
                                    else:
                                        continue
                                else:
                                    req_placed = True
                                    break

                            # if not placed all edge virtual nodes
                            if not req_placed:
                                k += 1
                            # if all edge virtual nodes placed
                            else:
                                break
                        if req_placed:
                            break
                        else:
                            continue

                if req_placed:
                    # do real placement, decrease real resources
                    for vir_node in req_place_result.keys():
                        self.X[vir_node] = req_place_result[vir_node]
                        CA[req_place_result[vir_node]] -= RC[vir_node]
                    for vir_link in req_routing_result.keys():
                        self.U[vir_link] = deepcopy(req_routing_result[vir_link])
                        for e in req_routing_result[vir_link]:
                            BW[e] -= RB[vir_link]
                else:
                    # do random placement for unplaced requests
                    self.random_placement(r, RC, RB)

            else:
                if topo_type == 'mesh':
                    # determine node number
                    node_num = len(ACT[r]) + len(STB[r])
                    peer_nodes = ACT[r] + STB[r]

                    # create a list of possible combinations
                    combination_list = list(itertools.combinations(DC, node_num))

                    # remove combination not enough resources
                    combination_list_rep = deepcopy(combination_list)
                    for comb in combination_list_rep:
                        if min(CA[i] for i in comb) < RC[peer_nodes[0]]:
                            combination_list.remove(comb)

                    # calculate number of usable links
                    usable_link_num = {}
                    for comb in combination_list:
                        comb_usable_link_num = 0
                        comb_pos_links = list(itertools.combinations(comb, 2))
                        for i in comb_pos_links:
                            if any(elem in EG for elem in list(itertools.permutations(i, 2))):
                                comb_usable_link_num = comb_usable_link_num + 1
                        usable_link_num[comb] = comb_usable_link_num

                    # sort according to usable link number
                    combination_list.sort(key=lambda x: usable_link_num[x], reverse=True)
                    if combination_list:
                        selected_comb = combination_list[0]
                        for i in range(len(selected_comb)):
                            self.X[peer_nodes[i]] = selected_comb[i]
                            CA[selected_comb[i]] = CA[selected_comb[i]] - RC[peer_nodes[0]]
                        req_placed = True

                    if req_placed:
                        # get virtual links
                        vir_links = self.get_virtual_links_one_req(r)
                        # do link mapping
                        self.shortest_path_link_map(vir_links, RB)
                    else:
                        self.random_placement(r, RC, RB)

    def random_placement(self, req, RC, RB):
        CA = self.topo['CA']
        DC = self.topo['DC']
        EG = self.topo['EG']
        BW = self.topo['BW']
        AvN = self.topo['AvN']

        ACT = self.req['ACT']
        STB = self.req['STB']

        # =========================== random node placement algorithm ================================
        vir_nodes = ACT[req] + STB[req]
        vir_links = self.get_virtual_links_one_req(req)

        while vir_nodes:
            req_placed = False
            # get one virtual node
            vir_node = vir_nodes[0]
            # check computing resources enough or not
            for d in DC:
                if CA[d] >= RC[vir_node]:
                    self.X[vir_node] = d
                    # decrease resources
                    CA[d] -= RC[vir_node]
                    req_placed = True
                    break
            if not req_placed:
                print("can not place")

        # =========================== shortest path link mapping algorithm ================================
        self.shortest_path_link_map(vir_links, RB)