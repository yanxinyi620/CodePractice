import re
import argparse
import pandas as pd
import numpy as np
import sys
import os
# input=sys.argv[1]
# out=sys.argv[2]


def tran2bedformat(df):

    df.iloc[:,0] = df.iloc[:,0].replace(['chr','Chr','CHR'], ['','',''], regex=True)
    df.iloc[:,0] = df.iloc[:,0].replace(['23','24'], ['X','Y'])
    df.iloc[:,1] = df.iloc[:,1].astype(int)
    df.iloc[:,2] = df.iloc[:,2].astype(int)
    df.iloc[:,5] = df.iloc[:,5].astype(float)
    df.iloc[:,6] = df.iloc[:,6].astype(int)
    df.iloc[:,7] = df.iloc[:,7].astype(int)
    df.iloc[:,8] = df.iloc[:,8].astype(int)
    df.iloc[:,9] = df.iloc[:,9].astype(float)
    df.iloc[:,10] = df.iloc[:,10].astype(float)
    df.iloc[:,11] = df.iloc[:,11].astype(float)

    return df


def get_mergecnv(cnvlist, gaplen):

    cnvlist = tran2bedformat(cnvlist)
    cnvlist = cnvlist.sort_values(by = [3,0,1],axis = 0,ascending = True)

    cnv_merge = []
    k = 0
    
    if gaplen <= 1:
        for i in range(cnvlist.shape[0]):
            line = cnvlist.iloc[i]
            
            if i>0 and line[0]==cnv_merge[-1][0] and line[3]==cnv_merge[-1][3] and line[4]==cnv_merge[-1][4] and (line[1]-cnv_merge[-1][2]) < (line[2]-line[1]+cnv_merge[-1][2]-cnv_merge[-1][1])*gaplen:

                cnv_merge[-1][2] = max(line[2],cnv_merge[-1][2])
                cnv_merge[-1][6] = cnv_merge[-1][2] - cnv_merge[-1][1]
                cnv_merge[-1][5] = (cnv_merge[-1][5]*cnv_merge[-1][7] + line[5]*line[7])/(cnv_merge[-1][7]+line[7])
                cnv_merge[-1][9] = (cnv_merge[-1][9]*cnv_merge[-1][7] + line[9]*line[7])/(cnv_merge[-1][7]+line[7])
                cnv_merge[-1][10] = (cnv_merge[-1][10]*cnv_merge[-1][7] + line[10]*line[7])/(cnv_merge[-1][7]+line[7])
                cnv_merge[-1][11] = (cnv_merge[-1][11]*cnv_merge[-1][7] + line[11]*line[7])/(cnv_merge[-1][7]+line[7])
                cnv_merge[-1][7] = cnv_merge[-1][7] + line[7]
                k = k+1

            else:
                cnv_merge.append(list(line))

    elif gaplen > 1:
        for i in range(cnvlist.shape[0]):
            line = cnvlist.iloc[i]

            if i>0 and line[0]==cnv_merge[-1][0] and line[3]==cnv_merge[-1][3] and line[4]==cnv_merge[-1][4] and (line[1]-cnv_merge[-1][2]) <= gaplen:
                
                cnv_merge[-1][2] = max(line[2],cnv_merge[-1][2])
                cnv_merge[-1][6] = cnv_merge[-1][2] - cnv_merge[-1][1]
                cnv_merge[-1][5] = (cnv_merge[-1][5]*cnv_merge[-1][7] + line[5]*line[7])/(cnv_merge[-1][7]+line[7])
                cnv_merge[-1][9] = (cnv_merge[-1][9]*cnv_merge[-1][7] + line[9]*line[7])/(cnv_merge[-1][7]+line[7])
                cnv_merge[-1][10] = (cnv_merge[-1][10]*cnv_merge[-1][7] + line[10]*line[7])/(cnv_merge[-1][7]+line[7])
                cnv_merge[-1][11] = (cnv_merge[-1][11]*cnv_merge[-1][7] + line[11]*line[7])/(cnv_merge[-1][7]+line[7])
                cnv_merge[-1][7] = cnv_merge[-1][7] + line[7]
                k = k+1

            else:
                cnv_merge.append(list(line))
        
    cnvmerge = pd.DataFrame(cnv_merge)
    
    if  k!=0:
        print(str(k))
        get_mergecnv(cnvmerge, gaplen)
    
    return cnvmerge


def main(fcnv, gaplen):

    cnvlist = pd.read_table(fcnv, sep='\t', low_memory=False, dtype='str', header=None)
    cnvlist = cnvlist[cnvlist.iloc[:,1]!='start']

    mergecnv = get_mergecnv(cnvlist, gaplen)
    mergecnv.to_csv(os.path.basename(args.cnv)+'.merge', sep='\t', header=False, index=False, mode='w')


if __name__ == '__main__':
    options = argparse.ArgumentParser(description='Result Filter')
    options.add_argument('-c', '--cnv', required=True, help='cnv file')
    options.add_argument('-l', '--gaplen', required=True, help='gap length')
    
    args = options.parse_args()
    main(args.cnv, float(args.gaplen))


