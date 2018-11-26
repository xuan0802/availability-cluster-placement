from avai_cluster_placement.topos.initilize_topo import initialize_topo
from avai_cluster_placement.evaluation.evaluation import evaluate
from copy import deepcopy
import importlib
from avai_cluster_placement.simulation_scenarios.scenarios import *
from avai_cluster_placement.visualization.visualization import *
from avai_cluster_placement.utilities import *


def run_and_evaluate_algorithms(req_name_list, requests):
    # define data structure to store performance results
    bw_gr = dict()
    av_gr = dict()
    ta_re = dict()
    co_gr = dict()
    bw_gr['label'] = "BWGR"
    av_gr['label'] = "AVGR"
    co_gr['label'] = "COGR"
    ta_re['label'] = "TARE"
    for data in FIG_TITLE_DATA_MAP.values():
        bw_gr[data] = dict()
        av_gr[data] = dict()
        ta_re[data] = dict()
        co_gr[data] = dict()

    # run algorithms
    algo_perf_map = {"TARE": ta_re, "AvailGreedy": av_gr, "BWGreedy": bw_gr, "ComGreedy": co_gr}
    # run algorithms with different requests
    for algo in ALGO_NAME_LIST:
        print("--------------------" + algo + "--------------------------")
        module = importlib.import_module("avai_cluster_placement.algorithms." + algo)
        for req_name in req_name_list:
            aver_avail_list = list()
            total_bw_list = list()
            i = 0
            print(req_name)
            for req in requests[req_name]:
                i += 1
                print(i)
                algo_instance = getattr(module, algo)(deepcopy(topo), deepcopy(req))
                algo_instance.run()
                perf = evaluate(algo_instance.get_results(), deepcopy(req), deepcopy(topo))
                aver_avail_list.append(perf["aver_avai"])
                total_bw_list.append(perf["total_bw"])

            algo_perf_map[algo]["aver_avail"][req_name] = aver_avail_list
            algo_perf_map[algo]["total_bw"][req_name] = total_bw_list

    return algo_perf_map


if __name__ == "__main__":
    # create a physical topology
    network = "geant"
    topo = initialize_topo(network)
    # save topo in a file
    save_to_file(topo, "topo_json/topo_" + network + ".json")
    # load topo from a file
    topo = load_topo("topo_json/topo_" + network + ".json")

    # create request scenario
    scenario_name = "vary_type"
    if scenario_name == "vary_num":
        scenario_req = vary_request_number(100)
    else:
        if scenario_name == "vary_type":
            scenario_req = vary_request_type(100)

    # run algorithms and evaluate
    algo_perf_map = run_and_evaluate_algorithms(scenario_req["req_list"], scenario_req["requests"])
    save_to_file(algo_perf_map, "results_json/results_" + network + "_" + scenario_name + ".json")
    # algo_perf_map = load_perf_results("results_json/results_" + network + "_" + scenario_name + ".json")

    # visualize results
    draw_scenarios(scenario_name, algo_perf_map)




