import ujson
from ast import literal_eval


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


def load_perf_results(filename):
    f = open(filename)
    perf_results = ujson.load(f)
    f.close()
    return perf_results
