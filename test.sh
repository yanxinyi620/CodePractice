# 第五步，结果文件整理
# simulate depth to deletion
result='/home/yanxinyi/project/niftypub/nifty_simu/oneTubeBlood/simu0409/data/'
path='/home/yanxinyi/project/niftypub/nifty_simu/oneTubeBlood/simu0409/'
code='/home/yanxinyi/project/niftypub/xhmm/Microdel-HMM_V1.3'
sex='male'

for i in `cat depth01.txt`
do
    for s in `cat sample.txt`
    do
        sample=${s}'_SE35_'${i}'M'
        
        for k in `seq -w 0.01 0.01 0.30`
        do  
            # 新建 xhmm 运行目录
            mkdir -p ${path}/depth_deletion/${s}_${i}_${k}
            mkdir -p ${path}/depth_deletion/${s}_${i}_${k}/HMM.raw.cnv.spot
            cd ${path}/depth_deletion/${s}_${i}_${k}/bin/

            # get cnv
            python3 ${code}/xhmm2cnv.py -i Male -p 0.5 -n 500000 -s Male &&\

            # get chr cnv
            python3 ${code}/xhmm2chr.py -i Male -s Male &&\

            # cnv merge
            python3 ${code}/cnv2merge.py -c Male.result.cnv -l 0.5 &&\

            # cnv anno gene (omim)
            python3 ${code}/cnv2anno.py -c Male.result.cnv.merge -g ${code}/data/omim.dominant.gene.bed -d ${code}/data/disease.bed -p 0.5 -l 3000000 &&\

            # cnv filter
            python3 ${code}/cnv2filter.py  -c Male.result.cnv.merge.anno -l 5000000 &&\

            # chr cnv filter
            python3 ${code}/chr2filter.py  -c sample.filter.cnv -r Male.result.chr.cnv &&\

            # get tail (Male.PCA_normalized.filtered.sample_zscores.RD.txt)
            tail -1 Male.PCA_normalized.filtered.sample_zscores.RD.txt|awk -F '\t' '{for(i=1;i<=NF;i++){a[FNR,i]=$i}}END{for(i=1;i<=NF;i++){for(j=1;j<=FNR;j++){printf a[j,i]"\t"}print ""}}' | sed 's/\t$//'| sed '1d' > zscore_tmp.txt &&\

            # paste chr-strat-end and sample_zscores.RD
            paste ${code}/data/plot.region zscore_tmp.txt > zscore2_tmp.txt &&\

            # get Graph input files
            perl ${code}/hmm_win.pl Male.result.cnv.merge.anno zscore2_tmp.txt hmm1_tmp.txt hmm2_tmp.txt &&\

            # Graph
            perl ${code}/Graph.pl -i hmm1_tmp.txt -o ../HMM.raw.cnv.spot -r hmm2_tmp.txt &
            
            cd ${result}
        done
        wait
    done
    wait
done










cd ${path}/depth_deletion/${s}_${i}_${k}/bin/

# get cnv
python3 ${code}/xhmm2cnv.py -i Male -p 0.5 -n 500000 -s Male &&\

# get chr cnv
python3 ${code}/xhmm2chr.py -i Male -s Male &&\

# cnv merge
python3 ${code}/cnv2merge.py -c Male.result.cnv -l 0.5 &&\

# cnv anno gene (omim)
python3 ${code}/cnv2anno.py -c Male.result.cnv.merge -g ${code}/data/omim.dominant.gene.bed -d ${code}/data/disease.bed -p 0.5 -l 3000000 &&\

# cnv filter
python3 ${code}/cnv2filter.py  -c Male.result.cnv.merge.anno -l 5000000 &&\

# chr cnv filter
python3 ${code}/chr2filter.py  -c sample.filter.cnv -r Male.result.chr.cnv &&\

# get tail (Male.PCA_normalized.filtered.sample_zscores.RD.txt)
tail -1 Male.PCA_normalized.filtered.sample_zscores.RD.txt|awk -F '\t' '{for(i=1;i<=NF;i++){a[FNR,i]=$i}}END{for(i=1;i<=NF;i++){for(j=1;j<=FNR;j++){printf a[j,i]"\t"}print ""}}' | sed 's/\t$//'| sed '1d' > zscore_tmp.txt &&\

# paste chr-strat-end and sample_zscores.RD
paste ${code}/data/plot.region zscore_tmp.txt > zscore2_tmp.txt &&\

# get Graph input files
perl ${code}/hmm_win.pl Male.result.cnv.merge.anno zscore2_tmp.txt hmm1_tmp.txt hmm2_tmp.txt &&\

# Graph
perl ${code}/Graph.pl -i hmm1_tmp.txt -o ../HMM.raw.cnv.spot -r hmm2_tmp.txt &



touch stat_error.txt
for s in `cat sample.txt`
do
    echo $s >> stat_error.txt
    l ext |grep 'ext'|grep $s |wc -l >> stat_error.txt
    l ext |grep 'win'|grep $s |wc -l >> stat_error.txt
    l ext |grep 'stat'|grep $s |wc -l >> stat_error.txt
    echo '' >> stat_error.txt
    l ext |grep 'ext'|grep $s  >> stat_error.txt
    echo '' >> stat_error.txt
    l ext |grep 'win'|grep $s  >> stat_error.txt
    echo '' >> stat_error.txt
    l ext |grep 'stat'|grep $s  >> stat_error.txt
    echo '' >> stat_error.txt
done


touch stat_error.txt
l ext |grep 'ext'|wc -l >> stat_error.txt
l ext |grep 'win'|wc -l >> stat_error.txt
l ext |grep 'stat'|wc -l >> stat_error.txt
echo '' >> stat_error.txt
l ext |grep 'ext' >> stat_error.txt
echo '' >> stat_error.txt
l ext |grep 'win' >> stat_error.txt
echo '' >> stat_error.txt
l ext |grep 'stat' >> stat_error.txt
echo '' >> stat_error.txt




