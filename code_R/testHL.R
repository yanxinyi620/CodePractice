#-------------------------------------------分析----------------------------------------------
data1tmp=read.csv("data1.csv",header = TRUE, sep = ",",quote = "\"",dec = ".",fill = TRUE,stringsAsFactors=F,comment.char="")
cname1=colnames(data1tmp)
data1=data1tmp
colnames(data1)=paste('v',seq(1,129),sep='')
data1[data1$v123=='Inconclusive' & nchar(data1$v121)>4,122]='mult_heter'

datatmp=data1[!is.na(data1$v126) & data1$v126=='发病',] #需要处理完分组以后在运行这一步
#analysis
#按基因型类型分组统计首次确诊日龄的数据量、中位数、均值、标准差（不统计无确诊记录的样本）
summarise(data1[!is.na(data1[,50]),],n=n(),med=median(v50),mean=mean(v50),sd=sd(v50),min=min(v50),max=max(v50),q1=quantile(v50,probs=0.25),q3=quantile(v50,probs=0.75))
# 仅统计发病且基因型非正常的病例
summarise(data1[!is.na(data1[,50]) & !is.na(data1$v126) & data1$v126=='发病' & data1$v123!='正常',],n=n(),med=median(v50),mean=mean(v50),sd=sd(v50),min=min(v50),max=max(v50),q1=quantile(v50,probs=0.25),q3=quantile(v50,probs=0.75))
summarise(group_by(data1[!is.na(data1[,50]),],v123),n=n(),med=median(v50),mean=mean(v50),sd=sd(v50),min=min(v50),max=max(v50),q1=quantile(v50,probs=0.25),q3=quantile(v50,probs=0.75))
# 仅统计发病病例
summarise(group_by(data1[!is.na(data1[,50]) & !is.na(data1$v126) & data1$v126=='发病',],v123),n=n(),med=median(v50),mean=mean(v50),sd=sd(v50),min=min(v50),max=max(v50),q1=quantile(v50,probs=0.25),q3=quantile(v50,probs=0.75))
#按基因型类型分组统计截止2018-7-31日时的日龄
summarise(data1[!is.na(data1[,12]),],n=n(),med=median(v129),mean=mean(v129),sd=sd(v129),min=min(v129),max=max(v129),q1=quantile(v129,probs=0.25),q3=quantile(v129,probs=0.75))
summarise(group_by(data1[!is.na(data1[,12]),],v123),n=n(),med=median(v129),mean=mean(v129),sd=sd(v129),min=min(v129),max=max(v129),q1=quantile(v129,probs=0.25),q3=quantile(v129,probs=0.75))
data1[data1$v129<=378,129]=1
data1[data1$v129<=554 & data1$v129>378,129]=2
data1[data1$v129<=745 & data1$v129>554,129]=3
data1[data1$v129>745,129]=4
#data1[,129]=ceiling(data1[,129]/90) #按照90天划分阶段
#按照基因类型计算发病率
result1=fb_stat(data1,123)

