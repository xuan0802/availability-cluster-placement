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
    for r in CR:
        request_avai[r] = algo.calculateAvai(r, placement, routing)
    average_req_avai = sum(request_avai[r] for r in CR)/len(CR)

    return {'total_bw': total_bw, 'aver_avai': average_req_avai}




