import pandas as pd

inputfile = 'anno.hgmd.gnomAD.filter.popmax.filter'
# inputfile = 'anno.hgmd.gnomAD.filter.popmax'
anno_hgmd_popmax = pd.read_table(inputfile, header=0, sep='\t', dtype='str')

function_group = 'function_type.txt'
function_group = pd.read_table(function_group, header=0, sep='\t', dtype='str')

anno_hgmd_group = pd.merge(anno_hgmd_popmax, function_group, on='Function', how='left')

anno_hgmd_group['af_filter'] = 'Fail'
anno_hgmd_group.af_filter[(anno_hgmd_group.Exception.notna()) | 
    (anno_hgmd_group.popmax_filter<'0.003') |  (anno_hgmd_group.popmax_filter.isna())] = 'Pass'
anno_hgmd_group.to_csv('anno.hgmd.gnomAD.filter.popmax.group', sep='\t', index=0, na_rep='NA')


anno_hgmd_group_summary = anno_hgmd_group.groupby(['Gene_Symbol', 'SampleID', 'type', 'group', 'af_filter'], as_index=False)['Chr'].count()
anno_hgmd_group_summary.rename(columns={'Chr':'score'}, inplace = True)
anno_hgmd_group_summary.to_csv('anno.hgmd.gnomAD.filter.popmax.summary', sep='\t', index=0, na_rep='NA')

'''
anno_hgmd_group01 = anno_hgmd_group.groupby(['Gene_Symbol', 'SampleID'], as_index=False)['Chr'].count()
anno_hgmd_group01.rename(columns={'Chr':'score'}, inplace = True)
anno_hgmd_group01.score = anno_hgmd_group01.score.astype(int)
anno_hgmd_group01_result = anno_hgmd_group01.pivot(index='Gene_Symbol', columns='SampleID', values='score')
'''

