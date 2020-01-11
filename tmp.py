# import re
# import numpy as np
import sys
import pandas as pd
# sys.path.append('/home/pengjiguang/project/acmgHL')
sys.path.append('/home/yanxinyi/project/PubMed-ACMG/test/mytest/acmg_HL') 
from acmgHL import ACMG, manual_review_format
# from acmgHL import ACMG, manual_review_format, verify_PVS1, verify_PM1, \
#     verify_PM2_BA1_BS1_BS2, verify_PM4_BP3, verify_PP3_BP4_BP7, Strength, bed2vcf
# from collections import namedtuple
# VCFRecord = namedtuple('VCFRecord', ("chrom", "pos", 'ref', 'alt'))
# from gnomAD import VCFRecord

# -----------------------------------------------------------------------------------
# deal with manual acmg result
acmg_manual = 'acmg_manual_interprete.txt'
acmg_manual = pd.read_table(acmg_manual, header=0, sep='\t', dtype='str')

'''
acmg_manual.columns = ['Chr', 'Start', 'Stop', 'Ref', 'Call', 'VCF_COORD', 
        'MIMInheritance', 'GeneSymbol', 'ExIn_ID', 'Transcript', 'Function', 
        'cHGVS', 'pHGVS1', 'pHGVS3', 'PVS1', 'PS1', 'PM5', 'PS2', 'PS3', 
        'PS4', 'PM3', 'PM6', 'PP1', 'PP4', 'BS3', 'BS4', 'BP2', 'BP5', 
        'PM1', 'PM2', 'PM4', 'PP2', 'PP3', 'PP5', 'BA1', 'BS1', 'BS2', 
        'BP1', 'BP3', 'BP4', 'BP6', 'BP7', 'aPVS1', 'aPM1', 'aPM2', 'aBA1', 
        'aBS1', 'aBS2', 'aPP3', 'aBP4', 'aBP7', 'aPM4', 'aBP3']

print(acmg_manual.isnull().sum())
acmg_manual = acmg_manual.fillna('0')
'''

# deal with auto acmg result
acmg_auto_input = 'testpmc.output'
acmg_auto_input = pd.read_table(acmg_auto_input, header=0, sep='\t', dtype='str')

def get_max_type(list):
    code = '0'
    if 'Strong' in list:
        code = 'S'
    elif 'Met' in list:
        code = 'P'
    elif 'Moderate' in list:
        code = 'M'
    elif 'Supporting' in list:
        code = 'P'
    return code

def get_BS3(list):
    code = '0'
    if 'BS3_Supporting' in list:
        code = 'P'
    return code

def get_PM3_PS2_score(num):
    code = '0'
    num = float(num)
    if num > 4:
        code = 'VS'
    elif num > 2:
        code = 'S'
    elif num > 1:
        code = 'M'
    elif num > 0.5:
        code = 'P'
    return code

def evidence_data(vcf_coord, data):
    evid = {'PM3':'Unmet', 'PS2':'Unmet', 'PP4':'Unmet', 'PP1':'Unmet', 'PS3':'Unmet', 'BS3':'Unmet'}
    
    pubmedlist = data[(data.VCF_COORD == vcf_coord) & (data.pm3_point != 'PDF_Only')]
    # pubmedlist[pubmedlist.columns[pd.Series(pubmedlist.columns).str.startswith('pm3')]]
    pm3point = pubmedlist.pm3_point[pubmedlist.pm3_point!='0']
    ps2point = pubmedlist.ps2_point[pubmedlist.ps2_point!='0']
    ps3evid = pubmedlist.ps3_strength[pubmedlist.ps3_strength!='Unmet']
    pp1point = pubmedlist.pp1_strength[(pubmedlist.pp1_strength!='0') & (pubmedlist.pp1_strength!='Unmet')]
    pp4evid = pubmedlist.pp4_strength[(pubmedlist.pp4_strength.notna()) & (pubmedlist.pp4_strength!='Unmet')]

    pm3point = [max(list(map(float, x.split('|@|')))) for x in pm3point]
    if sum(pm3point) > 0:
        evid['PM3'] = get_PM3_PS2_score(sum(pm3point))
    else:
        evid['PM3'] = '0'
    if sum(ps2point.astype('float')) > 0:
        evid['PS2'] = get_PM3_PS2_score(sum(ps2point.astype('float')))
    else:
        evid['PS2'] = '0'

    evid['PS3'] = get_max_type(list(ps3evid))
    evid['BS3'] = get_BS3(list(ps3evid))
    evid['PP1'] = get_max_type(list(pp1point))
    evid['PP4'] = get_max_type(list(pp4evid))

    evid = [str(x) for x in evid.values()]
    return ';'.join(evid)

