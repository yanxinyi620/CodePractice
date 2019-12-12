import gzip
import re
# import numpy as np
import pandas as pd

gene2pubtator = '/data/pubTator/gene2pubtatorcentral.gz'
mutation2pubtator = '/data/pubTator/mutation2pubtatorcentral.gz'
avada = '/data/AVADA/avada_v1.00_2016.vcf'
clinvar = '/home/pengjiguang/data/clinvar/tab_delimited/20191119/var_citations.txt'
clinvarvcf = '/home/pengjiguang/data/clinvar/clinvar_20191118.vcf.gz'

# --------------------------------------------------------------------------------
# clinvar source
clin = pd.read_table(clinvar, header=0, sep='\t', dtype='str')
clinvcf = pd.read_table(clinvarvcf, compression='gzip', header=27, sep='\t', dtype='str')

def clinvarvcfinfo(info):
    
    clinvarinfo = {'ALLELEID':'unknown', 'CLNHGVS':'unknown', 'GENEINFO':'unknown', 'transcript':'unknown'}
    infolist = info.split(';')
    for i in infolist:
        if '=' in i:
            item = i.split('=')
            if item[0] in clinvarinfo.keys():
                clinvarinfo[item[0]] = item[1]
    
    if ':' in clinvarinfo['CLNHGVS']:
        clinvarinfo['transcript'] = clinvarinfo['CLNHGVS'].split(':')[0]
    
    return ';'.join(list(clinvarinfo.values()))

clinvcf['INFO'] = clinvcf['INFO'].apply(clinvarvcfinfo)
clinvcf['ALLELEID'] = clinvcf['INFO'].map(lambda x:x.split(';')[0])
clinvcf['CLNHGVS'] = clinvcf['INFO'].map(lambda x:x.split(';')[1])
clinvcf['GENEINFO'] = clinvcf['INFO'].map(lambda x:x.split(';')[2])
clinvcf['transcript'] = clinvcf['INFO'].map(lambda x:x.split(';')[3])

clin = clin[['VariationID', 'citation_source', 'citation_id']]
clin = clin.drop_duplicates()
clinvcf = clinvcf.rename(columns={'ID':'VariationID' , '#CHROM':'CHROM'})
clinvarpubmed = pd.merge(clin, clinvcf, how='inner', on='VariationID')
clinvarpubmed['chgvs'] = 'unknown'
clinvarpubmed['phgvs'] = 'unknown'
clinvarpubmed = clinvarpubmed[['CHROM', 'POS', 'REF', 'ALT', 'VariationID', 'GENEINFO', 'transcript', 'chgvs', 'phgvs', 'citation_id', 'citation_source']]

clinvarpubmed.to_csv('clinvarpubmed.csv', sep='\t', index=0, na_rep='NA')

# --------------------------------------------------------------------------------
# avada source
avad = pd.read_table(avada, header=28, sep='\t', dtype='str')

def avadainfo(info):
    
    avadainfo = {'PMID':'unknown', 'GENE_SYMBOL':'unknown', 'REFSEQ_ID':'unknown', 'ORIGINAL_VARIANT_STRING':'unknown'}
    infolist = info.split(';')
    for i in infolist:
        if '=' in i:
            item = i.split('=')
            if item[0] in avadainfo.keys():
                avadainfo[item[0]] = item[1]
    
    return ';'.join(list(avadainfo.values()))

avad['INFO'] = avad['INFO'].apply(avadainfo)
avad['PMID'] = avad['INFO'].map(lambda x:x.split(';')[0])
avad['GENE_SYMBOL'] = avad['INFO'].map(lambda x:x.split(';')[1])
avad['REFSEQ_ID'] = avad['INFO'].map(lambda x:x.split(';')[2])
avad['ORIGINAL_VARIANT_STRING'] = avad['INFO'].map(lambda x:x.split(';')[3])
avad = avad.rename(columns={'#CHROM':'CHROM'})
avad['chgvs'] = 'unknown'
avad['phgvs'] = 'unknown'
avad['citation_source'] = 'avada'
avad = avad[['CHROM', 'POS', 'REF', 'ALT', 'PMID', 'GENE_SYMBOL', 'REFSEQ_ID', 'ORIGINAL_VARIANT_STRING', 'chgvs', 'phgvs', 'citation_source']]

avad.to_csv('avadapubmed.csv', sep='\t', index=0, na_rep='NA')