#分维度统计数量
summarise(group_by(data1,v123),n=n(),sum=sum(v127)/(1000*30))
summarise(group_by(datatmp,v123),n=n())
#统计不同阶段的1000person-month
d=540
data11=data1[data1$v127>d-90,]
data12=data11[!is.na(data11$v126) & data11$v126=='发病' & data11$v127<=d,]
data11[data11$v127>d,127]=d
data11$v127=data11$v127-d+90
summarise(group_by(data11,v123),n=n(),sum=sum(v127)/(1000*30))
summarise(group_by(data12,v123),n=n())
#年龄分组
summarise(group_by(data1,v129,v123),n=n(),sum=sum(v127)/(1000*30))
summarise(group_by(datatmp,v129,v123),n=n())
#年龄需要进行wilcox.test检验
#性别
summarise(group_by(data1,v17,v123),n=n(),sum=sum(v127)/(1000*30))
summarise(group_by(datatmp,v17,v123),n=n())
chisq.test(matrix(summarise(group_by(data1,v17,v123),n=n(),sum=sum(v127)/(1000*30))$n[c(1,5,2,6,3,7,4,8)],ncol=4))
#民族
summarise(group_by(data1,v7,v123),n=n(),sum=sum(v127)/(1000*30))
summarise(group_by(datatmp,v7,v123),n=n())
chisq.test(matrix(summarise(group_by(data1,v7,v123),n=n(),sum=sum(v127)/(1000*30))$n[c(1,5,2,6,3,7,4,8)],ncol=4))
chisq.test(matrix(c(71,12898,570,225946,0,12,0,139)[c(1,5,2,6,3,7,4,8)],ncol=4))
fisher.test(matrix(c(71,12898,570,225946,0,12,0,139)[c(1,5,2,6,3,7,4,8)],ncol=4),workspace = 2000000)
#分娩方式
data1[data1$v14!='自然产' & data1$v14!='剖宫产',14]='del3'
summarise(group_by(data1,v14,v123),n=n(),sum=sum(v127)/(1000*30))
summarise(group_by(datatmp,v14,v123),n=n())
chisq.test(matrix(summarise(group_by(data1,v14,v123),n=n(),sum=sum(v127)/(1000*30))$n[c(1,5,9,2,6,10,3,7,11,4,8,12)],ncol=4))
fisher.test(matrix(summarise(group_by(data1,v14,v123),n=n(),sum=sum(v127)/(1000*30))$n[c(1,5,9,2,6,10,3,7,11,4,8,12)],ncol=4),workspace = 2000000,simulate.p.value = TRUE)
#孕周
data1[data1$v63<37,63]='36'
data1[data1$v63>=37 & data1$v63<=38,63]='37'
data1[data1$v63>=39 & data1$v63<=40,63]='39'
data1[data1$v63>=41 & data1$v63<=41,63]='41'
data1[data1$v63>41,63]='42'
summarise(group_by(data1,v63,v123),n=n(),sum=sum(v127)/(1000*30))
summarise(group_by(datatmp,v63,v123),n=n())
chisq.test(matrix(c(summarise(group_by(data1,v63,v123),n=n(),sum=sum(v127)/(1000*30))$n[c(1,5,9,13,17,2,6,10,14,18,3,7,11,15)],0,5630,52412,155101,12216,726),ncol=4))
fisher.test(matrix(c(summarise(group_by(data1,v63,v123),n=n(),sum=sum(v127)/(1000*30))$n[c(1,5,9,13,17,2,6,10,14,18,3,7,11,15)],0,5630,52412,155101,12216,726),ncol=4),workspace = 2000000,simulate.p.value = TRUE)
#tmp1=summarise(group_by(data1,v63,v123),n=n())
#write.csv(tmp1,'tmp1.csv',quote=FALSE,row.names=FALSE)
#体重
data1[data1$v13<2500,13]='2499'
data1[data1$v13>=2500 & data1$v13<=4000,13]='2500'
data1[data1$v13>4000,13]='4001'
summarise(group_by(data1,v13,v123),n=n(),sum=sum(v127)/(1000*30))
summarise(group_by(datatmp,v13,v123),n=n())
fisher.test(matrix(summarise(group_by(data1,v13,v123),n=n(),sum=sum(v127)/(1000*30))$n[c(1,5,9,2,6,10,3,7,11,4,8,12)],ncol=4),workspace = 2000000,simulate.p.value = TRUE)
#tmp2=summarise(group_by(data1,v13,v123),n=n())
#write.csv(tmp2,'tmp2.csv',quote=FALSE,row.names=FALSE)
#高危因素
data1[data1$v16!='新生儿重症监护室住院超过24小时' & !is.na(data1$v16),16]='risk3'
data1[is.na(data1$v16),16]='risk1'
summarise(group_by(data1,v16,v123),n=n(),sum=sum(v127)/(1000*30))
summarise(group_by(datatmp,v16,v123),n=n())
fisher.test(matrix(c(557,12660,70,221417,3,5,0,44,10,245,1,4624)[c(1,5,9,2,6,10,3,7,11,4,8,12)],ncol=4),workspace = 2000000,simulate.p.value = TRUE)
#初筛
data1[data1$v21=='通过',21]='pass'
data1[data1$v21=='未通过',21]='nopass'
summarise(group_by(data1,v21,v123),n=n(),sum=sum(v127)/(1000*30))
summarise(group_by(datatmp,v21,v123),n=n())
chisq.test(matrix(summarise(group_by(data1,v21,v123),n=n(),sum=sum(v127)/(1000*30))$n[c(1,5,2,6,3,7,4,8)],ncol=4))
#传统方法
data1[((!is.na(data1[,21]) & data1$v21=='pass') | (!is.na(data1[,31]) & data1$v31=='通过')),61]='pass'
data1[!((!is.na(data1[,21]) & data1$v21=='pass') | (!is.na(data1[,31]) & data1$v31=='通过')),61]='notpass'
summarise(group_by(data1,v61,v123),n=n(),sum=sum(v127)/(1000*30))
summarise(group_by(datatmp,v61,v123),n=n())
chisq.test(matrix(summarise(group_by(data1,v61,v123),n=n(),sum=sum(v127)/(1000*30))$n[c(1,5,2,6,3,7,4,8)],ncol=4))
#GJB2/SLC26A4的Positive/Inconclusive
datatt=data1[(data1$v123=='Positive' | data1$v123=='Inconclusive') & (substr(data1$v122,0,4)=='GJB2' | substr(data1$v122,0,4)=='SLC2'),]
datatt$v122=substr(datatt$v122,0,4)
summarise(group_by(datatt,v122,v123),n=n(),sum=sum(v127)/(1000*30))
summarise(group_by(datatt[!is.na(datatt$v126) & datatt$v126=='发病',],v122,v123),n=n())
chisq.test(matrix(summarise(group_by(datatt,v122,v123),n=n(),sum=sum(v127)/(1000*30))$n[c(1,5,2,6,3,7,4,8)],ncol=4))

