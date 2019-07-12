import re
import argparse
import pandas as pd
import numpy as np
import sys
input1=sys.argv[1]
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
            # print('\t'.join(line).replace(',','')+'\t'+sample+'\t'+sex+'\t'+cnvtype+'\t'+runid)
    
    cnvlist = pd.DataFrame(cnv_list)
    cnvlist.columns = header

    return cnvlist


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
                    # cgenetmp = linegene.iloc[j][3]+'|chr'+linegene.iloc[j][0]+':'+str(linegene.iloc[j][1])+'-'+str(linegene.iloc[j][2])+'|'+str(overlap)
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
                    
                    # cdiseasetmp = linedisease.iloc[j][5]+'|chr'+linedisease.iloc[j][0]+':'+str(linedisease.iloc[j][1])+'-'+str(linedisease.iloc[j][2])+'|'+overlap+'/'+linedisease.iloc[j][4]
                    cdiseasetmp = linedisease.iloc[j][5]+'|'+overlap+'/'+linedisease.iloc[j][4]
                    
                    cdisease.append(cdiseasetmp)
                else:
                    cdisease.append('<'+str(overlap_len))

            cnv_disease.append(list(line)+[';'.join(cdisease)])
        else:
            cnv_disease.append(list(line)+['NA'])

    cnvdisease = pd.DataFrame(cnv_disease)
    return cnvdisease


def get_arraycnv(cnvlist, arraylist):

    cnvlist = tran2bedformat(cnvlist)
    arraylist = tran2bedformat(arraylist)

    cnv_array = []
    for i in range(cnvlist.shape[0]):
        line = cnvlist.iloc[i]
        linearray = arraylist[(arraylist[0]==line[0]) & (arraylist[5]==line[3]) & (arraylist[1]<line[2]) & (arraylist[2]>line[1])]
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

                carraytmp = linearray.iloc[j][8]+'|'+overlap+'/'+cnvlen
                carray.append(carraytmp)

            cnv_array.append(list(line)+[';'.join(carray)])
        else:
            cnv_array.append(list(line)+['NA'])

    cnvarray = pd.DataFrame(cnv_array)
    return cnvarray

    



def main(fcnv, fgene, farray, fdisease, prob, length):

    cnvarray = pd.read_table(farray, sep='\t', low_memory=False, dtype='str', index_col=0)
    arraylist = cnvarray2bed(cnvarray)
    arraylist.to_csv('array.bed', sep='\t', header=False, index=False, mode='w')
    arraylist.columns=[0,1,2,3,4,5,6,7,8]

    genelist = pd.read_table(fgene, sep='\t', low_memory=False, dtype='str', header=None)
    genelist = genelist[genelist.iloc[:,1]!='start']

    cnvlist = pd.read_table(fcnv, sep='\t', low_memory=False, dtype='str', header=None)
    cnvlist = cnvlist[cnvlist.iloc[:,1]!='start']

    diseaselist = pd.read_table(fdisease, sep='\t', low_memory=False, dtype='str', header=None)
    diseaselist = diseaselist[diseaselist.iloc[:,1]!='start']


    cnvdisease = get_disease(cnvlist, diseaselist, length)
    cnvdisease.to_csv('cnv.disease.txt', sep='\t', header=False, index=False, mode='w')

    cnvgene = get_gene(cnvdisease, genelist, prob)
    cnvgene.to_csv('cnv.disease.gene.txt', sep='\t', header=False, index=False, mode='w')

    cnvgenearray = get_arraycnv(cnvgene, arraylist)
    cnvgenearray.to_csv('cnv.disease.gene.array.txt', sep='\t', header=False, index=False, mode='w')



if __name__ == '__main__':
    options = argparse.ArgumentParser(description='Result Filter')
    options.add_argument('-c', '--cnv', required=True, help='cnv file')
    options.add_argument('-g', '--gene', required=True, help='gene file')
    options.add_argument('-a', '--array', required=True, help='array file')
    options.add_argument('-d', '--disease', required=True, help='disease file')
    options.add_argument('-p', '--prob', default=0.5, help='probability cutoff')
    options.add_argument('-n', '--len', default=100000, help='cnv length cutoff')
    
    args = options.parse_args()
    # os.system('echo "chrom\tstart\tend\tname\ttype\tscore\tlength\tcount\tnumber\tzscore\tmeanrd\tcopyratio" > %s' % (runID+'.result.txt'))
    # os.system('echo "sample\tcnv" > %s' % (runID+'.result.cnv.txt'))
    main(args.cnv, args.gene, args.array, args.disease, float(args.prob), int(args.len))


