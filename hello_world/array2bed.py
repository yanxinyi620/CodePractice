import re
import argparse
import pandas as pd
import numpy as np
import sys
input=sys.argv[1]
# out=sys.argv[2]


def cnvarray2bed(cnvarray):
    
    header = ['chr', 'start', 'end', 'loc', 'copyratio', 'sample', 'sex', 'type', 'runid']
    print('\t'.join(header))
    cnv_list = []
    cnvarray['Array_result']=cnvarray['Array_result'].replace([r'\)x', '（', '）', '，'],[')*', '(', ')', ','],regex=True)

    for i in range(cnvarray.shape[0]):
        string = cnvarray.iloc[i].iloc[0]
        sex = cnvarray.iloc[i].iloc[1]
        sample = cnvarray.index[i]
        runid = cnvarray.iloc[i].iloc[2]
        cnv = re.findall(r'(X|Y|\d+)([p|q]\w+\.?\w*\.?\w*)\((\d+,?\d*,?\d*,?\d*)-(\d+,?\d*,?\d*,?\d*)\)\*(\d-?\d*)',string)
        for j in range(len(cnv)):
            line = [cnv[j][0],cnv[j][2],cnv[j][3],cnv[j][1],cnv[j][4]]
            line[1] = line[1].replace(',', '')
            line[2] = line[2].replace(',', '')

            if '-' in line[4]:
                a = re.findall(r'\d+', line[4])
                line[4] = np.mean(np.array(a).astype(float))
            else:
                line[4] = int(line[4])

            if line[0] in ['23', '24', 'X', 'Y', 23, 24] and sex in ['Male', 'male']:
                if line[4]>1:
                    cnvtype = 'dup'
                elif line[4]<1:
                    cnvtype = 'del'
                else:
                    cnvtype = 'other'
            elif line[0] in ['24', 'Y', 24] and sex in ['Female', 'female']:
                cnvtype = 'error'
            else:
                if line[4]>2:
                    cnvtype = 'dup'
                elif line[4]<2:
                    cnvtype = 'del'
                else:
                    cnvtype = 'other'

            line[4] = str(line[4])
            cnv_list.append(line + [sample,sex,cnvtype,runid])
            print('\t'.join(line[0:3])+'\t'+sample+'\t'+cnvtype+'\t'+sex+'\t'+runid+'\t'+line[3]+'\t'+line[4])
    
    cnvlist = pd.DataFrame(cnv_list)
    cnvlist.columns = header

    return cnvlist


cnvarray=pd.read_table(input, sep='\t', low_memory=False, dtype='str', index_col=0)
cnvarray2bed(cnvarray)



