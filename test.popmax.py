# ---------------------------------------------------------------------------------
import sys
from pyfaidx import Fasta
# from collections import namedtuple
# VCFRecord = namedtuple('VCFRecord', ("chrom", "pos", 'ref', 'alt'))
genome = Fasta('/data/hg19/hg19.fa')

import pandas as pd
sys.path.append('/data/gnomAD/')
from gnomAD import GNOMAD

input = 'anno.hgmd.gnomAD.select'
anno_hgmd = pd.read_table(input, header=0, sep='\t', dtype='str')
genelist = 'HLgene.list'
genelist = pd.read_table(genelist, header=None, sep='\t', dtype='str')
genelist.columns = ['Gene Symbol']

anno_hgmd_filter = pd.merge(anno_hgmd, genelist, how = 'inner', on = 'Gene Symbol')
anno_hgmd_filter.to_csv('anno.hgmd.gnomAD.filter', sep='\t', index=0, na_rep='NA', header=None)


# ---------------------------------------------------------------------------------
anno_hgmd_filter = pd.read_table('anno.hgmd.gnomAD.filter', header=None, sep='\t', dtype='str')
anno_hgmd_filter.columns = ['Chr', 'Start', 'Stop', 'Ref', 'Call', 'wgs_GnomAD_AC', 
        'wgs_GnomAD_AN', 'wgs_GnomAD_AF', 'wgs_GnomAD_Homo', 'MapLoc', 'SampleID', 
        'VarType', 'Zygosity', 'A.Depth', 'A.Ratio', 'Filter', 'Gene_Symbol', 'ExIn_ID', 
        'Function', 'cHGVS', 'pHGVS', 'pHGVS1', 'pHGVS3', 'rsID']

# get vcf format
def bed2vcf(bed):
    """
    transform bed to vcf, and complement the missing "." in ref and alt
    :param chrom:
    :param start:
    :param ref:
    :param alt:
    :return: Str
    """
    chrom, start, ref, alt = bed.split('-')
    start = int(start)
    chrom = chrom.replace('chr', '')
    if ref in ['','.','-'] or alt in ['','.','-']:
        pos = start
        chrom_num = 'chr' + str(chrom)
        complement = genome[chrom_num][start-1:start].seq
        ref = (complement + ref).replace('.', '').replace('-', '')
        alt = (complement + alt).replace('.', '').replace('-', '')
    else:
        pos = start + 1
    return '-'.join([chrom, str(pos), ref, alt])

anno_hgmd_filter['bed'] = anno_hgmd_filter['Chr']+'-'+anno_hgmd_filter['Start']+'-'+anno_hgmd_filter['Ref']+'-'+anno_hgmd_filter['Call']
anno_hgmd_filter['vcf'] = anno_hgmd_filter['bed'].apply(bed2vcf)

# exceptionlist
exceptionlist = 'exception.list'
exceptionlist = pd.read_table(exceptionlist, header=0, sep='\t', dtype='str')
exceptionlist = exceptionlist[['Index', 'VCF_COORD']]
exceptionlist.columns = ['Exception', 'VCF_COORD']
anno_hgmd_filter = pd.merge(anno_hgmd_filter, exceptionlist, left_on='vcf', right_on='VCF_COORD', how='left')
anno_hgmd_filter = anno_hgmd_filter.drop(['VCF_COORD'], axis=1)

# popmax
def get_popmax(vcf):
    varient = vcf.upper()
    test1 = GNOMAD(varient)
    popmax = test1.af_popmax
    popmax_filter = test1.af_popmax_filter
    return popmax, popmax_filter

# anno_hgmd_filter['pop_max'] = anno_hgmd_filter['vcf'].apply(get_popmax)
anno_hgmd_filter['pop_max'], anno_hgmd_filter['popmax_filter'] = zip(*anno_hgmd_filter['vcf'].apply(get_popmax))
anno_hgmd_filter.to_csv('anno.hgmd.gnomAD.filter.popmax', sep='\t', index=0, na_rep='NA')



'''
anno_hgmd_filter_0 = anno_hgmd_filter.iloc[0:5, :].copy()
# anno_hgmd_filter_0['pop_max'] = anno_hgmd_filter_0['vcf'].apply(get_popmax)
anno_hgmd_filter_0['pop_max'], anno_hgmd_filter_0['popmax_filter'] = zip(*anno_hgmd_filter_0['vcf'].apply(get_popmax))
'''


