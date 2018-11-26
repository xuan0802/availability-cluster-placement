from avai_cluster_placement.requests.request import request_generator
import numpy as np


def vary_request_number(rep):
    # generate different requests
    requests = {}
    req_num_list = [i for i in range(10) if i >= 1]
    req_name_list = list()
    for req_num in req_num_list:
        req_name_list.append("req_num" + str(req_num))

    for req_name in req_name_list:
        requests[req_name] = list()

    for req_num in req_num_list:
        for i in range(rep):
            req = request_generator(req_num, req_num, req_num)
            requests["req_num" + str(req_num)].append(req)

    return {"req_list": req_name_list, "requests": requests}


def vary_request_type(rep):
    # generate 10 requests for each type
    req_types = ["oAmS", "mAoS", "mA"]
    requests = {}
    for req_type in req_types:
        requests[req_type] = list()
    req_nums_pool = [i for i in range(20) if i > 5]
    req_nums = np.random.choice(req_nums_pool, rep)
    for req_num in req_nums:
        req = request_generator(req_num, 0, 0)
        requests["oAmS"].append(req)
        req = request_generator(0, req_num, 0)
        requests["mAoS"].append(req)
        req = request_generator(0, 0, req_num)
        requests["mA"].append(req)

    return {"req_list": req_types, "requests": requests}




