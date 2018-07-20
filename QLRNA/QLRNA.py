import numpy as np
import os
from QLRNA.rna_toolkit import *


from QLRNA.Stacking_Assignment import RL_Stacking
from QLRNA.UBP_type_1_Assignment import RL_UBP_1
from QLRNA.UBP_type_2_Assignment import RL_UBP_2
from QLRNA.UBP_type_3_Assignment import RL_UBP_3
from QLRNA.UBP_type_4_Assignment import RL_UBP_4
from QLRNA.UBP_type_5_Assignment import RL_UBP_5
from QLRNA.UBP_type_6_Assignment import RL_UBP_6

from QLRNA import  Extract_UBP
import random


def stacking_split_stop(stacking_start_list,stacking_end_list):
    for ii in range(len(stacking_start_list)):
        stacking_shorter_start = stacking_start_list[ii]
        stacking_shorter_end = stacking_end_list[ii]
        if stacking_shorter_end - stacking_shorter_start > 5:
            return True
    return False


def extract_stacking(check_array):
    stacking_start_list = []
    stacking_end_list = []
    stacking_num_list = set(check_array[np.where((check_array > 0))])
    for i in stacking_num_list:
        set_together = np.where(check_array == i)[0]
        j = int(len(set_together)/2)
        stacking_start_list.append(min(set_together[:j]))
        stacking_end_list.append(max(set_together[:j]))
    return stacking_start_list,stacking_end_list


def qlrna(dp_temp):

    # A:1 C:2 G:3 U:4 To_Be_Assigned:0
    # BP TYPE: 1:AU 2:UA 3:CG 4:GC 5:GU 6:UG
    # BP_Type = {1:[1,4],2:[4,1],3:[2,3],4:[3,2],5:[3,4],6:[4,3]}

    nt_dict = {'A':1,'C':2,'G':3,'U':4}
    bp_list = [[1,4],[4,1],[2,3],[3,2],[3,4],[4,3]]
    bp_dict = {'14':'1','41':'2','23':'3','32':'4','34':'5','43':'6'}


    if '\n' == dp_temp[-1]:
        dp = dp_temp[:-1]
    else:
        dp = dp_temp
    print(dp)

    rna_length = len(dp)
    seq_array = np.zeros([rna_length], dtype=int)

    bp_raw = dp_to_bp(dp)
    bp_array = np.array(bp_raw) - 1            # 0 is first position. -1 is unpaired.
    check_array =structure_analysis(bp_raw)
    stacking_start_list, stacking_end_list = extract_stacking(check_array)

    bp_array_temp = bp_array

