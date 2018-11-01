from random import *
import pandas as pd

N_DC = 24


def initialize_topo():
    DC = []
    EG = []
    BW = {}
    CA = {}
    AvN = {}
    AvL = {}

    # a set of cloud centers
    for i in range(N_DC):
        DC.append('dc' + str(i + 1))
    # a set of link between two cloud centers
    df = pd.read_csv("topos/USAnet.csv", delimiter=",")
    for v in df.values:
        EG.append(tuple('dc' + str(x) for x in v))

    # init computing capacity
    center_capacity_list = [1000, 1500, 2500, 5000]
    for n in DC:
        CA[n] = choice(center_capacity_list)

    # init bandwidth capacity
    link_bw_list = [1000, 2000, 5000, 10000]
    for e in EG:
        BW[e] = choice(link_bw_list)

    # init availability values
    avail_list = [0.9, 0.99]
    for n in DC:
        AvN[n] = choice(avail_list)
    for e in EG:
        AvL[e] = choice(avail_list)

    # create input data
    input_topo = dict()
    input_topo['DC'] = DC
    input_topo['EG'] = EG
    input_topo['BW'] = BW
    input_topo['CA'] = CA
    input_topo['AvN'] = AvN
    input_topo['AvL'] = AvL

    return input_topo
