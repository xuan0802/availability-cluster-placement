from avai_cluster_placement.constants import *
from matplotlib import pyplot as plt
import numpy as np
from statistics import mean, pstdev


def draw_line_chart(req_num_list, fig_title, *algorithm_results):
    """draw a line chart"""
    req_name_list = list()
    for req_num in req_num_list:
        req_name_list.append("req_num" + str(req_num))
    for result in algorithm_results:
        # calculate mean values and standard deviation
        algo_mean_values = list()
        algo_stddev_values = list()
        for req_name in req_name_list:
            # mean values
            algo_mean_values.append(mean(result[FIG_TITLE_DATA_MAP[fig_title]][req_name]))
            # stand deviation
            algo_stddev_values.append(pstdev(result[FIG_TITLE_DATA_MAP[fig_title]][req_name])/3)
        # draw
        plt.errorbar(req_num_list, algo_mean_values, yerr=algo_stddev_values, color=LABEL_COLOR_MAP[result["label"]],
                     label=result["label"], marker=LABEL_MARKER_MAP[result["label"]], capsize=3, capthick=0.5)

    plt.ylim(FIG_TITLE_YLIMIT_MAP[fig_title])
    plt.xlabel('Request number', fontsize='x-large')
    plt.ylabel(fig_title, fontsize='x-large')
    plt.legend(fontsize='large')
    plt.show()


def draw_bar_chart(xtick, fig_title, *algorithm_results):
    """draw a bar chart"""
    fig, ax = plt.subplots()
    index = np.arange(len(xtick))
    bar_width = 0.2
    opacity = 0.8
    i = 0
    req_type_list = xtick
    for result in algorithm_results:
        # calculate mean values and standard deviation
        algo_mean_values = list()
        algo_stddev_values = list()
        for req_type in req_type_list:
            # mean values
            algo_mean_values.append(mean(result[FIG_TITLE_DATA_MAP[fig_title]][req_type]))
            # stand deviation
            algo_stddev_values.append(pstdev(result[FIG_TITLE_DATA_MAP[fig_title]][req_type]) / 2)
        # draw
        ax.bar(index + i * bar_width, algo_mean_values,
               bar_width, yerr=algo_stddev_values, alpha=opacity, color=LABEL_COLOR_MAP[result["label"]],
               label=result["label"], capsize=4)
        i = i + 1
    ax.set_ylim(FIG_TITLE_YLIMIT_MAP[fig_title])
    ax.set_xlabel('Request Type', fontsize='x-large')
    ax.set_ylabel(fig_title, fontsize='x-large')
    ax.set_xticks(index + bar_width)
    ax.set_xticklabels(xtick)
    ax.legend(fontsize='large')
    fig.tight_layout()
    plt.show()


def draw_scenarios(scenario_name, perf_result):
    fig_title_list = ['Average availability', 'Total bandwidth usage (Mbps)']

    if scenario_name == "vary_type":
        xtick = ["oAmS", "mAoS", "mA"]
        for fig_title in fig_title_list:
            draw_bar_chart(xtick, fig_title, *perf_result.values())
    else:
        if scenario_name == "vary_num":
            req_num_list = [i for i in range(10) if i >= 1]
            for fig_title in fig_title_list:
                draw_line_chart(req_num_list, fig_title, *perf_result.values())