acmg_auto = acmg_manual.copy()
acmg_auto['evidence'] = acmg_auto['VCF_COORD'].apply(evidence_data, args = (acmg_auto_input,))
acmg_auto['auPM3'] = acmg_auto['evidence'].map(lambda x:x.split(';')[0])
acmg_auto['auPS2'] = acmg_auto['evidence'].map(lambda x:x.split(';')[1])
acmg_auto['auPP4'] = acmg_auto['evidence'].map(lambda x:x.split(';')[2])
acmg_auto['auPP1'] = acmg_auto['evidence'].map(lambda x:x.split(';')[3])
acmg_auto['auPS3'] = acmg_auto['evidence'].map(lambda x:x.split(';')[4])
acmg_auto['auBS3'] = acmg_auto['evidence'].map(lambda x:x.split(';')[5])
acmg_auto = acmg_auto.drop(['evidence'], axis=1)


# -----------------------------------------------------------------------------------
# create evidence dict
def get_evidence_dict(list, source):
    info = list

    if source == 'manual':
        if info['auPM3'] == '':
            info['auPM3'] = ''

        if info['auPS2'] == '':
            info['auPS2'] =''

        if info['auPP4'] == '':
            info['auPP4'] =''

        if info['auPP1'] == '':
            info['auPP1'] =''

        if info['auPS3'] == '':
            info['auPS3'] =''

        if info['auBS3'] == '':
            info['auBS3'] = ''

    if source == 'manual':
        acmg = {'PVS1': info['PVS1'], 'PS1': info['PS1'], 'PM5': info['PM5'],
                'PS2': info['PS2-de'], 'PM6': info['PM6-de'], 'PS3': info['PS3-FUN'],
                'BS3': info['BS3-FUN'], 'PM3': info['PM3-cis/trans'],
                'BP2': info['BP2-cis/trans'], 'PP1': info['PP1-SEG'],
                'BS4': info['BS4-SEG'], 'PS4': info['PS4'], 'PP4': info['PP4'],
                'BP5': info['BP5'], 'PM1': info['PM1'], 'PM2': info['PM2'],
                'PM4': info['PM4'], 'PP2': info['PP2'], 'PP3': info['PP3'],
                'PP5': info['PP5'], 'BA1': info['BA1'], 'BS1': info['BS1'],
                'BS2': info['BS2'], 'BP1': info['BP1'], 'BP3': info['BP3'],
                'BP4': info['BP4'], 'BP6': info['BP6'], 'BP7': info['BP7']}
    elif source == 'auto':
        acmg = {'PVS1': info['PVS1'], 'PS1': info['PS1'], 'PM5': info['PM5'],
                'PS2': info['auPS2'], 'PM6': info['PM6-de'],'PS3': info['auPS3'],
                'BS3': info['auBS3'], 'PM3': info['auPM3'],
                'BP2': info['BP2-cis/trans'], 'PP1': info['auPP1'],
                'BS4': info['BS4-SEG'], 'PS4': info['PS4'], 'PP4': info['auPP4'],
                'BP5': info['BP5'], 'PM1': info['PM1'], 'PM2': info['PM2'],
                'PM4': info['PM4'], 'PP2': info['PP2'], 'PP3': info['PP3'],
                'PP5': info['PP5'], 'BA1': info['BA1'], 'BS1': info['BS1'],
                'BS2': info['BS2'], 'BP1': info['BP1'], 'BP3': info['BP3'],
                'BP4': info['BP4'], 'BP6': info['BP6'], 'BP7': info['BP7']}
    elif source == 'onlyauto':
        # remove PM3,BP2,PS2,PM6,PS3,BS3,PP4,BP5,PP1
        # auto auPM3, auPS2, auPP4, auPP1, auPS3, auBS3
        acmg = {'PVS1': info['PVS1'], 'PS1': info['PS1'], 'PM5': info['PM5'],
                'PS2': '0', 'PM6': '0','PS3': '0',
                'BS3': '0', 'PM3': '0',
                'BP2': '0', 'PP1': '0',
                'BS4': info['BS4-SEG'], 'PS4': info['PS4'], 'PP4': '0',
                'BP5': '0', 'PM1': info['PM1'], 'PM2': info['PM2'],
                'PM4': info['PM4'], 'PP2': info['PP2'], 'PP3': info['PP3'],
                'PP5': info['PP5'], 'BA1': info['BA1'], 'BS1': info['BS1'],
                'BS2': info['BS2'], 'BP1': info['BP1'], 'BP3': info['BP3'],
                'BP4': info['BP4'], 'BP6': info['BP6'], 'BP7': info['BP7']}
    return acmg

