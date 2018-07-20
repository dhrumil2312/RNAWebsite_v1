import pandas as pd
import numpy as np



def type_1_ubp(dp):
    ubp_info = []
    candi_pos_list = []
    for i in range(len(dp)):
        if dp[i] == '(':
            candi_pos_list.append(i)
    if len(candi_pos_list) <= 1:
        return ubp_info
    else:
        for i in range(len(candi_pos_list) - 1):
            st_i = candi_pos_list[i]
            ed_i = candi_pos_list[i+1]
            if ed_i - st_i > 1 and ')' not in dp[st_i+1:ed_i]:
                ubp_info.append([st_i,ed_i])
        return ubp_info


def type_2_ubp(dp):
    ubp_info = []
    candi_pos_list = []
    for i in range(len(dp)):
        if dp[i] == ')':
            candi_pos_list.append(i)
    if len(candi_pos_list) <= 1:
        return ubp_info
    else:
        for i in range(len(candi_pos_list) - 1):
            st_i = candi_pos_list[i]
            ed_i = candi_pos_list[i+1]
            if ed_i - st_i > 1 and '(' not in dp[st_i+1:ed_i]:
                ubp_info.append([st_i,ed_i])
        return ubp_info

def type_3_ubp(dp):
    ubp_info = []
    i = 0
    st_i = len(dp)
    while i < len(dp):
        if dp[i] == ")":
            st_i = i
        elif dp[i] == "(" and i > st_i:
            ed_i = i
            if ed_i > st_i + 1:
                ubp_info.append([st_i,ed_i])
            st_i = len(dp)
        i += 1
    return ubp_info

def type_4_ubp(dp):
    ubp_info = []
    i = 0
    st_i = len(dp)
    while i < len(dp):
        if dp[i] == "(":
            st_i = i
        elif dp[i] == ")" and i > st_i:
            ed_i = i
            if ed_i > st_i + 1:
                ubp_info.append([st_i,ed_i])
            st_i = len(dp)
        i += 1
    return ubp_info

def type_5_ubp(dp):
    if dp[0] != '.':
        return 0
    else:
        i = 0
        while dp[i] != "(":
            i += 1
        return i


def type_6_ubp(dp):
    if dp[-1] != '.':
        return 0
    else:
        i = 1
        while dp[-i] != ")":
            i += 1
        return i
