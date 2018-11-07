from avai_cluster_placement.algorithms.Algorithms import Algorithm


def evaluate(result, request, topology):
    # get placement and routing results
    placement = result['placement']
    routing = result['routing']
    # get resource demand for each request
    algo = Algorithm(topology, request)
    CR = request['CR']
    ACT = request['ACT']
    STB = request['STB']
    resource_demand = algo.calResourceDemand()
    RB = resource_demand['RB']
    RC = resource_demand['RC']
    # get topology information
    DC = topology['DC']
    EG = topology['EG']
    AvN = topology['AvN']
    AvL = topology['AvL']

    # calculate bandwidth consumption
    total_bw = 0
    vir_links = algo.get_virtual_links()
    for vir_link in vir_links:
        if vir_link in routing.keys():
            total_bw += len(routing[vir_link])*RB[vir_link]

    # calculate availability
    request_avai = {}
    Av_soft = 0.9
    for r in CR:
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
                            vir_links_stb = algo.get_virtual_links_one_stb(r, v)
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

                            temp *= (1 - Av_soft*Av_link_stb)
            # availability of all vir nodes
            function_avai[d] = 1 - temp
        temp = 1
        for d in DC:
            # add availability of physical node
            temp *= 1 - AvN[d]*function_avai[d]
        request_avai[r] = 1 - temp
    average_req_avai = sum(request_avai[r] for r in CR)/len(CR)

    return {'total_bw': total_bw, 'aver_avai': average_req_avai}

