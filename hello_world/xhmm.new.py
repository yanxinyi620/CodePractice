#!/usr/bin/env python3

import os
import argparse
import pandas as pd
import numpy as np
from collections import namedtuple

CNV = namedtuple('CNV', ('chrom', 'start', 'end', 'name', 'type', 'score', 'length', 'count', 'number'))


def main(runID, prob_cutoff, cnv_len_cutoff):
    df_del = pd.read_table(runID+'.posteriors.DEL.txt' , sep='\t', header=0, low_memory=False, dtype='str', index_col=0)
    df_dup = pd.read_table(runID+'.posteriors.DUP.txt' , sep='\t', header=0, low_memory=False, dtype='str', index_col=0)

    # get zscore
    zscore = runID+'.PCA_normalized.filtered.sample_zscores.RD.txt'
    df_zs = pd.read_table(zscore, sep='\t', header=0, low_memory=False, dtype='str', index_col=0)
    df_zs = df_zs.astype(float)
    
    # get reads number
    rd = runID+'.RD.txt'
    #rd = runID+'.PCA_normalized.txt'
    df_rd = pd.read_table(rd, sep='\t', header=0, low_memory=False, dtype='str', index_col=0)
    df_rd=df_rd.astype(float)
    
    f = open(runID+'.result.cnv.txt', 'a')

    for i in range(df_del.shape[0]):
        line1 = df_del.iloc[[i]]
        line2 = df_dup.iloc[[i]]
        cnv1 = get_cnv(line1, prob_cutoff, cnv_len_cutoff, 'del')
        cnv2 = get_cnv(line2, prob_cutoff, cnv_len_cutoff, 'dup')
        cnv = pd.concat([cnv1, cnv2])
        if cnv.empty:
            pass
        else:
            # print(cnv)
            
            # get zscore
            cnv = get_zscore(cnv, df_zs)
            # get reads number
            cnv = get_rd(cnv, df_rd)
            
            # write result
            cnv.to_csv(runID+'.result.txt', sep='\t', header=False, index=False, mode='a')
            
            # write sample cnv format
            samplecnv = get_samplecnv(cnv)
            print(samplecnv, file=f)


def get_cnv(line, prob_cutoff, cnv_len_cutoff, type):
    line = line.iloc[0]
    lineindex = list(line.index)
    line = line.astype(float)
    line = line[line >= prob_cutoff]
    cnv_line = []

    for j in range(len(line)):
        # if j>0 and line.index[j].split(':')[0]==line.index[j-1].split(':')[0] and int(line.index[j].split(':')[1].split('-')[0])==int(line.index[j-1].split(':')[1].split('-')[1])+1:
        if j>0 and line.index[j].split(':')[0]==line.index[j-1].split(':')[0] and lineindex.index(line.index[j])==lineindex.index(line.index[j-1])+1:
            name = line.name
            count = count+1
            chrom = line.index[j].split(':')[0]
            pos = line.index[j].split(':')[1]
            end = int(pos.split('-')[1])
            cnv_line[-1]=cnv_line[-1]._replace(end=end)
            score = float("%.3f" % ((score*(count-1)+line[j])/count))
            cnv_line[-1]=cnv_line[-1]._replace(count=count)
            cnv_line[-1]=cnv_line[-1]._replace(score=score)
            length=cnv_line[-1].end-cnv_line[-1].start
            cnv_line[-1]=cnv_line[-1]._replace(length=length)
        else:
            # number = j+1
            number = lineindex.index(line.index[j])
            count = 1
            name = line.name
            chrom = line.index[j].split(':')[0]
            pos = line.index[j].split(':')[1]
            start = int(pos.split('-')[0])
            end = int(pos.split('-')[1])
            score = float("%.3f" % line[j])
            length = end - start
            cnv = CNV(chrom, start, end, name, type, score, length, count, number)
            cnv_line.append(cnv)

    cnv_line = pd.DataFrame(cnv_line)

    if cnv_line.empty:
        pass
    else:
        cnv_line = cnv_line[cnv_line['length']>cnv_len_cutoff]
    
    return cnv_line


def get_zscore(cnv, df_zs):
    cnv['zscore']=0
    for i in range(len(cnv)):
        df_zs_index = list(df_zs.index)
        samplenum = df_zs_index.index(cnv.iloc[i,list(cnv.columns).index('name')])
        startnum = cnv.iloc[i,list(cnv.columns).index('number')]
        endnum = startnum + cnv.iloc[i,list(cnv.columns).index('count')]
        zsmean = df_zs.iloc[samplenum, startnum:endnum].mean()
        cnv.iloc[i,-1] = round(zsmean,3)
    return cnv


def get_rd(cnv, df_rd):
    cnv['ur']=0
    cnv['copyratio']=0
    for i in range(len(cnv)):
        df_rd_index = list(df_rd.index)
        samplenum = df_rd_index.index(cnv.iloc[i,list(cnv.columns).index('name')])
        startnum = cnv.iloc[i,list(cnv.columns).index('number')]
        endnum = startnum + cnv.iloc[i,list(cnv.columns).index('count')]
        rdmean = df_rd.iloc[samplenum, startnum:endnum].mean()
        cnv.iloc[i,-2] = round(rdmean,3)
        cnv.iloc[i,-1] = round(rdmean/df_rd.iloc[samplenum].mean(),3)
    return cnv


def get_samplecnv(cnv):
    cnv = cnv.sort_values(by='length',ascending=False)
    sample = list(cnv['name'])[0]
    cnvindex = list(cnv.columns)
    samplecnv=[]
    for k in range(cnv.shape[0]):
        c1 = cnv.iloc[k,cnvindex.index('type')]
        c2 = cnv.iloc[k,cnvindex.index('chrom')]
        c3 = str(cnv.iloc[k,cnvindex.index('start')])
        c4 = str(cnv.iloc[k,cnvindex.index('end')])
        c5 = cnv.iloc[k,cnvindex.index('length')]
        
        if c5>1000000:
            c5 = str(round(c5/1000000,1))+'Mb'
        elif c5>1000:
            c5 = str(round(c5/1000))+'Kb'
        
        if abs(cnv.iloc[k,cnvindex.index('zscore')])>3:
            c6 = '-M'
        else:
            c6 = ''
        
        cnvline = c1+'('+c2+':'+c3+'-'+c4+','+c5+')'+c6
        samplecnv.append(cnvline)
    
    samplecnv = sample+'\t'+';'.join(samplecnv)
    return samplecnv


if __name__ == '__main__':
    options = argparse.ArgumentParser(description='XHMM Result Filter')
    options.add_argument('-i', '--input', required=True, help='xhmm DEL.txt file')
    options.add_argument('-p', '--prob', default=0.5, help='probability cutoff')
    options.add_argument('-n', '--len', default=500000, help='cnv length cutoff')
    
    args = options.parse_args()
    #runID = args.input.split('.')[0]
    runID = args.input
    os.system('echo "chrom\tstart\tend\tname\ttype\tscore\tlength\tcount\tnumber\tzscore\tmeanrd\tcopyratio" > %s' % (runID+'.result.txt'))
    os.system('echo "sample\tcnv" > %s' % (runID+'.result.cnv.txt'))
    main(runID, float(args.prob), int(args.len))

# py3 xhmm.new.py -i RunSZ012151 -p 0.9 -n 500000 &



