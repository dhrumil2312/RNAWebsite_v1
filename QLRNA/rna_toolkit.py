import numpy as np
import math



def is_pseudoknotted(bp):
    bp_paired_list = []
    for i in range(len(bp)):
        if i < bp[i]:
            bp_paired_list.append([i,bp[i]-1])
    is_pseudoknotted_idx = 0
    for ii in range(len(bp_paired_list)):
        test_paired = bp_paired_list[ii]
        for jj in range(len(bp_paired_list)):
            if test_paired[0] < bp_paired_list[jj][0] and test_paired[1] > bp_paired_list[jj][0] and test_paired[1] < bp_paired_list[jj][1]:
                is_pseudoknotted_idx += 1
    return is_pseudoknotted_idx

def bp_to_dp(bp):
    dp = ''
    for i in range(len(bp)):
        if bp[i] == 0:
            dp += '.'
        elif i < bp[i]:
            dp += '('
        else:
            dp += ')'
    return dp


def dp_to_bp(dp):
    a_list = []
    bp_array = np.zeros(len(dp),dtype = int)
    for i in range(len(dp)):
        if dp[i] == "(":
            a_list.append(i)
        if dp[i] == ")":
            bp_array[i] = a_list[-1] + 1
            bp_array[a_list[-1]] = i + 1
            a_list.pop()
    return bp_array



def entropy(seq, mm):
    seqDict = {}
    n = len(seq)
    for i in range(n-mm+1):
        if seq[i:i+mm] in seqDict:
            seqDict[seq[i:i+mm]] += 1
        else:
            seqDict[seq[i:i+mm]] = 1
    nn = float(n-mm+1)
    x = 0
    for i in seqDict:
        prob = seqDict[i]/nn
        seqDict[i] = - prob * math.log(prob, 2)
        x += seqDict[i]
    return x


def entropy_max(nn, ent_n):
    entropy_max_value = 0
    if nn <= ent_n:
        entropy_max_value = 0
    elif nn - ent_n + 1 <= 4**ent_n:
            prob = 1/float(nn - ent_n + 1)
            for i in range(nn - ent_n + 1):
                entropy_max_value +=  (-(prob) * math.log(prob, 2))
    elif nn - ent_n + 1 > 4**ent_n:
        a = (nn - ent_n + 1) / (4**ent_n)
        b = (nn - ent_n + 1) % (4**ent_n)
        entropy_max_value = (-b) * (a+1)/float(nn - ent_n + 1) * math.log((a+1)/float(nn - ent_n + 1), 2) - ((4**ent_n-b) * a / float(nn - ent_n + 1) * math.log(a/float(nn - ent_n + 1), 2))
    return entropy_max_value


def structure_analysis(bp_array):
    bp_array_temp = bp_array - 1
    dp = bp_to_dp(bp_array)
    str_len = len(bp_array)
    check_array = np.zeros(str_len,dtype = int)
    idx_interloop = 0
    idx_bulge = 0
    for j in range(str_len):
        if check_array[j] == 0:
            if bp_array[j] > 0:
                check_array[j] = 1 # 1: base-paired
            elif bp_array[j] == 0 and np.sum(bp_array[:j+1]) == 0:
                check_array[j] = -1 # -1: start_ubp
            elif bp_array[j] == 0 and np.sum(bp_array[j:]) == 0:
                check_array[j:] = -2 # -2: end_ubp
            elif bp_array[j] == 0 and dp[:j].count("(") == dp[:j].count(")"):
                check_array[j] = -3 # -3: between two branches
    for j in range(str_len):
        if check_array[j] == 0:
            n_forward = 1
            n_backward = 1
            while dp[j + n_forward] == ".":
                n_forward += 1
            while dp[j - n_backward] == ".":
                n_backward += 1
            symbol_forward = dp[j + n_forward]
            symbol_backward = dp[j - n_backward]
            if symbol_backward == "(" and symbol_forward == ")":
                check_array[j - n_backward+1:j + n_forward] = -4 #-4:hairpin
            elif symbol_backward == "(" and symbol_forward == "(":
                down_start_pos = bp_array_temp[j + n_forward]
                n_down_len = 1
                while dp[down_start_pos + n_down_len] != ")":
                    n_down_len += 1
                if n_down_len == 1:
                    idx_bulge += 1
                    check_array[j - n_backward+1:j + n_forward] = -1000-idx_bulge
                elif "(" in dp[down_start_pos:down_start_pos + n_down_len]:
                    check_array[j - n_backward+1:j + n_forward] = -3
                else:
                    idx_interloop += 1
                    check_array[j - n_backward+1:j + n_forward] = -10-idx_interloop
                    check_array[down_start_pos+1:down_start_pos + n_down_len] = -10-idx_interloop
            elif symbol_backward == ")" and symbol_forward == ")":
                if bp_array_temp[j + n_forward] + 1 ==  bp_array_temp[j - n_backward]:
                    idx_bulge += 1
                    check_array[j - n_backward+1:j + n_forward] = -1000-idx_bulge
                else:
                    check_array[j - n_backward+1:j + n_forward] = -3
            else:
                check_array[j - n_backward+1:j + n_forward] = -3
    idx_stacking = 0
    for j in range(str_len - 1):
        if dp[j] == "(":
            if check_array[j] == 1 and check_array[j + 1] != 1:
                check_array[j] += idx_stacking
                check_array[bp_array_temp[j]] += idx_stacking
                idx_stacking += 1
            elif check_array[j] == 1 and check_array[j + 1] == 1 and bp_array_temp[j] != bp_array_temp[j + 1] + 1:
                check_array[j] += idx_stacking
                check_array[bp_array_temp[j]] += idx_stacking
                idx_stacking += 1
            elif check_array[j] == 1 and check_array[j + 1] == 1 and bp_array_temp[j] == bp_array_temp[j + 1] + 1:
                check_array[j] += idx_stacking
                check_array[bp_array_temp[j]] += idx_stacking

    return check_array