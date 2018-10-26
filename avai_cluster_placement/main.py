from avai_cluster_placement.requests.request import request_generator
from avai_cluster_placement.topos.USANet import initialize_topo
from avai_cluster_placement.algorithms.TARE import TARE
from avai_cluster_placement.algorithms.avai_greedy import AvailGreedy
from avai_cluster_placement.evaluation import evaluate
from copy import deepcopy

if __name__ == "__main__":
    req = request_generator(20, 20, 0)
    topo = initialize_topo()
    req1 = deepcopy(req)
    req2 = deepcopy(req)
    topo1 = deepcopy(topo)
    topo2 = deepcopy(topo)
    req3 = deepcopy(req)
    req4 = deepcopy(req)
    topo3 = deepcopy(topo)
    topo4 = deepcopy(topo)
    x = AvailGreedy(topo3, req3)
    x.run()
    print(evaluate(x.get_results(), req4, topo4))
    y = TARE(topo1, req1)
    y.run()
    print(evaluate(y.get_results(), req2, topo2))
