from QLRNA.ubp_type_4_env import ubp_4
from QLRNA.RL_brain import QLearningTable
import pickle


with open('QLRNA/ubp_type_4_q_table.pickle', 'rb') as ff:
    q_table_ubp_4 = pickle.load(ff)


def ubp_4_assign_q_learning(shorter_init):
    env = ubp_4(shorter_init)
    RL = QLearningTable(actions=list(range(4)),e_greedy=1)
    RL.q_table = RL.q_table.append(q_table_ubp_4) 
    observation = env.shorter
    while True:
        action = RL.choose_action(observation)
        shorter_,reward, done = env.step(action)
        observation_ = shorter_
        # RL.learn(str(observation), action, reward, str(observation_))
        observation = observation_
        if done:
            break
    return observation


def RL_UBP_4(st_bp_i,len_ubp):
    shorter_init = st_bp_i +'N'*len_ubp
    ubp_4_seq = ubp_4_assign_q_learning(shorter_init)
    return ubp_4_seq