#HL
summarise(group_by(data1,v126,v123),n=n())
summarise(group_by(data1[data1$v127<=90,],v126,v123),n=n())
as.matrix(summarise(group_by(data1,v17,v126,v123),n=n()))
#Turnround time
summarise(group_by(data1,''),n=n(),med=median(v125-v124),mean=mean(v125-v124),sd=sd(v125-v124),min=min(v125-v124),max=max(v125-v124),q1=quantile((v125-v124),probs=0.25),q3=quantile((v125-v124),probs=0.75))
summarise(group_by(data1,''),n=n(),med=median(v125-v124),mean=mean(v125-v124),sd=sd(v125-v124),min=min(v125-v124),max=max(v125-v124))
summarise(group_by(data1,v123),n=n(),med=median(v125-v124),mean=mean(v125-v124),sd=sd(v125-v124),min=min(v125-v124),max=max(v125-v124))
summarise(group_by(data1,year(v12)),n=n(),med=median(v125-v124),mean=mean(v125-v124),sd=sd(v125-v124),min=min(v125-v124),max=max(v125-v124))
summarise(group_by(data1,year(v12),v123),n=n(),med=median(v125-v124),mean=mean(v125-v124),sd=sd(v125-v124),min=min(v125-v124),max=max(v125-v124))
#加入AABR检查后通过率及各维度统计数据
summarise(group_by(data1,v123,v89),n=n())
a=as.matrix(summarise(group_by(data1,v21,v31,v41,v126,v123,v89),n=n()))

#初筛FLU计算
days0=180
lfu1_1=summarise(group_by(data1[data1$v21=='nopass',],v123),n=n())
lfu1_2=summarise(group_by(data1[data1$v21=='nopass' & (is.na(data1[,31]) | data1$v40>days0) & (is.na(data1[,41]) | data1$v50>days0) & (is.na(data1[,89]) | data1$v91>days0),],v123),n=n())
lfu1=cbind(lfu1_1,lfu1_2[,2],flu1=paste(as.matrix(round(lfu1_2[,2]/lfu1_1[,2]*100,2)),'%',sep=''))
lfu1
#复筛FLU计算OAE/AABR
days0=180
summarise(group_by(data1[(!is.na(data1$v31) & data1$v31!='复筛' & data1$v40<=days0) | (!is.na(data1$v89) & data1$v91<=days0),],v123),n=n()) #180天内做了复筛的人数
lfu10_1=summarise(group_by(data1[(!is.na(data1[,31]) & (data1$v31=='未通过' & data1$v40<=days0)) | (!is.na(data1[,89]) & (data1$v89=='确诊异常' & data1$v91<=days0)),],v123),n=n()) #180天内做了OAE复筛的未通过或者AABR确诊异常的人数
lfu10_2=summarise(group_by(data1[((!is.na(data1[,31]) & (data1$v31=='未通过' & data1$v40<=days0)) | (!is.na(data1[,89]) & (data1$v89=='确诊异常' & data1$v91<=days0))) & (is.na(data1[,41]) | data1$v50>days0),],v123),n=n()) #180天内做了OAE复筛的未通过或者AABR确诊异常的人群中，未做确诊的人数
lfu10=cbind(lfu10_1,lfu10_2[,2],flu1=paste(as.matrix(round(lfu10_2[,2]/lfu10_1[,2]*100,2)),'%',sep=''))
lfu10

