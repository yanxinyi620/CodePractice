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

    return df


def get_arraycnv(cnvlist, arraylist):

    cnvlist = tran2bedformat(cnvlist)
    arraylist = tran2bedformat(arraylist)

    cnv_array = []
    for i in range(cnvlist.shape[0]):
        line = cnvlist.iloc[i]
        linearray = arraylist[(arraylist[0]==line[0]) & (arraylist[3]==line[3]) & (arraylist[4]==line[4]) & (arraylist[1]<line[2]) & (arraylist[2]>line[1])]
        if len(linearray) > 0:
            carray = []
            for j in range(len(linearray)):
                overlap = min(linearray.iloc[j][2], line[2]) - max(linearray.iloc[j][1], line[1])
                cnvlen = linearray.iloc[j][2] - linearray.iloc[j][1]
                
                if overlap > 1000000:
                    overlap = str(round(overlap/1000000,1))+'Mb'
                else:
                    overlap = str(round(overlap/1000,0))+'Kb'
                
                if cnvlen > 1000000:
                    cnvlen = str(round(cnvlen/1000000,1))+'Mb'
                else:
                    cnvlen = str(round(cnvlen/1000,0))+'Kb'

                carraytmp = overlap+'/'+cnvlen
                carray.append(carraytmp)

            cnv_array.append(list(line)+[';'.join(carray)])
        else:
            cnv_array.append(list(line)+['NA'])
        
        #print('\t'.join(cnv_array[-1]))

    cnvarray = pd.DataFrame(cnv_array)
    return cnvarray


def main(fcnv, farray):

    arraylist = pd.read_table(farray, sep='\t', low_memory=False, dtype='str', header=None)
    arraylist = arraylist[arraylist.iloc[:,1]!='start']

    cnvlist = pd.read_table(fcnv, sep='\t', low_memory=False, dtype='str', header=None)
    cnvlist = cnvlist[cnvlist.iloc[:,1]!='start']

    cnvarray = get_arraycnv(cnvlist, arraylist)
    cnvarray.to_csv(os.path.basename(args.cnv)+'.array.txt', sep='\t', header=False, index=False, mode='w')



if __name__ == '__main__':
    options = argparse.ArgumentParser(description='Result Filter')
    options.add_argument('-c', '--cnv', required=True, help='cnv file')
    options.add_argument('-a', '--array', required=True, help='array bed file')
    
    args = options.parse_args()
    main(args.cnv, args.array)


