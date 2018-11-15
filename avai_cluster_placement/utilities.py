import ujson
from ast import literal_eval
from avai_cluster_placement.constants import *
from matplotlib import pyplot as plt
import numpy as np


def save_to_file(input_dict, filename):
    """save topo to a json file"""
    f = open(filename, "w")
    ujson.dump(input_dict, f)
    f.close()


def load_topo(filename):
    # load topo from a file
    EG = []
    BW = {}
    CA = {}
    AvN = {}
    AvL = {}

    f = open(filename)
    topo = ujson.load(f)
    f.close()
    DC = topo['DC']
    for e in topo['EG']:
        EG.append(tuple(e))
    for i in topo['CA'].keys():
        CA[i] = topo['CA'][i]
    for i in topo['BW'].keys():
        BW[literal_eval(i)] = topo['BW'][i]
    for i in topo['AvN'].keys():
        AvN[i] = topo['AvN'][i]
    for i in topo['AvL'].keys():
        AvL[literal_eval(i)] = topo['AvL'][i]

    # create input data
    input = dict()
    input['DC'] = DC
    input['EG'] = EG
    input['CA'] = CA
    input['AvN'] = AvN
    input['AvL'] = AvL
    input['BW'] = BW

    return input


def load_req(filename):
    f = open(filename)
    requests = ujson.load(f)
    f.close()
    return requests


def draw_line_chart(req_num_list, fig_title, *algorithm_results):
    """draw a line chart"""
    for result in algorithm_results:
        plt.plot(req_num_list, result[FIG_TITLE_DATA_MAP[fig_title]], color=LABEL_COLOR_MAP[result["label"]],
                 label=result["label"], marker=LABEL_MARKER_MAP[result["label"]])

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
    for result in algorithm_results:
        ax.bar(index + i * bar_width, result[FIG_TITLE_DATA_MAP[fig_title]],
               bar_width, alpha=opacity, color=LABEL_COLOR_MAP[result["label"]], label=result["label"])
        i = i + 1
    ax.set_ylim(FIG_TITLE_YLIMIT_MAP[fig_title])
    ax.set_xlabel('Request Type', fontsize='x-large')
    ax.set_ylabel(fig_title, fontsize='x-large')
    ax.set_xticks(index + bar_width)
    ax.set_xticklabels(xtick)
    ax.legend(fontsize='large')
    fig.tight_layout()
    plt.show()