#初筛、复筛OAE/AABR通过情况,传统方法通过情况（不限制时间段）
summarise(group_by(data1[!is.na(data1[,21]),],v123),n=n()) #初筛OAE
summarise(group_by(data1[!is.na(data1[,21]) & data1$v21=='通过',],v123),n=n()) #初筛OAE，通过的数量
summarise(group_by(data1[!is.na(data1[,31]),],v123),n=n()) #复筛OAE
summarise(group_by(data1[!is.na(data1[,31]) & data1$v31=='通过',],v123),n=n()) #复筛OAE，通过的数量
summarise(group_by(data1[!is.na(data1$v31) | !is.na(data1$v89),],v123),n=n()) #复筛OAE/AABR
summarise(group_by(data1[(!is.na(data1$v31) & data1$v31=='通过' & (is.na(data1$v89) | data1$v89=='确诊正常')) | ((is.na(data1$v31) | data1$v31=='通过') & !is.na(data1$v89) & data1$v89=='确诊正常'),],v123),n=n()) #复筛OAE/AABR，通过的数量
#通过传统方法的人数
summarise(group_by(data1[(!is.na(data1[,21]) & data1$v21=='通过') | (!is.na(data1[,31]) & data1$v31=='通过'),],v123),n=n()) #初筛通过/复筛通过

#发病人群，通过初筛OAE、复筛OAE/AABR的人数
summarise(group_by(data1[(!is.na(data1[,126]) & data1$v126=='发病'),],v123),n=n()) #发病人数
summarise(group_by(data1[(!is.na(data1[,126]) & data1$v126=='发病' & data1$v127<=90),],v123),n=n()) #90天内发病的人数
summarise(group_by(data1[(!is.na(data1[,126]) & data1$v126=='发病' & data1$v127<=180),],v123),n=n()) #180天内发病的人数
summarise(group_by(data1[(!is.na(data1[,126]) & data1$v126=='发病' & data1$v127<=360),],v123),n=n()) #360天内发病的人数
summarise(group_by(data1[!is.na(data1[,21]) & data1$v21=='通过' & (!is.na(data1[,126]) & data1$v126=='发病'),],v123),n=n()) #初筛通过的发病人数
days0=9999
summarise(group_by(data1[((is.na(data1[,31]) | (data1$v31=='通过' & data1$v40<=days0)) & (is.na(data1[,89]) | (data1$v89=='确诊正常' & data1$v91<=days0))) & (!is.na(data1[,31]) | !is.na(data1[,89])) & (!is.na(data1[,126]) & data1$v126=='发病'),],v123),n=n()) #复筛OAE/AABR通过的发病人数
#通过传统方法且确诊发病的人数
summarise(group_by(data1[((!is.na(data1[,21]) & data1$v21=='通过') | (!is.na(data1[,31]) & data1$v31=='通过')) & (!is.na(data1[,126]) & data1$v126=='发病'),],v123),n=n()) #初筛通过/复筛通过,发病;

