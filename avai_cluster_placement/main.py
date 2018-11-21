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
    requests = {}
    req_num_list = [i for i in range(10) if i >= 1]
    req_name_list = list()
    for req_num in req_num_list:
        req_name_list.append("req_num" + str(req_num))

    for req_name in req_name_list:
        requests[req_name] = list()

    for req_num in req_num_list:
        for i in range(10):
            req = request_generator(req_num, req_num, req_num)
            requests["req_num" + str(req_num)].append(req)

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
        bw_gr[data] = dict()
        av_gr[data] = dict()
        ta_re[data] = dict()
        co_gr[data] = dict()

    # a list of algorithms
    algo_name_list = ["TARE", "AvailGreedy", "BWGreedy", "ComGreedy"]
    algo_perf_map = {"TARE": ta_re, "AvailGreedy": av_gr, "BWGreedy": bw_gr, "ComGreedy": co_gr}
    # run algorithms with different requests
    for algo in algo_name_list:
        print("--------------------" + algo + "--------------------------")
        module = importlib.import_module("avai_cluster_placement.algorithms." + algo)
        for req_name in req_name_list:
            aver_avail_list = list()
            total_bw_list = list()
            i = 0
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

    # make plots
    fig_title_list = ['Average availability', 'Total bandwidth usage (Mbps)']
    for fig_title in fig_title_list:
        draw_line_chart(req_num_list, fig_title, bw_gr, av_gr, ta_re, co_gr)


def vary_request_type():
    # generate 10 requests for each type
    req_types = ["oAmS", "mAoS", "mA"]
    requests = {}
    for req_type in req_types:
        requests[req_type] = list()

    req_nums = [2*i for i in range(12) if i > 10]
    for req_num in req_nums:
        req = request_generator(req_num, 0, 0)
        requests["oAmS"].append(req)
        req = request_generator(0, req_num, 0)
        requests["mAoS"].append(req)
        req = request_generator(0, 0, req_num)
        requests["mA"].append(req)

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

    # a list of algorithms
    algo_name_list = ["TARE", "AvailGreedy", "BWGreedy", "ComGreedy"]
    algo_perf_map = {"TARE": ta_re, "AvailGreedy": av_gr, "BWGreedy": bw_gr, "ComGreedy": co_gr}
    # run algorithms with different requests
    for algo in algo_name_list:
        print("--------------------" + algo + "--------------------------")
        module = importlib.import_module("avai_cluster_placement.algorithms." + algo)
        for req_type in req_types:
            aver_avail_list = list()
            total_bw_list = list()
            i = 0
            for req in requests[req_type]:
                i += 1
                print(i)
                algo_instance = getattr(module, algo)(deepcopy(topo), deepcopy(req))
                algo_instance.run()
                perf = evaluate(algo_instance.get_results(), deepcopy(req), deepcopy(topo))
                aver_avail_list.append(perf["aver_avai"])
                total_bw_list.append(perf["total_bw"])
            print(req_type)

            algo_perf_map[algo]["aver_avail"][req_type] = aver_avail_list
            algo_perf_map[algo]["total_bw"][req_type] = total_bw_list

    # create plots
    # create list of ticks on x axis
    xtick = ["oAmS", "mAoS", "mA"]

    fig_title_list = ['Average availability', 'Total bandwidth usage (Mbps)']
    for fig_title in fig_title_list:
        draw_bar_chart(xtick, fig_title, bw_gr, av_gr, co_gr, ta_re)


if __name__ == "__main__":
    # # """run all algorithms and make plots"""
    network = "geant"
    topo_ = initialize_topo(network)
    # save topo in a file
    save_to_file(topo_, "topo_json/topo_" + network + ".json")
    # load topo from a file
    topo = load_topo("topo_json/topo_" + network + ".json")
    # vary_request_type()
    vary_request_number()