def get_acmg_result(line, source):
    evidence = get_evidence_dict(line, source)
    acmg = manual_review_format(evidence)
    
    '''
    chr = line['VCF_COORD'].split('-')[0]
    pos = line['VCF_COORD'].split('-')[1]
    ref = line['VCF_COORD'].split('-')[2]
    alt = line['VCF_COORD'].split('-')[3]
    inheritance = line['MIMInheritance']
    vcfrecord = VCFRecord(chr, pos, ref, alt)
    acmg['PVS1'] = verify_PVS1(line)
    if str(line['PVS1']) == '5':
        acmg['PVS1'] = Strength.VeryStrong

    acmg['PM1'] = verify_PM1(line)
    acmg['PM2'], acmg['BA1'], acmg['BS1'], acmg['BS2'] = verify_PM2_BA1_BS1_BS2(vcfrecord, inheritance)
    acmg['PM4'], acmg['BP3'] = verify_PM4_BP3(line)
    acmg['PP3'], acmg['BP4'], acmg['BP7'] = verify_PP3_BP4_BP7(line)

    # Deprecated PP2 / BP1, PP5 / BP6
    acmg['PP2'] = Strength.Unmet
    acmg['BP1'] = Strength.Unmet
    acmg['PP5'] = Strength.Unmet
    acmg['BP6'] = Strength.Unmet
    '''

    verdict = ACMG(acmg)
    result = [','.join(verdict.evidences), verdict.classification]
    # line['evidences'] = ','.join(verdict.evidences)
    # line['classification'] = verdict.classification
    return result

acmg_result = pd.DataFrame(columns = list(acmg_auto.columns) + ['manual_evidences', 'manual_classification', 
            'auto_evidences', 'auto_classification', 'onlyauto_evidences', 'onlyauto_classification'])
for i in range(acmg_auto.shape[0]):

    line = acmg_auto.iloc[i, ]
    if line['VCF_COORD'].startswith('MT'):
        #　print('\t'.join(list(line.fillna('NA')) + ['NA', 'NA', 'NA', 'NA']))
        acmg_result.loc[i] = list(line) + ['NA', 'NA', 'NA', 'NA', 'NA', 'NA']
    else:
        manual_result = get_acmg_result(line, 'manual')
        auto_result = get_acmg_result(line, 'auto')
        # print('\t'.join(list(line) + manual_result + auto_result))
        onlyauto_result = get_acmg_result(line, 'onlyauto')
        acmg_result.loc[i] = list(line) + manual_result + auto_result + onlyauto_result

acmg_result.to_csv('acmg_result.txt', sep='\t', index=0)


# -----------------------------------------------------------------------------------
# deal with manual acmg result
# all
acmg_count = acmg_result.groupby(['auto_classification', 'manual_classification'], as_index=False)['VCF_COORD'].count()
acmg_count = acmg_count.pivot(index='auto_classification', columns='manual_classification', values='VCF_COORD')
acmg_count = acmg_count[['Benign', 'Likely_Benign', 'Uncertain_Significance', 'Likely_Pathogenic', 'Pathogenic']]
acmg_count = acmg_count.reindex(['Benign', 'Likely_Benign', 'Uncertain_Significance', 'Likely_Pathogenic', 'Pathogenic'])
acmg_count.to_csv('acmg_result_count.txt', sep='\t')

