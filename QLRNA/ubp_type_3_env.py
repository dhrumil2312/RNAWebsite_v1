import pandas as pd
import numpy as np
df = pd.read_csv("QLRNA/ubp_type_3.csv",header = 0)
EXISTING_SHORTER = df['seq']
EXISTING_ST = df['st_bp']
EXISTING_ED = df['ed_bp']
EXISTING_PAIR = []
for i in range(len(EXISTING_SHORTER)):
        EXISTING_PAIR.append(str(EXISTING_ST[i])+EXISTING_SHORTER[i]+str(EXISTING_ED[i]))
df['existing_seg'] = EXISTING_PAIR

class ubp_3(object):

    def __init__(self,shorter):
        self.action_space = ['A','C','G','U']
        self.n_actions = len(self.action_space)
        self.shorter = shorter


    def step(self,action):
        shorter = self.shorter
        ps_candidate = shorter.find("N")
        if action == 0: # Assign A
            shorter_ = shorter[:ps_candidate] + "A" + shorter[ps_candidate+1:]
        elif action == 1: # Assign C
            shorter_ = shorter[:ps_candidate] + "C" + shorter[ps_candidate+1:]
        elif action == 2: #  Assign G
            shorter_ = shorter[:ps_candidate] + "G" + shorter[ps_candidate+1:]
        elif action == 3:   # Assign U
            shorter_ = shorter[:ps_candidate] + "U" + shorter[ps_candidate+1:]


        self.shorter = shorter_
        reward = 0
        if shorter_ in EXISTING_PAIR:
            reward += np.median(df['foldability'][df['existing_seg'] == shorter_])
            # print(reward)
        if shorter_.count("N") == 0:
            done = True
        else:
            done = False
        return shorter_, reward, done

    def reset(self,shorter):
        self.shorter = shorter
