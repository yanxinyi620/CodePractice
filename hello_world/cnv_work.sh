path='/home/yanxinyi/project/niftypub/nifty_xhmm/code/'
run1='/home/zhangshaojie/zhangsj/nifty/shanghai/depth_1.6/mm'
run2='/home/zhangshaojie/zhangsj/nifty/shanghai/depth_1.6/ww'

# get cnv result
/home/pengjiguang/miniconda3/bin/python ${path}xhmm.new.py -i $run1 -p 0.5 -n 500000
/home/pengjiguang/miniconda3/bin/python ${path}xhmm.new.py -i $run2 -p 0.5 -n 500000

# select sample
cat *.result.txt |awk '$4~"CL100125020"||$4~"CL100125106"{print$0}' > cnvresult.bed

# array to bed
/home/pengjiguang/miniconda3/bin/python ${path}array2bed.py ${path}array.txt >arraycnv.bed

# merge cnv
# /home/pengjiguang/miniconda3/bin/python ${path}cnv_merge.py -c cnvresult.bed -l 5000000
/home/pengjiguang/miniconda3/bin/python ${path}cnv_merge.py -c cnvresult.bed -l 0.1

# cnv list get gene and disease
/home/pengjiguang/miniconda3/bin/python ${path}cnv2genedisease.py -c cnvresult.bed.merge -g ${path}omim.dominant.gene.bed -d ${path}disease.bed
/home/pengjiguang/miniconda3/bin/python ${path}cnv2genedisease.py -c arraycnv.bed -g ${path}omim.dominant.gene.bed -d ${path}disease.bed

# cnv and arraycnv.bed mastch
/home/pengjiguang/miniconda3/bin/python ${path}get_cnv.py -c cnvresult.bed.merge.disease.gene.txt -a arraycnv.bed.disease.gene.txt
/home/pengjiguang/miniconda3/bin/python ${path}get_cnv.py -c arraycnv.bed.disease.gene.txt -a cnvresult.bed.merge.disease.gene.txt