acmg_count = acmg_result.groupby(['auto_classification', 'onlyauto_classification'], as_index=False)['VCF_COORD'].count()
acmg_count = acmg_count.pivot(index='auto_classification', columns='onlyauto_classification', values='VCF_COORD')
acmg_count = acmg_count[['Benign', 'Likely_Benign', 'Uncertain_Significance', 'Likely_Pathogenic', 'Pathogenic']]
acmg_count = acmg_count.reindex(['Benign', 'Likely_Benign', 'Uncertain_Significance', 'Likely_Pathogenic', 'Pathogenic'])
print(acmg_count)

acmg_count = acmg_result.groupby(['onlyauto_classification', 'manual_classification'], as_index=False)['VCF_COORD'].count()
acmg_count = acmg_count.pivot(index='onlyauto_classification', columns='manual_classification', values='VCF_COORD')
acmg_count = acmg_count[['Benign', 'Likely_Benign', 'Uncertain_Significance', 'Likely_Pathogenic', 'Pathogenic']]
acmg_count = acmg_count.reindex(['Benign', 'Likely_Benign', 'Uncertain_Significance', 'Likely_Pathogenic', 'Pathogenic'])
print(acmg_count)


# 150 loci
loci150 = '150locilist'
loci150 = pd.read_table(loci150, header=None, sep='\t', dtype='str')
loci150.columns = ['VCF_COORD']
acmg_result150 = pd.merge(loci150, acmg_result, on='VCF_COORD', how='inner')

acmg150_count = acmg_result150.groupby(['auto_classification', 'manual_classification'], as_index=False)['VCF_COORD'].count()
acmg150_count = acmg150_count.pivot(index='auto_classification', columns='manual_classification', values='VCF_COORD')
acmg150_count = acmg150_count[['Benign', 'Likely_Benign', 'Uncertain_Significance', 'Likely_Pathogenic', 'Pathogenic']]
acmg150_count = acmg150_count.reindex(['Benign', 'Likely_Benign', 'Uncertain_Significance', 'Likely_Pathogenic', 'Pathogenic'])
acmg150_count.to_csv('acmg_result_count150.txt', sep='\t')

acmg150_count = acmg_result150.groupby(['auto_classification', 'onlyauto_classification'], as_index=False)['VCF_COORD'].count()
acmg150_count = acmg150_count.pivot(index='auto_classification', columns='onlyauto_classification', values='VCF_COORD')
acmg150_count = acmg150_count[['Benign', 'Likely_Benign', 'Uncertain_Significance', 'Likely_Pathogenic', 'Pathogenic']]
acmg150_count = acmg150_count.reindex(['Benign', 'Likely_Benign', 'Uncertain_Significance', 'Likely_Pathogenic', 'Pathogenic'])
print(acmg150_count)

acmg150_count = acmg_result150.groupby(['onlyauto_classification', 'manual_classification'], as_index=False)['VCF_COORD'].count()
acmg150_count = acmg150_count.pivot(index='onlyauto_classification', columns='manual_classification', values='VCF_COORD')
acmg150_count = acmg150_count[['Benign', 'Likely_Benign', 'Uncertain_Significance', 'Likely_Pathogenic', 'Pathogenic']]
acmg150_count = acmg150_count.reindex(['Benign', 'Likely_Benign', 'Uncertain_Significance', 'Likely_Pathogenic', 'Pathogenic'])
print(acmg150_count)



# -----------------------------------------------------------------------------------
'''
# test
i = 6
i = 2387
line = acmg_auto.iloc[i, ]
get_acmg_result(line, 'manual')
get_acmg_result(line, 'auto')

source = 'auto'
evidence = get_evidence_dict(line, source)
acmg = manual_review_format(evidence)


'''


# -----------------------------------------------------------------------------------
'''
# 枚举
level = 
value = 
class Strength(Enum):
    """
    ACMG pathogenic strength
    """
    Unmet = 0
    Supporting = 1
    Moderate = 2
    Strong = 3
    VeryStrong = 4

    def upgrade(level):
        if value + level <= 4:
            return Strength(value + level)
        else:
            return Strength(4)

    def downgrade(level):
        if value - level >= 0:
            return Strength(value - level)
        else:
            return Strength(0)

'''