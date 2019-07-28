# head -n 56974802 hg19.fa > hg19simuDG.fa
# tail -n 4890262 hg19.fa >> hg19simuDG.fa


art='../art_bin_MountRainier/art_illumina'
result='simu_result'
# result='simu_ctrl'
mkdir -p $result

cat hg19simuDG.txt|while read sample concentration readnums depth fdepth mdepth
# cat hg19simuDGctrl.txt|while read sample concentration readnums depth fdepth mdepth
do

    echo $sample $fdepth $mdepth start...

    '''
    # 模拟cnv样本 fastq序列
    $art -ss GA1 -i ./hg19simuDG.fa -o ./$result/$sample.f -l 35 -f $fdepth -k 0
    $art -ss GA1 -i ./hg19.fa -o ./$result/$sample.m -l 35 -f $mdepth -k 0
    cat ./$result/$sample.f.fq ./$result/$sample.m.fq > ./$result/$sample.fq
    gzip ./$result/$sample.fq
    # rm ./$result/$sample*.fq ./$result/$sample*.aln
    

    # 模拟样本比对，fastq2sam
    bwa aln -o0 -e10 -i0 -M0 -E4 -O11 -L -t10 -l12 -k2 /home/yanxinyi/project/niftypub/nifty_xhmm/program/index/reference.fa ./$result/$sample.fq.gz >./$result/$sample.sai && \
    bwa samse /home/yanxinyi/project/niftypub/nifty_xhmm/program/index/reference.fa ./$result/$sample.sai ./$result/$sample.fq.gz >./$result/$sample.sam &
    '''

    # sam2ext
    Sam2EXT -i ./$result/$sample.sam -e ./$result/$sample.ext.gz -s ./$result/$sample.stat -W ./$result/$sample.win.gz




done



wait


result='./'
sample='simu_01'
perl /home/yanxinyi/project/niftypub/nifty_xhmm/Microdel_V3.0/statgc.rmdup.pl ./$result/$sample.ext.gz ./$result/
/usr/bin/perl /home/yanxinyi/project/niftypub/nifty_xhmm/Microdel_V3.0/Ratio.Loose.pl -window /home/yanxinyi/project/niftypub/nifty_xhmm/program/window/win.Tags100k.noSlide.Hg19.gz -ext ./$result/$sample.stat.gc -out ./$result/$sample.NIFTY.ratio


result='./'
sample='CL100128470-L01_12'
perl /home/yanxinyi/project/niftypub/nifty_xhmm/Microdel_V3.0/statgc.rmdup.pl ./$result/$sample.ext.gz ./$result/
/usr/bin/perl /home/yanxinyi/project/niftypub/nifty_xhmm/Microdel_V3.0/Ratio.Loose.pl -window /home/yanxinyi/project/niftypub/nifty_xhmm/program/window/win.Tags100k.noSlide.Hg19.gz -ext ./$result/$sample.stat.gc -out ./$result/$sample.NIFTY.ratio


awk '{printf ("%.1f\n",$6)}' $sample.NIFTY.ratio >$sample.male.depth;
sed -i "1i$sample" $sample.male.depth

paste  *.male.depth | trans >male.depth