#漏检数：通过传统方法且确诊发病的人数+传统方法未检出，基因检出的人数（基因Positive/atrisk）
#1.初筛通过,发病/基因Positive/atrisk；2.初筛未通过，复筛通过，发病/基因Positive/atrisk；3.初筛未通过，复筛NA/不通过，确诊NA/未发病，基因Positive/atrisk
#分成下面三组求和：
#初筛通过/复筛通过 且 基因!='正常',发病;
#summarise(group_by(data1[((!is.na(data1[,21]) & data1$v21=='通过') | (!is.na(data1[,31]) & data1$v31=='通过')) & (!is.na(data1[,126]) & data1$v126=='发病') & data1$v123!='正常',],v123),n=n()) 
#初筛通过/复筛通过 且 基因!='正常',发病,去掉Inconclusive中AABR正常的部分;
summarise(group_by(data1[((!is.na(data1[,21]) & data1$v21=='通过') | (!is.na(data1[,31]) & data1$v31=='通过')) & (!is.na(data1[,126]) & data1$v126=='发病') & data1$v123!='正常' & !(!is.na(data1$v89) & data1$v89=='确诊正常' & data1$v123=='Inconclusive'),],v123),n=n()) 
summarise(group_by(data1[((!is.na(data1[,21]) & data1$v21=='通过') | (!is.na(data1[,31]) & data1$v31=='通过')) & (is.na(data1[,126]) | data1$v126=='不发病') & (data1$v123=='Positive' | data1$v123=='atrisk'),],v123),n=n()) #初筛通过/复筛通过 & NA/不发病 & 基因Positive/atrisk;（1+2）
summarise(group_by(data1[data1$v21=='未通过' & (is.na(data1[,31]) | data1$v31!='通过') & (is.na(data1[,126]) | data1$v126=='不发病') & (data1$v123=='Positive' | data1$v123=='atrisk'),],v123),n=n()) #初筛不通过&复筛NA/不通过&确诊NA/不发病&基因positive/atrisk（3）
#增加一类，发病人中，初筛未通过，没有做复筛，最终发病
summarise(group_by(data1[((!is.na(data1[,21]) & data1$v21=='未通过') & (is.na(data1[,31]) | data1$v31=='复筛')) & (!is.na(data1[,126]) & data1$v126=='发病') & data1$v123=='Positive',],v123),n=n()) #初筛未通过 且 无复筛 且 基因Positive,发病;

#table3
#True positive：初筛不通过，确诊为听力异常的人数（发病人数）；
summarise(group_by(data1[!is.na(data1[,21]) & data1$v21=='未通过' & (!is.na(data1[,126]) & data1$v126=='发病'),],v123),n=n())
#Ture negative：初筛通过，确诊为听力正常的人数（正常人数）；
summarise(group_by(data1[!is.na(data1[,21]) & data1$v21=='通过' & (!is.na(data1[,126]) & data1$v126=='不发病'),],v123),n=n())
#False positive：初筛不通过，后续确诊为正常的，即为假阳性
summarise(group_by(data1[!is.na(data1[,21]) & data1$v21=='未通过' & (!is.na(data1[,126]) & data1$v126=='不发病'),],v123),n=n())
#False negative：初筛通过，后续发展为耳聋的，即为假阴性（漏检）"
summarise(group_by(data1[!is.na(data1[,21]) & data1$v21=='通过' & (!is.na(data1[,126]) & data1$v126=='发病'),],v123),n=n()) 

#tableS2
data10=data1
data10$v122=substr(data10$v122,1,4)
summarise(group_by(data10[(!is.na(data10[,126]) & data10$v126=='发病') & data10$v123=='Positive',],v123,v122),n=n()) #发病人数
summarise(group_by(data10[(!is.na(data10[,126])) & data10$v123=='Positive',],v123,v122),n=n()) #总人数
summarise(group_by(data10[data10$v123=='Positive',],v123,v122),n=n()) #总人数
days0=360
summarise(group_by(data10[(!is.na(data10[,126]) & data10$v126=='发病' & data10$v127<=days0) & data10$v123=='Positive',],v123,v122),n=n())

summarise(group_by(data10[(!is.na(data10[,126]) & data10$v126=='发病') & data10$v123=='Inconclusive',],v123,v122),n=n()) #发病人数
summarise(group_by(data10[(!is.na(data10[,126])) & data10$v123=='Inconclusive',],v123,v122),n=n()) #总人数
summarise(group_by(data10[data10$v123=='Inconclusive',],v123,v122),n=n()) #总人数
days0=360
summarise(group_by(data10[(!is.na(data10[,126]) & data10$v126=='发病' & data10$v127<=days0) & data10$v123=='Inconclusive',],v123,v122),n=n())