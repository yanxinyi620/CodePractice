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


def get_gene(cnvlist, genelist, overlap_prop):

    cnvlist = tran2bedformat(cnvlist)
    genelist = tran2bedformat(genelist)

    cnv_gene = []
    for i in range(cnvlist.shape[0]):
        line = cnvlist.iloc[i]
        linegene = genelist[(genelist[0]==line[0]) & (genelist[1]<line[2]) & (genelist[2]>line[1])]
        if len(linegene) > 0:
            cgene = []
            for j in range(len(linegene)):
                overlap = min(linegene.iloc[j][2], line[2]) - max(linegene.iloc[j][1], line[1])
                prop = round(overlap/(linegene.iloc[j][2] - linegene.iloc[j][1]),2) 
                if  prop >= overlap_prop:
                    cgenetmp = linegene.iloc[j][3]+'|'+str(prop)
                    cgene.append(cgenetmp)
                else:
                    cgene.append('<'+str(overlap_prop))

            cnv_gene.append(list(line)+[';'.join(cgene)])
        else:
            cnv_gene.append(list(line)+['NA'])

    cnvgene = pd.DataFrame(cnv_gene)
    return cnvgene


def get_disease(cnvlist, diseaselist, overlap_len):

    cnvlist = tran2bedformat(cnvlist)
    diseaselist = tran2bedformat(diseaselist)

    cnv_disease = []
    for i in range(cnvlist.shape[0]):
        line = cnvlist.iloc[i]
        linedisease = diseaselist[(diseaselist[0]==line[0]) & (diseaselist[3]==line[4]) & (diseaselist[1]<line[2]) & (diseaselist[2]>line[1])]
        if len(linedisease) > 0:
            cdisease = []
            for j in range(len(linedisease)):
                overlap = min(linedisease.iloc[j][2], line[2]) - max(linedisease.iloc[j][1], line[1])
                if  overlap >= overlap_len:
                    if overlap > 1000000:
                        overlap = str(round(overlap/1000000,1))+'Mb'
                    else:
                        overlap = str(round(overlap/1000,0))+'Kb'

                    cdiseasetmp = linedisease.iloc[j][5]+'|'+overlap+'/'+linedisease.iloc[j][4]
                    
                    cdisease.append(cdiseasetmp)
                else:
                    cdisease.append('<'+str(overlap_len))

            cnv_disease.append(list(line)+[';'.join(cdisease)])
        else:
            cnv_disease.append(list(line)+['NA'])

    cnvdisease = pd.DataFrame(cnv_disease)
    return cnvdisease


def main(fcnv, fgene, fdisease, prob, length):

    cnvlist = pd.read_table(fcnv, sep='\t', low_memory=False, dtype='str', header=None)
    cnvlist = cnvlist[cnvlist.iloc[:,1]!='start']

    genelist = pd.read_table(fgene, sep='\t', low_memory=False, dtype='str', header=None)
    genelist = genelist[genelist.iloc[:,1]!='start']

    diseaselist = pd.read_table(fdisease, sep='\t', low_memory=False, dtype='str', header=None)
    diseaselist = diseaselist[diseaselist.iloc[:,1]!='start']

    cnvdisease = get_disease(cnvlist, diseaselist, length)
    cnvdisease.to_csv(os.path.basename(args.cnv)+'.disease.txt', sep='\t', header=False, index=False, mode='w')

    cnvgene = get_gene(cnvdisease, genelist, prob)
    cnvgene.to_csv(os.path.basename(args.cnv)+'.disease.gene.txt', sep='\t', header=False, index=False, mode='w')


if __name__ == '__main__':
    options = argparse.ArgumentParser(description='Result Filter')
    options.add_argument('-c', '--cnv', required=True, help='cnv file')
    options.add_argument('-g', '--gene', required=True, help='gene file')
    options.add_argument('-d', '--disease', required=True, help='disease file')
    options.add_argument('-p', '--prob', default=0.5, help='probability cutoff')
    options.add_argument('-n', '--len', default=500000, help='cnv length cutoff')
    
    args = options.parse_args()
    main(args.cnv, args.gene, args.disease, float(args.prob), int(args.len))


