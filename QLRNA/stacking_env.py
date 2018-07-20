import pandas as pd
import numpy as np
df = pd.read_csv("QLRNA/bp.csv",header = 0)
EXISTING_SHORTER = df['shorter']
EXISTING_LONGER = df['longer']
EXISTING_PAIR = []
for i in range(len(EXISTING_SHORTER)):
        EXISTING_PAIR.append([EXISTING_SHORTER[i],EXISTING_LONGER[i]])


class Stacking(object):

    def __init__(self,shorter,longer):
        self.action_space = [['A','U'],['U','A'],['C','G'],['G','C'],['G','U'],['U','G']]
        self.n_actions = len(self.action_space)
        self.shorter = shorter
        self.longer = longer
        # interloop_candi = []
        # for i in range(len(EXISTING_SHORTER)):
        #     if len(EXISTING_SHORTER[i]) == len(shorter) and len(EXISTING_LONGER[i]) == len(longer):
        #         interloop_candi.append([EXISTING_SHORTER[i],EXISTING_LONGER[i]])
        # self.interloop_candi = interloop_candi

    def step(self,action):
        shorter = self.shorter
        longer = self.longer
        ps_candidate = shorter.find("N")
        if action == 0: # Assign A
            shorter_ = shorter[:ps_candidate] + "A" + shorter[ps_candidate+1:]
            longer_ = longer[:ps_candidate] + "U" + longer[ps_candidate+1:]
        elif action == 1: # Assign C
            shorter_ = shorter[:ps_candidate] + "U" + shorter[ps_candidate+1:]
            longer_ = longer[:ps_candidate] + "A" + longer[ps_candidate+1:]
        elif action == 2: #  Assign G
            shorter_ = shorter[:ps_candidate] + "C" + shorter[ps_candidate+1:]
            longer_ = longer[:ps_candidate] + "G" + longer[ps_candidate+1:]
        elif action == 3:   # Assign U
            shorter_ = shorter[:ps_candidate] + "G" + shorter[ps_candidate+1:]
            longer_ = longer[:ps_candidate] + "C" + longer[ps_candidate+1:]
        elif action == 4:
            shorter_ = shorter[:ps_candidate] + "G" + shorter[ps_candidate+1:]
            longer_ = longer[:ps_candidate] + "U" + longer[ps_candidate+1:]
        elif action == 5:
            shorter_ = shorter[:ps_candidate] + "U" + shorter[ps_candidate+1:]
            longer_ = longer[:ps_candidate] + "G" + longer[ps_candidate+1:]

        self.shorter = shorter_
        self.longer = longer_
        reward = 0
        if [shorter_,longer_] in EXISTING_PAIR or [longer_,shorter_] in EXISTING_PAIR:
            reward += max(np.median(df['foldability'][df['shorter'] == shorter_]), np.median(df['foldability'][df['shorter'] == longer_]))
            # print(reward)
        if shorter_.count("N") == 0:
            done = True
        else:
            done = False
        return shorter_,longer_, reward, done

    def reset(self,shorter,longer):
        self.shorter = shorter
        self.longer = longer
