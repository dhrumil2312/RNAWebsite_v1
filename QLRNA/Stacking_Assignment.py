from QLRNA.stacking_env import Stacking
from QLRNA.RL_brain import QLearningTable
from QLRNA.RL_brain import SarsaTable
from QLRNA.RL_brain import SarsaLambdaTable
import pandas as pd
import pickle
import time


with open('QLRNA/stacking_q_learning_q_table_A_U.pickle', 'rb') as ff:
    q_table_A_U = pickle.load(ff)
with open('QLRNA/stacking_q_learning_q_table_C_G.pickle', 'rb') as ff:
    q_table_C_G = pickle.load(ff)
with open('QLRNA/stacking_q_learning_q_table_G_C.pickle', 'rb') as ff:
    q_table_G_C = pickle.load(ff)
with open('QLRNA/stacking_q_learning_q_table_G_U.pickle', 'rb') as ff:
    q_table_G_U = pickle.load(ff)
with open('QLRNA/stacking_q_learning_q_table_U_A.pickle', 'rb') as ff:
    q_table_U_A = pickle.load(ff)
with open('QLRNA/stacking_q_learning_q_table_U_G.pickle', 'rb') as ff:
    q_table_U_G = pickle.load(ff)

# with open('sarsa_ld_q_table_interloop.pickle', 'rb') as ff:
#     q_table = pickle.load(ff)
# with open('sarsa_ld_trace_table_interloop.pickle', 'rb') as fff:
#     trace_table = pickle.load(fff)

# def interloop_assign(shorter_init,longer_init):
#     env = Interloop(shorter_init,longer_init)
#     RL = SarsaLambdaTable(actions=list(range(4)))
#     RL.q_table = RL.q_table.append(q_table)
#     RL.eligibility_trace = RL.eligibility_trace.append(trace_table)
#     observation = env.shorter+"_"+env.longer
#     action = RL.choose_action(observation)
#     n_step = 0
#     while True:
#         n_step += 1
#         shorter_,longer_, reward, done = env.step(action,n_step)
#         observation_ = shorter_+"_"+longer_
#         action_ = RL.choose_action(observation_)
#         RL.learn(str(observation), action, reward, str(observation_),action_)
#         observation = observation_
#         action = action_
#         if done:
#             break
#     shorter_final = observation.split('_')[0]
#     longer_final = observation.split('_')[1]
#     return shorter_final,longer_final


def stacking_assign_q_learning(shorter_init,longer_init):
    env = Stacking(shorter_init,longer_init)
    RL = QLearningTable(actions=list(range(6)),e_greedy = 1)
    if shorter_init[0] == 'A' and longer_init[0] == 'U':
        RL.q_table = RL.q_table.append(q_table_A_U)
    elif shorter_init[0] == 'C' and longer_init[0] == 'G':
        RL.q_table = RL.q_table.append(q_table_C_G)
    elif shorter_init[0] == 'G' and longer_init[0] == 'C':
        RL.q_table = RL.q_table.append(q_table_G_C)
    elif shorter_init[0] == 'G' and longer_init[0] == 'U':
        RL.q_table = RL.q_table.append(q_table_G_U)
    elif shorter_init[0] == 'U' and longer_init[0] == 'A':
        RL.q_table = RL.q_table.append(q_table_U_A)
    elif shorter_init[0] == 'U' and longer_init[0] == 'G':
        RL.q_table = RL.q_table.append(q_table_U_G)

    observation = env.shorter+"_"+env.longer
    while True:
        action = RL.choose_action(observation)
        shorter_,longer_, reward, done = env.step(action)
        observation_ = shorter_+"_"+longer_
        # RL.learn(str(observation), action, reward, str(observation_))
        observation = observation_
        if done:
            break
    shorter_final = observation.split('_')[0]
    longer_final = observation.split('_')[1]
    return shorter_final,longer_final

def RL_Stacking(shorter_start_nt,shorter_end_nt,longer_start_nt,longer_end_nt,shorter_length,longer_length):
    nt_dict = {1:'A',2:'C',3:"G",4:"U"}
    shorter_init = nt_dict[shorter_start_nt] + 'N'*shorter_length +nt_dict[shorter_end_nt]
    longer_init = nt_dict[longer_start_nt] + 'N'*longer_length + nt_dict[longer_end_nt]

    shorter_init = shorter_init[::-1]
    shorter_final,longer_final = stacking_assign_q_learning(shorter_init,longer_init)
    shorter_final = shorter_final[::-1]
    return shorter_final,longer_final