# --------------------------------------------------------------------------------
# pubtator source
gene2pub = pd.read_csv(gene2pubtator, header=None, compression='gzip', sep='\t',  quoting=3, dtype='str')
mutation2pub = pd.read_table(mutation2pubtator, header=None, compression='gzip', sep='\t', dtype='str')

gene2pub.columns = ['PMID', 'type', 'ENTREZ_ID', 'gene', 'genesource']
mutation2pub.columns = ['PMID', 'mutationtype', 'newhgvs', 'rawhgvs', 'mutationsource']

pubtator = pd.merge(gene2pub, mutation2pub, how='inner', on='PMID')
print(pubtator.isnull().sum())
pubtator = pubtator[(pubtator['mutationsource'].notna()) & (pubtator['mutationsource'].str.contains('tmVar'))]

pubtator.to_csv('pubtatorpubmed.csv', sep='\t', index=0, na_rep='NA')



# --------------------------------------------------------------------------------
# search PMID
# clinvarpubmed
# avad
# pubtator

test = 'test.rs.1.txt'
test = pd.read_table(test, header=0, sep='\t')

clinvarpubmed['VCF_COORD'] = clinvarpubmed['CHROM'] + '-' + clinvarpubmed['POS']+ '-' + clinvarpubmed['REF'] + '-' + clinvarpubmed['ALT']
testclinvar = pd.merge(test, clinvarpubmed, how='left', on='VCF_COORD')

avad['VCF_COORD'] = avad['CHROM'] + '-' + avad['POS']+ '-' + avad['REF'] + '-' + avad['ALT']
testavad = pd.merge(test, avad, how='left', on='VCF_COORD')

# --------------
# pubtator test 1
'''
testrsID = test.dropna(subset=["rsID"])
testpubtator = pd.merge(testrsID, mutation2pub, how='inner', left_on='rsID', right_on='newhgvs')
'''

def get_aa_abbr(phgvs):

    # U and O are the 21 and 22 aa
    aa = {'Ala':'A','Phe':'F','Cys':'C','Sec':'U','Asp':'D','Asn':'N','Glu':'E','Gln':'Q','Gly':'G','His':'H','Leu':'L','Ile':'I','Lys':'K','Pyl':'O','Met':'M','Pro':'P','Arg':'R','Ser':'S','Thr':'T','Val':'V','Trp':'W','Tyr':'Y','Ter':'X'}
    
    phgvs = phgvs.split(';')[0]
    phgvs = phgvs.replace(' ', '')
    for key in aa:
        if key in phgvs:
            phgvs = phgvs.replace(key, aa[key])

    return phgvs

# pubtator test 2
'''
result = []
for i in range(test.shape[0]):
    for j in range(pubtator.shape[0]):
        pubtator.newhgvs[i] = get_aa_abbr(pubtator.newhgvs[i])
        if (not pd.isna(test.rsID[i]) and test.rsID[i] == pubtator.newhgvs[j]) or test.cHGVS[i] == pubtator.newhgvs[j] or test.pHGVS1[i] == pubtator.newhgvs[j]:
            result.append(test + [pubtator.PMID[j]])
testpubtator = pd.DataFrame(result)
'''

# pubtator test 3
pubtator['newhgvs'] = pubtator['newhgvs'].apply(get_aa_abbr)
test1 = test.dropna(subset=["rsID"])
test2 = test
test3 = test[test.pHGVS1 != '.']

testpubtator1 = pd.merge(test1, pubtator, how='inner', left_on='rsID', right_on='newhgvs')
testpubtator2 = pd.merge(test2, pubtator, how='inner', left_on='cHGVS', right_on='newhgvs')
testpubtator3 = pd.merge(test3, pubtator, how='inner', left_on='pHGVS1', right_on='newhgvs')
testpubtator = testpubtator1.append([testpubtator2, testpubtator3]).drop_duplicates()

testclinvar.to_csv('testclinvar.pmid.csv', sep='\t', index=0, na_rep='NA')
testavad.to_csv('testavad.pmid.csv', sep='\t', index=0, na_rep='NA')
testpubtator.to_csv('testpubtator.pmid.csv', sep='\t', index=0, na_rep='NA')

# 验证 testpubtator 使用 phgvs 和 chgvs 匹配的准确性
testpubtator_rsID = testpubtator1[['VCF_COORD', 'GeneSymbol', 'Transcript', 'cHGVS', 'pHGVS1', 'pHGVS3', 'rsID', 'PMID', 'mutationtype', 'newhgvs', 'rawhgvs', 'mutationsource']].drop_duplicates()
testpubtator_all = testpubtator[['VCF_COORD', 'GeneSymbol', 'Transcript', 'cHGVS', 'pHGVS1', 'pHGVS3', 'rsID', 'PMID', 'mutationtype', 'newhgvs', 'rawhgvs', 'mutationsource']].drop_duplicates()
testpubtator_rsID.to_csv('testpubtator.pmid.rsID.csv', sep='\t', index=0, na_rep='NA')
testpubtator_all.to_csv('testpubtator.pmid.all.csv', sep='\t', index=0, na_rep='NA')



