# import gzip
import re
import numpy as np
import pandas as pd

# deal with test_result
test_result = 'test.result.txt'
test_result = pd.read_table(test_result, header=0, sep='\t', dtype='str')

def evidence(info):
    evid = {'pubmed':0, 'PM3':0, 'PS2':0, 'PP4':0, 'PP1':0, 'PS3':0}
    infolist = info.split(';')
    for i in infolist:
        if ':' in i and 'PMID' in i:
            evid['pubmed'] = evid['pubmed'] + 1
            item = i.split(':')
            if item[0] in evid.keys():
                evid[item[0]] = evid[item[0]] + 1
    evid = [str(x) for x in evid.values()]
    return ';'.join(evid)

test_result['evidence'] = test_result['PubMedID'].apply(evidence)
test_result['pubmed'] = test_result['evidence'].map(lambda x:x.split(';')[0])
test_result['PM3'] = test_result['evidence'].map(lambda x:x.split(';')[1])
test_result['PS2'] = test_result['evidence'].map(lambda x:x.split(';')[2])
test_result['PP4'] = test_result['evidence'].map(lambda x:x.split(';')[3])
test_result['PP1'] = test_result['evidence'].map(lambda x:x.split(';')[4])
test_result['PS3'] = test_result['evidence'].map(lambda x:x.split(';')[5])
test_result = test_result.drop(['evidence'], axis=1)
# test_result.to_csv('test_result.txt', sep='\t', index=0)


# deal with output
output = 'testpmc.reverse.output'
output = pd.read_table(output, header=0, sep='\t', dtype='str')
outputPMC = output[output.PMCID != 'noPMC']
outputPMID = output[output.PMCID == 'noPMC']

def evidence_data(info, data):
    evid = {'related':0, 'pubmed':0, 'PM3':0, 'PS2':0, 'PP4':0, 'PP1':0, 'PS3':0, 
            'PM3score':0, 'PS2score':0, 'PP1score':0}
    
    pubmedlist = data[(data.VCF_COORD == info) & (data.pm3_point != 'PDF_Only')]
    evid['related'] = pubmedlist.shape[0]

    # pubmedlist[pubmedlist.columns[pd.Series(pubmedlist.columns).str.startswith('pm3')]]
    pm3point = pubmedlist.pm3_point[pubmedlist.pm3_point!='0']
    ps2point = pubmedlist.ps2_point[pubmedlist.ps2_point!='0']
    ps3evid = pubmedlist.ps3_strength[pubmedlist.ps3_strength!='Unmet']
    pp1point = pubmedlist.pp1_strength[(pubmedlist.pp1_strength!='0') & (pubmedlist.pp1_strength!='Unmet')]
    pp4evid = pubmedlist.pp4_strength[(pubmedlist.pp4_strength.notna()) & (pubmedlist.pp4_strength!='Unmet')]
    
    evid['PM3'] = len(pm3point)
    evid['PS2'] = len(ps2point)
    evid['PS3'] = len(ps3evid)
    evid['PP1'] = len(pp1point)
    evid['PP4'] = len(pp4evid)

    pm3point = [max(list(map(float, x.split('|')))) for x in pm3point]
    evid['PM3score'] = sum(pm3point)
    evid['PS2score'] = sum(ps2point.astype('float'))
    # evid['PP1score'] = sum(pp1point.astype('float'))
    evid['pubmed'] = pubmedlist[(pubmedlist.pm3_point!='0') | (pubmedlist.ps2_point!='0') | 
                                (pubmedlist.ps3_strength!='Unmet') | ((pubmedlist.pp1_strength!='0') & (pubmedlist.pp1_strength!='Unmet')) | 
                                ((pubmedlist.pp4_strength.notna()) & (pubmedlist.pp4_strength!='Unmet'))].shape[0]

    evid = [str(x) for x in evid.values()]
    return ';'.join(evid)

test_result['evidence_pmc'] = test_result['VCF_COORD'].apply(evidence_data, args = (outputPMC,))
test_result['pmcrelated'] = test_result['evidence_pmc'].map(lambda x:x.split(';')[0])
test_result['pmcpubmed'] = test_result['evidence_pmc'].map(lambda x:x.split(';')[1])
test_result['pmcPM3'] = test_result['evidence_pmc'].map(lambda x:x.split(';')[2])
test_result['pmcPS2'] = test_result['evidence_pmc'].map(lambda x:x.split(';')[3])
test_result['pmcPP4'] = test_result['evidence_pmc'].map(lambda x:x.split(';')[4])
test_result['pmcPP1'] = test_result['evidence_pmc'].map(lambda x:x.split(';')[5])
test_result['pmcPS3'] = test_result['evidence_pmc'].map(lambda x:x.split(';')[6])
test_result['pmcPM3score'] = test_result['evidence_pmc'].map(lambda x:x.split(';')[7])
test_result['pmcPS2score'] = test_result['evidence_pmc'].map(lambda x:x.split(';')[8])
test_result['pmcPP1score'] = test_result['evidence_pmc'].map(lambda x:x.split(';')[9])
test_result = test_result.drop(['evidence_pmc'], axis=1)

test_result['evidence_pmid'] = test_result['VCF_COORD'].apply(evidence_data, args = (outputPMID,))
test_result['pmidrelated'] = test_result['evidence_pmid'].map(lambda x:x.split(';')[0])
test_result['pmidpubmed'] = test_result['evidence_pmid'].map(lambda x:x.split(';')[1])
test_result['pmidPM3'] = test_result['evidence_pmid'].map(lambda x:x.split(';')[2])
test_result['pmidPS2'] = test_result['evidence_pmid'].map(lambda x:x.split(';')[3])
test_result['pmidPP4'] = test_result['evidence_pmid'].map(lambda x:x.split(';')[4])
test_result['pmidPP1'] = test_result['evidence_pmid'].map(lambda x:x.split(';')[5])
test_result['pmidPS3'] = test_result['evidence_pmid'].map(lambda x:x.split(';')[6])
test_result['pmidPM3score'] = test_result['evidence_pmid'].map(lambda x:x.split(';')[7])
test_result['pmidPS2score'] = test_result['evidence_pmid'].map(lambda x:x.split(';')[8])
test_result['pmidPP1score'] = test_result['evidence_pmid'].map(lambda x:x.split(';')[9])
test_result = test_result.drop(['evidence_pmid'], axis=1)

test_result.to_csv('test_result_output.txt', sep='\t', index=0)