############### stacking RL

    while stacking_split_stop(stacking_start_list, stacking_end_list):
        np_stacking_len = np.array(stacking_end_list) - np.array(stacking_start_list)
        temp_i = np.min(np.argwhere(np_stacking_len > 5))
        stacking_start_list.append(stacking_start_list[temp_i] + 3)
        stacking_end_list.append(stacking_end_list[temp_i])
        stacking_end_list[temp_i] = stacking_start_list[temp_i] + 3

    for ii in range(len(stacking_start_list)):
        stacking_shorter_start = stacking_start_list[ii]
        stacking_shorter_end = stacking_end_list[ii]
        stacking_longer_start = bp_array_temp[stacking_shorter_end]
        stacking_longer_end = bp_array_temp[stacking_shorter_start]

        if seq_array[stacking_shorter_start] == 0:
            ps_seed = random.randint(0, 3)
            seq_array[stacking_shorter_start] = bp_list[ps_seed][0]
            seq_array[stacking_longer_end] = bp_list[ps_seed][1]
        if seq_array[stacking_shorter_end] == 0:
            ps_seed = random.randint(0, 3)
            seq_array[stacking_shorter_end] = bp_list[ps_seed][0]
            seq_array[stacking_longer_start] = bp_list[ps_seed][1]
        if stacking_shorter_end - stacking_shorter_start > 1:
            stacking_shorter_assign,stacking_longer_assign = RL_Stacking(seq_array[stacking_shorter_start],seq_array[stacking_shorter_end],seq_array[stacking_longer_start],seq_array[stacking_longer_end],stacking_shorter_end-stacking_shorter_start-1,stacking_longer_end-stacking_longer_start-1)
            for i in range(stacking_shorter_end-stacking_shorter_start+1):
                seq_array[stacking_shorter_start + i] = nt_dict[stacking_shorter_assign[i]]
            for i in range(stacking_longer_end-stacking_longer_start+1):
                seq_array[stacking_longer_start + i] = nt_dict[stacking_longer_assign[i]]

    UBP_5_num = Extract_UBP.type_5_ubp(dp)
    UBP_6_num = Extract_UBP.type_6_ubp(dp)

    if UBP_5_num > 0:
        st_i = UBP_5_num
        if st_i > 9:
            seq_array = np.zeros(len(bp_array))
            print("Failed")
            return ''
        else:
            if seq_array[st_i] == 0:
                ps_seed = random.randint(0, 3)
                seq_array[st_i] = bp_list[ps_seed][0]
                seq_array[bp_array[st_i]] = bp_list[ps_seed][1]
            st_bp_num = bp_dict[str(seq_array[st_i]) + str(seq_array[bp_array[st_i]])]
            ubp_5_assign_temp = RL_UBP_5(st_bp_num, st_i)
            ubp_5_assign = ubp_5_assign_temp[1:]
            for assign_i in range(len(ubp_5_assign)):
                seq_array[assign_i] = nt_dict[ubp_5_assign[assign_i]]

    if UBP_6_num > 0:
        rna_length = len(dp)
        st_i = rna_length - UBP_6_num
        if UBP_6_num > 9:
            seq_array = np.zeros(len(bp_array))
            print("Failed")
            return ''
        else:
            if seq_array[st_i] == 0:
                ps_seed = random.randint(0, 3)
                seq_array[st_i] = bp_list[ps_seed][0]
                seq_array[bp_array[st_i]] = bp_list[ps_seed][1]
            st_bp_num = bp_dict[str(seq_array[st_i]) + str(seq_array[bp_array[st_i]])]
            ubp_6_assign_temp = RL_UBP_6(st_bp_num, UBP_6_num - 1)
            ubp_6_assign = ubp_6_assign_temp[1:]
            for assign_i in range(len(ubp_6_assign)):
                seq_array[st_i + assign_i + 1] = nt_dict[ubp_6_assign[assign_i]]

    UBP_1_list = Extract_UBP.type_1_ubp(dp)
    UBP_2_list = Extract_UBP.type_2_ubp(dp)
    UBP_3_list = Extract_UBP.type_3_ubp(dp)
    UBP_4_list = Extract_UBP.type_4_ubp(dp)

    ####### UBP_1 RL
    for ubp_info_i in UBP_1_list:
        st_i = ubp_info_i[0]
        ed_i = ubp_info_i[1]

        if ed_i - st_i > 9:
            seq_array = np.zeros(len(bp_array))
            print("Failed")
            return ''
        else:

            if seq_array[st_i] == 0:
                ps_seed = random.randint(0, 3)
                seq_array[st_i] = bp_list[ps_seed][0]
                seq_array[bp_array[st_i]] = bp_list[ps_seed][1]
            if seq_array[ed_i] == 0:
                ps_seed = random.randint(0, 3)
                seq_array[ed_i] = bp_list[ps_seed][0]
                seq_array[bp_array[ed_i]] = bp_list[ps_seed][1]


            st_bp_num = bp_dict[str(seq_array[st_i])+str(seq_array[bp_array[st_i]])]
            ed_bp_num = bp_dict[str(seq_array[ed_i])+str(seq_array[bp_array[ed_i]])]

            ubp_1_assign_temp = RL_UBP_1(st_bp_num, ed_bp_num, ed_i - st_i - 1)
            ubp_1_assign = ubp_1_assign_temp[1:-1]
            for assign_i in range(len(ubp_1_assign)):
                seq_array[st_i + assign_i + 1] = nt_dict[ubp_1_assign[assign_i]]

    ####### UBP_2 RL
    for ubp_info_i in UBP_2_list:
        st_i = ubp_info_i[0]
        ed_i = ubp_info_i[1]

        if ed_i - st_i > 9:
            seq_array = np.zeros(len(bp_array))
            print("Failed")
            return ''
        else:

            if seq_array[st_i] == 0:
                ps_seed = random.randint(0, 3)
                seq_array[st_i] = bp_list[ps_seed][0]
                seq_array[bp_array[st_i]] = bp_list[ps_seed][1]
            if seq_array[ed_i] == 0:
                ps_seed = random.randint(0, 3)
                seq_array[ed_i] = bp_list[ps_seed][0]
                seq_array[bp_array[ed_i]] = bp_list[ps_seed][1]


            st_bp_num = bp_dict[str(seq_array[st_i])+str(seq_array[bp_array[st_i]])]
            ed_bp_num = bp_dict[str(seq_array[ed_i])+str(seq_array[bp_array[ed_i]])]

            ubp_2_assign_temp = RL_UBP_2(st_bp_num, ed_bp_num, ed_i - st_i - 1)
            ubp_2_assign = ubp_2_assign_temp[1:-1]
            for assign_i in range(len(ubp_2_assign)):
                seq_array[st_i + assign_i + 1] = nt_dict[ubp_2_assign[assign_i]]

    
    ####### UBP_3 RL
    for ubp_info_i in UBP_3_list:
        st_i = ubp_info_i[0]
        ed_i = ubp_info_i[1]

        if ed_i - st_i > 9:
            seq_array = np.zeros(len(bp_array))
            print("Failed")
            return ''
        else:

            if seq_array[st_i] == 0:
                ps_seed = random.randint(0, 3)
                seq_array[st_i] = bp_list[ps_seed][0]
                seq_array[bp_array[st_i]] = bp_list[ps_seed][1]
            if seq_array[ed_i] == 0:
                ps_seed = random.randint(0, 3)
                seq_array[ed_i] = bp_list[ps_seed][0]
                seq_array[bp_array[ed_i]] = bp_list[ps_seed][1]

            st_bp_num = bp_dict[str(seq_array[st_i])+str(seq_array[bp_array[st_i]])]
            ed_bp_num = bp_dict[str(seq_array[ed_i])+str(seq_array[bp_array[ed_i]])]


            ubp_3_assign_temp = RL_UBP_3(st_bp_num, ed_bp_num, ed_i - st_i - 1)
            ubp_3_assign = ubp_3_assign_temp[1:-1]
            for assign_i in range(len(ubp_3_assign)):
                seq_array[st_i + assign_i + 1] = nt_dict[ubp_3_assign[assign_i]]


    ####### UBP_4 RL
    for ubp_info_i in UBP_4_list:
        st_i = ubp_info_i[0]
        ed_i = ubp_info_i[1]

        if ed_i - st_i > 9:
            seq_array = np.zeros(len(bp_array))
            print("Failed")
            return ''
        else:

            if seq_array[st_i] == 0:
                ps_seed = random.randint(0, 3)
                seq_array[st_i] = bp_list[ps_seed][0]
                seq_array[bp_array[st_i]] = bp_list[ps_seed][1]


            st_bp_num = bp_dict[str(seq_array[st_i])+str(seq_array[bp_array[st_i]])]

            ubp_4_assign_temp = RL_UBP_4(st_bp_num, ed_i - st_i - 1)
            ubp_4_assign = ubp_4_assign_temp[1:]
            for assign_i in range(len(ubp_4_assign)):
                seq_array[st_i + assign_i + 1] = nt_dict[ubp_4_assign[assign_i]]



    seq = ''
    for i in range(len(seq_array)):
        if seq_array[i] == 0:
            seq += 'N'
        elif seq_array[i] == 1:
            seq += 'A'
        elif seq_array[i] == 2:
            seq += 'C'
        elif seq_array[i] == 3:
            seq += 'G'
        elif seq_array[i] == 4:
            seq += 'U'

    return seq


 
