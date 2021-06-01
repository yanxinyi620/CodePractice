# 第四步， 模拟 depth deletion 数据
# simulate depth to deletion
result='/home/yanxinyi/project/niftypub/nifty_simu/oneTubeBlood/simu0409/data/'
path='/home/yanxinyi/project/niftypub/nifty_simu/oneTubeBlood/simu0409/'
code='/home/yanxinyi/project/niftypub/xhmm/Microdel-HMM_V1.3'
sex='male'

for i in `cat depth02.txt`
do
    for s in `cat sample02.txt`
    do
        sample=${s}'_SE35_'${i}'M'
        
        for k in `seq -w 0.01 0.01 0.30`
        do  
            # 新建 xhmm 运行目录
            mkdir -p ${path}/depth_deletion/${s}_${i}_${k}
            mkdir -p ${path}/depth_deletion/${s}_${i}_${k}/bin
            cd ${path}/depth_deletion/${s}_${i}_${k}
            
            # 模拟疾病 #可以把浓度模拟放在python 减少数据读取次数
            /home/pengjiguang/miniconda3/bin/python $result/simu_depth_disease.py $result/depth/$sample.$sex.depth $result/disease.bed Male.depth $k &&\
            
            # xhmm 核心步骤（中心化、PCA、XHMM）
            # xhmm.pl
            perl ${code}/xhmm.pl ${path}/depth_deletion/${s}_${i}_${k} Male &&\
            rm ${path}/depth_deletion/${s}_${i}_${k}/bin/Male*RD* &&\
            rm ${path}/depth_deletion/${s}_${i}_${k}/bin/*PCA* &

            cd ${result}
        done
        wait
        echo 'finished ' $i ' ' $sample ' at ' $(date "+%Y-%m-%d %H:%M:%S")
    done
    wait
done


# 第四步， 模拟 depth deletion 数据
# simulate depth to deletion
result='/home/yanxinyi/project/niftypub/nifty_simu/oneTubeBlood/simu0409/data/'
path='/home/yanxinyi/project/niftypub/nifty_simu/oneTubeBlood/simu0409/'
code='/home/yanxinyi/project/niftypub/xhmm/Microdel-HMM_V1.3'
sex='male'

for i in `cat depth.txt`
do
    for s in `cat sample.txt`
    do
        sample=${s}'_SE35_'${i}'M'
        
        for k in `seq -w 0.01 0.01 0.30`
        do  
            # 新建 xhmm 运行目录
            mkdir -p ${path}/depth_deletion/${s}_${i}_${k}
            mkdir -p ${path}/depth_deletion/${s}_${i}_${k}/bin
            cd ${path}/depth_deletion/${s}_${i}_${k}
            
            # 模拟疾病 #可以把浓度模拟放在python 减少数据读取次数
            /home/pengjiguang/miniconda3/bin/python $result/simu_depth_disease.py $result/depth/$sample.$sex.depth $result/disease.bed Male.depth $k &&\
            
            # xhmm 核心步骤（中心化、PCA、XHMM）
            # xhmm.pl
            perl ${code}/xhmm.pl ${path}/depth_deletion/${s}_${i}_${k} Male &&\
            rm ${path}/depth_deletion/${s}_${i}_${k}/bin/Male*RD* &&\
            rm ${path}/depth_deletion/${s}_${i}_${k}/bin/*PCA* &

            cd ${result}
        done
        wait
        echo 'finished ' $i ' ' $sample ' at ' $(date "+%Y-%m-%d %H:%M:%S")
    done
    wait
done



# 第五步， 结果处理
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
            mkdir -p ${path}/depth_deletion/${s}_${i}_${k}/bin
            cd ${path}/depth_deletion/${s}_${i}_${k}/bin
            
            # xhmm2cnv
            python3 



            cd ${result}
        done
        wait
        echo 'finished ' $i ' ' $sample ' at ' $(date "+%Y-%m-%d %H:%M:%S")
    done
    wait
done