# --------------------------------------------------------------------------------
# result verify
test_result = 'test.result.txt'
test_result = pd.read_table(test_result, header=0, sep='\t')

testclinvar = pd.read_table('testclinvar.pmid.csv', header=0, sep='\t')
testavad = pd.read_table('testavad.pmid.csv', header=0, sep='\t', dtype='str')
testpubtator = pd.read_table('testpubtator.pmid.csv', header=0, sep='\t', dtype='str')

testclinvar = testclinvar[['VCF_COORD', 'citation_id', 'citation_source']].drop_duplicates()
testavad = testavad[['VCF_COORD', 'PMID', 'citation_source']].drop_duplicates()
testpubtator = testpubtator[['VCF_COORD', 'PMID', 'mutationsource']].drop_duplicates()

testclinvar.columns = ['VCF_COORD', 'PMID', 'citation_source']
testpubtator.columns = ['VCF_COORD', 'PMID', 'citation_source']
testpmid = testclinvar.append([testavad, testpubtator]).drop_duplicates(['VCF_COORD', 'PMID'], 'first')

def concatpmid(df):
    r = []
    for i in range(df.shape[1]):
        r = r + [','.join(df.iloc[:, i].dropna(axis=0,how='any').values)]
    return pd.Series(r)
    
testpmid = testpmid.groupby(['VCF_COORD'])['PMID', 'citation_source'].apply(concatpmid)
testpmid = testpmid.reset_index()
testpmid.columns = ['VCF_COORD', 'PMID', 'citation_source']

result = pd.merge(test_result, testpmid, how='inner', on='VCF_COORD')

def stat_result(PubMedID, PMID):
    
    PubMedID = list(set(re.findall(re.compile(r'PMID(\d+)'), PubMedID)))
    if PubMedID:
        len1 = len(PubMedID)
    else:
        len1 = 0
    
    if PMID:
        len2 = PMID.count(',')+1
    else:
        len2 = 0
    
    samepmid = 0
    if PubMedID and PMID:
        for i in range(len2):
            if PMID.split(',')[i] in PubMedID:
                samepmid += 1

    return '|'.join([str(len1), str(len2), str(samepmid)])

result['stat_result'] = result.apply(lambda row: stat_result(row['PubMedID'], row['PMID']), axis=1)
result['PubMed_num'] = result['stat_result'].map(lambda x:x.split('|')[0])
result['PMID_num'] = result['stat_result'].map(lambda x:x.split('|')[1])
result['PMID_same_num'] = result['stat_result'].map(lambda x:x.split('|')[2])

result.to_csv('test.pmid.txt', sep='\t', index=0, na_rep='NA')



# --------------------------------------------------------------------------------
# pmid2pmc
pmid2pmc = '/data/pubTator/pmcid.pmid'
pmid2pmc = pd.read_table(pmid2pmc, header=0, sep='\t', dtype='str')

def get_pmc(PubMedID, PMID):

    global pmid2pmc
    PubMedID = list(set(re.findall(re.compile(r'PMID(\d+)'), PubMedID)))
    pmcn = nopmcn = 0
    pmcid = []
    if PubMedID:
        for i in PubMedID:
            pmctmp = ','.join(pmid2pmc.PMCID[pmid2pmc.PMID == i].values)
            if pmctmp:
                pmcid.append(pmctmp)
                if i in PMID.split(','):
                    pmcn+=1
                else:
                    nopmcn+=1
            
            else:
                pmcid.append('noPMC')
    else:
        pmcid = '0'

    return '|'.join([str(pmcn), str(nopmcn), ','.join(pmcid)])

result['pmid2pmc'] = result.apply(lambda row: get_pmc(row['PubMedID'], row['PMID']), axis=1)
result['matchPMC_num'] = result['pmid2pmc'].map(lambda x:x.split('|')[0])
result['unmatchPMC_num'] = result['pmid2pmc'].map(lambda x:x.split('|')[1])
result['PMCID'] = result['pmid2pmc'].map(lambda x:x.split('|')[2])

result.to_csv('test.pmid.pmc.txt', sep='\t', index=0, na_rep='NA')