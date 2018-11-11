from random import *

num_act_list = [2, 3, 4, 5]
num_stb_list = [2, 3, 4, 5]
demand_com_list = [10]
demand_bw_list = [10]


def request_generator(oAmS, mAoS, mA):
    CR = []
    ACT = {}
    STB = {}
    RC_u = {}
    RB_u = {}

    for i in range(oAmS):
        req = 'req' + 'A' + str(i)
        CR.append(req)
        num_stb = choice(num_stb_list)
        STB[req] = []
        ACT[req] = []
        for j in range(num_stb):
            STB[req].append(req + 'stb' + str(j))
        ACT[req].append(req + 'act0')
        RC_u[req] = choice(demand_com_list)
        RB_u[req] = choice(demand_bw_list)

    for i in range(mAoS):
        req = 'req' + 'B' + str(i)
        CR.append(req)
        num_act = choice(num_act_list)
        ACT[req] = []
        STB[req] = []
        for j in range(num_act):
            ACT[req].append(req + 'act' + str(j))
        STB[req].append(req + 'stb0')
        RC_u[req] = choice(demand_com_list)
        RB_u[req] = choice(demand_bw_list)

    for i in range(mA):
        req = 'req' + 'C' + str(i)
        CR.append(req)
        num_act = choice(num_act_list)
        ACT[req] = []
        STB[req] = []
        for j in range(num_act):
            ACT[req].append(req + 'act' + str(j))
        RC_u[req] = choice(demand_com_list)
        RB_u[req] = choice(demand_bw_list)

    return {'CR': CR, 'ACT': ACT, 'STB': STB, 'RC_u': RC_u, 'RB_u': RB_u}

