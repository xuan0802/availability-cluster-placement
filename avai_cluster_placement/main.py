from avai_cluster_placement.requests.request import request_generator
from avai_cluster_placement.topos.initilize_topo import initialize_topo
from avai_cluster_placement.evaluation import evaluate
from copy import deepcopy
from avai_cluster_placement.utilities import save_to_file, load_topo
from avai_cluster_placement.constants import *
import importlib
from avai_cluster_placement.utilities import *


def vary_request_number():
    # generate different requests
    requests = []
    req_num_list = [i for i in range(10) if i >= 1]
    for i in req_num_list:
        req = request_generator(i, i, i)
        requests.append(req)
    # save requests in a file
    save_to_file(requests, "req_json/req.json")

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
        bw_gr[data] = list()
        av_gr[data] = list()
        ta_re[data] = list()
        co_gr[data] = list()

    # a list of algorithms
    algo_name_list = ["TARE", "AvailGreedy", "BWGreedy", "ComGreedy"]
    algo_perf_map = {"TARE": ta_re, "AvailGreedy": av_gr, "BWGreedy": bw_gr, "ComGreedy": co_gr}
    # run algorithms with different requests
    for algo in algo_name_list:
        print("--------------------" + algo + "--------------------------")
        module = importlib.import_module("avai_cluster_placement.algorithms." + algo)
        for req in requests:
            algo_instance = getattr(module, algo)(deepcopy(topo), deepcopy(req))
            algo_instance.run()
            perf = evaluate(algo_instance.get_results(), deepcopy(req), deepcopy(topo))
            algo_perf_map[algo]["aver_avail"].append(perf["aver_avai"])
            algo_perf_map[algo]["total_bw"].append(perf["total_bw"])

    # make plots
    fig_title_list = ['Average availability', 'Total bandwidth usage (Mbps)']
    for fig_title in fig_title_list:
        draw_line_chart(req_num_list, fig_title, bw_gr, av_gr, ta_re, co_gr)


def vary_request_type():
    # generate requests
    requests = []
    request_num = 20
    # create each type of request
    req = request_generator(request_num, 0, 0)
    requests.append(req)
    req = request_generator(request_num, 0, 0)
    requests.append(req)
    req = request_generator(0, 0, request_num)
    requests.append(req)

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
        bw_gr[data] = list()
        av_gr[data] = list()
        ta_re[data] = list()
        co_gr[data] = list()

    # a list of algorithms
    algo_name_list = ["TARE", "AvailGreedy", "BWGreedy", "ComGreedy"]
    algo_perf_map = {"TARE": ta_re, "AvailGreedy": av_gr, "BWGreedy": bw_gr, "ComGreedy": co_gr}
    # run algorithms with different requests
    for algo in algo_name_list:
        print("--------------------" + algo + "--------------------------")
        module = importlib.import_module("avai_cluster_placement.algorithms." + algo)
        for req in requests:
            algo_instance = getattr(module, algo)(deepcopy(topo), deepcopy(req))
            algo_instance.run()
            perf = evaluate(algo_instance.get_results(), deepcopy(req), deepcopy(topo))
            algo_perf_map[algo]["aver_avail"].append(perf["aver_avai"])
            algo_perf_map[algo]["total_bw"].append(perf["total_bw"])

    # create plots
    # create list of ticks on x axis
    xtick = ["oAmS", "mAoS", "mA"]

    fig_title_list = ['Average availability', 'Total bandwidth usage (Mbps)']
    for fig_title in fig_title_list:
        draw_bar_chart(xtick, fig_title, bw_gr, av_gr, co_gr, ta_re)


if __name__ == "__main__":
    # # """run all algorithms and make plots"""
    network = "usa"
    # topo_ = initialize_topo(network)
    # # save topo in a file
    # save_to_file(topo_, "topo_json/topo_" + network + ".json")
    # # load topo from a file
    topo = load_topo("topo_json/topo_" + network + ".json")
    vary_request_type()
    # vary_request_number()

