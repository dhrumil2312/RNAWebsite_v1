from QLRNA.ubp_type_6_env import ubp_6
from QLRNA.RL_brain import QLearningTable
import pickle


with open('QLRNA/ubp_type_6_q_table.pickle', 'rb') as ff:
    q_table_ubp_6 = pickle.load(ff)


def ubp_6_assign_q_learning(shorter_init):
    env = ubp_6(shorter_init)
    RL = QLearningTable(actions=list(range(4)),e_greedy=1)
    RL.q_table = RL.q_table.append(q_table_ubp_6)
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


def RL_UBP_6(st_bp_i,len_ubp):
    shorter_init = st_bp_i +'N'*len_ubp
    ubp_6_seq = ubp_6_assign_q_learning(shorter_init)
    return ubp_6_seq