python /ifs4/B2C_NIFTY/PROJECT/Zebra/Zebra_V2.0/bin/select_unique_reads.py /ifs8/B2C_NIFTY/PROJECT/Zebra/NiftyProd/20180422_RunSZ003783/EXTandSTAT/CL100061666-L01/49/CL100061666-L01_49.sam /ifs8/B2C_NIFTY/PROJECT/Zebra/NiftyProd/20180422_RunSZ003783/EXTandSTAT/CL100061666-L01/49/CL100061666-L01_49.txt
Rscript /ifs4/B2C_NIFTY/PROJECT/Zebra/Zebra_V2.0/bin/SeqFF.R --i=/ifs8/B2C_NIFTY/PROJECT/Zebra/NiftyProd/20180422_RunSZ003783/EXTandSTAT/CL100061666-L01/49 --m=/ifs8/B2C_NIFTY/PROJECT/Zebra/NiftyProd/20180422_RunSZ003783/EXTandSTAT/CL100061666-L01/49/CL100061666-L01_49.txt --d=/ifs8/B2C_NIFTY/PROJECT/Zebra/NiftyProd/20180422_RunSZ003783/EXTandSTAT/CL100061666-L01/49 --o=/ifs8/B2C_NIFTY/PROJECT/Zebra/NiftyProd/20180422_RunSZ003783/EXTandSTAT/CL100061666-L01/49/CL100061666-L01_49.txt.frac --t=sam
python /ifs4/B2C_NIFTY/PROJECT/Zebra/Zebra_V2.0/bin/NIFLM.py -i /ifs8/B2C_NIFTY/PROJECT/Zebra/NiftyProd/20180422_RunSZ003783/EXTandSTAT/CL100061666-L01/49/CL100061666-L01_49.ext.gz -o /ifs8/B2C_NIFTY/PROJECT/Zebra/NiftyProd/20180422_RunSZ003783/EXTandSTAT/CL100061666-L01/49/CL100061666-L01_49.NIFLM.frac
rm /ifs8/B2C_NIFTY/PROJECT/Zebra/NiftyProd/20180422_RunSZ003783/EXTandSTAT/CL100061666-L01/49/CL100061666-L01_49.sai /ifs8/B2C_NIFTY/PROJECT/Zebra/NiftyProd/20180422_RunSZ003783/EXTandSTAT/CL100061666-L01/49/CL100061666-L01_49.sam /ifs8/B2C_NIFTY/PROJECT/Zebra/NiftyProd/20180422_RunSZ003783/EXTandSTAT/CL100061666-L01/49/CL100061666-L01_49.txt





#!/bin/bash

##index='/data/bwa/hg19.fa'
##chrsize='/data/hg19/hg19.chrom.sizes'
##thread=36

#sam flag
#2 - read mapped in proper pair
#524=512,8,4 - read fails platform/vendor quality checks, mate unmapped, read unmapped

mkdir -p seg_len
ls /home/pengjiguang/project/nifty/PE/PE100/CL100036545/fastq/*.fq.gz|sed 's/\/home\/pengjiguang\/project\/nifty\/PE\/PE100\/CL100036545\/fastq\///;s/_[12].fq.gz//'|sort -u|while read sample
do
	echo $sample start...

	samtools view -@4 -f 66 -F 524 -q 60 bam/$sample.bam |perl -lane '{$NM=$1 if /NM:i:(\d+)/;$AS=$1 if /AS:i:(\d+)/;$XS=$1 if /XS:i:(\d+)/;$MD=$1 if /MD:Z:(\w+)/; print join "\t",$F[0],$F[2],$F[3],$F[1],$F[9],$F[8],$MD,$NM,$AS,$XS}'|awk '$6>=-300 && $6<=300 && $8<=2 && $9>=80 && $10<80{print $0}' >seg_len/$sample.seglen&
	bash stats.seglen.sh seg_len/$sample.seglen >seg_len/$sample.seglen.stats&
	#all=`awk '$2<=22||$2=="X"{print$6}' seg_len/$sample.seglen|sed -e's/\-//'g|sta --median --brief`
	#chrY=`grep -w Y seg_len/$sample.seglen|cut -f 6|sed -e's/\-//'g|sta --median --brief`
	#lenSY=`awk '$2=="Y"&&$6<=med&&$6>=-med{print$0}' med=$all seg_len/$sample.seglen|wc -l`
	#lenY=`awk '$2=="Y"{print$0}' seg_len/$sample.seglen|wc -l`
	#fracY=`awk 'BEGIN{printf "%.2f\n",'$lenSY'/'$lenY'}'`
	#echo -e $sample"\t"$all"\t"$chrY"\t"$lenSY"\t"$lenY"\t"$fracY >>seglen.stats
	#/home/pengjiguang/miniconda3/bin/python bam2ext.py seg_len/$sample.seglen seg_len/$sample.seglen.ext seg_len/$sample.seglen.stats &
done



