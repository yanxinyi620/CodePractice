import re
import argparse
import pandas as pd
import numpy as np
import sys
import os
# input=sys.argv[1]
# out=sys.argv[2]


def tran2bedformat(df):

    # df = df[df[1]!='start'].copy()
    df.iloc[:,0] = df.iloc[:,0].replace(['chr','Chr','CHR'], ['','',''], regex=True)
    df.iloc[:,0] = df.iloc[:,0].replace(['23','24'], ['X','Y'])
    df.iloc[:,1] = df.iloc[:,1].astype(int)
    df.iloc[:,2] = df.iloc[:,2].astype(int)

    return df


def num2hf(num):

    # trans number to human format
    if num > 1000000:
        num = str(round(num/1000000,1))+'Mb'
    elif num > 1000:
        num = str(int(num/1000))+'Kb'
    else:
        num = str(num)+'Bp'

    return num


def get_overlap(df1, df2, cutoff, result_num):
    
    df1 = tran2bedformat(df1)
    df2 = tran2bedformat(df2)
    res = result_num

    df_overlap = []

    for i in range(df1.shape[0]):
        line = df1.iloc[i]
        linedf2 = df2[(df2[0]==line[0]) & (df2[1]<line[2]) & (df2[2]>line[1])]

        if len(linedf2) > 0:
            cdf2 = []
            for j in range(len(linedf2)):
                overlap = min(linedf2.iloc[j][2], line[2]) - max(linedf2.iloc[j][1], line[1])
                lendf2 = linedf2.iloc[j][2] - linedf2.iloc[j][1]
                prop = round(overlap/lendf2, 2)

                if cutoff <= 1 and prop >= cutoff:
                    lendf2 = num2hf(lendf2)
                    df2tmp = df2.iloc[j][res]+'|'+str(prop)+'/'+lendf2
                    cdf2.append(df2tmp)

                elif cutoff > 1 and overlap >= cutoff:
                    lendf2 = num2hf(lendf2)
                    overlap = num2hf(overlap)
                    df2tmp = df2.iloc[j][res]+'|'+overlap+'/'+lendf2
                    cdf2.append(df2tmp)

                else:
                    cdf2.append('<'+str(cutoff))

            df_overlap.append(list(line)+[';'.join(cdf2)])
        else:
            df_overlap.append(list(line)+['NA'])

    dfoverlap = pd.DataFrame(df_overlap)
    return dfoverlap


def main(fcnv, fgene, fdisease, prob, length):

    cnvlist = pd.read_table(fcnv, sep='\t', low_memory=False, dtype='str', header=None)
    cnvlist = cnvlist[cnvlist.iloc[:,1]!='start']

    genelist = pd.read_table(fgene, sep='\t', low_memory=False, dtype='str', header=None)
    genelist = genelist[genelist.iloc[:,1]!='start']

    diseaselist = pd.read_table(fdisease, sep='\t', low_memory=False, dtype='str', header=None)
    diseaselist = diseaselist[diseaselist.iloc[:,1]!='start']

    cnvdisease = get_overlap(cnvlist, diseaselist, length, 5)
    cnvdisease.to_csv(os.path.basename(args.cnv)+'.disease.txt', sep='\t', header=False, index=False, mode='w')

    cnvgene = get_overlap(cnvdisease, genelist, prob, 3)
    cnvgene.to_csv(os.path.basename(args.cnv)+'.disease.gene.txt', sep='\t', header=False, index=False, mode='w')


if __name__ == '__main__':
    options = argparse.ArgumentParser(description='Result Filter')
    options.add_argument('-c', '--cnv', required=True, help='cnv file')
    options.add_argument('-g', '--gene', required=True, help='gene file')
    options.add_argument('-d', '--disease', required=True, help='disease file')
    options.add_argument('-p', '--prob', default=0.5, help='gene overlap length or probability cutoff')
    options.add_argument('-l', '--len', default=500000, help='disease overlap length or probability cutoff')
    
    args = options.parse_args()
    main(args.cnv, args.gene, args.disease, float(args.prob), float(args.len))


