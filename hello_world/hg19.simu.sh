#head -n 56974802 hg19.fa > hg19simuDG.fa
#tail -n 4890262 hg19.fa >> hg19simuDG.fa

art='../art_bin_MountRainier/art_illumina'

# 1) simulation of single-end reads of 35bp with 10X using the built-in combined quality profile, and without Indels
# $art -ss GA1 -i ./hg19simuDG.fa -o ./single_end_com -l 35 -f 0.1 -sam -k 0
#convert an aln file to a bed file
# ../art_bin_MountRainier/aln2bed.pl single_end_com.bed single_end_com.aln

result='simu_result'
mkdir -p $result
cat hg19simuDGctrl.txt|while read sample concentration readnums depth fdepth mdepth
do
    echo $sample $fdepth $mdepth start...
    $art -ss GA1 -i ./hg19simuDG.fa -o ./$result/$sample.f -l 35 -f $fdepth -k 0
    $art -ss GA1 -i ./hg19.fa -o ./$result/$sample.m -l 35 -f $mdepth -k 0
    
    cat ./$result/$sample.f.fq ./$result/$sample.m.fq > ./$result/$sample.fq
    gzip ./$result/$sample.fq
    # rm ./$result/$sample.f.fq ./$result/$sample.m.fq
    
    # ../art_bin_MountRainier/aln2bed.pl ./$result/$sample.bed ./$result/$sample.aln
done
