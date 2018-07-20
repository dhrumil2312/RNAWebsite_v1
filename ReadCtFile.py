import re
import rna_toolkit

def read_ct_files(file_name):

    reg_str = r'^\s*?(\d{1,5})\s*?([AUGCaugc])\s*?(\d{1,5})\s*?(\d{1,5})\s*?(\d{1,5})\s*?(\d{1,5})'
    mod = re.compile(reg_str)
    seq = ''
    bp = []
    f = open(file_name)
    file_txt = f.readlines()
    f.close()
    line_i = 0
    while file_txt[line_i][0] == '#':
        line_i += 1
    for line_txt in file_txt[line_i+1:]:
        items = mod.findall(line_txt)
        seq += items[0][1].upper()
        bp.append(int(items[0][4]))
    if rna_toolkit.is_pseudoknotted(bp) == 0:
        dp = rna_toolkit.bp_to_dp(bp)

    else:
        dp = ''
        print('pseudoknotted')
    return seq,dp