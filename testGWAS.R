# color theme
VScode color theme

# GWAS 关联分析模拟
# 表型值 = 遗传效应 + 残差效应

# 载入两个数据文件
myGD = read.table(file="http://zzlab.net/GAPIT/data/mdp_numeric.txt",head=T)
myGM = read.table(file="http://zzlab.net/GAPIT/data/mdp_SNP_information.txt",head=T)

# 模拟数据，从snp中随机抽取10个qtn，模拟遗传效应，残差效应，表型值
G2P=function(X,h2,alpha,NQTN,distribution,a2=0){  
  n=nrow(X)
  m=ncol(X)
  QTN.position=sample(m,NQTN,replace=F) 
  SNPQ=as.matrix(X[,QTN.position]) 
  QTN.position
  if(distribution=="normal") 
  {addeffect=rnorm(NQTN,0,1)
  }else
  {addeffect=alpha^(1:NQTN)}
  effect=SNPQ%*%addeffect 
  effectvar=var(effect)
  residualvar=(effectvar-h2*effectvar)/h2
  residual=rnorm(n,0,sqrt(residualvar))
  y=effect+residual
  return(list(addeffect = addeffect, y=y, add = effect, residual = residual, QTN.position=QTN.position, SNPQ=SNPQ))
}

# Sampling QTN
X=myGD[,-1]
set.seed(910817)
mySim=G2P(X,h2=.75,alpha=1,NQTN=10,distribution="norm")
str(mySim)

# 计算表型值与snp间的相关
GWASbyCor=function(X,y){
    n=nrow(X)
    r=cor(y,X) 
    n=nrow(X)
    t=r/sqrt((1-r^2)/(n-2))
    p=2*(1-pt(abs(t),n-2))  
    zeros=p==0 
    p[zeros]=1e-10
    return(p)}

# 计算相关分析的p值，绘制曼哈顿图，标出qtn位置
par(mfrow=c(1,1))
p= GWASbyCor(X=X,y=mySim$y)
color.vector <- rep(c("deepskyblue","orange","forestgreen","indianred3"),10)
m=ncol(X)
plot(t(-log10(p))~seq(1:m),col=color.vector[myGM[,2]])  #绘制散点图（曼哈顿图）
abline(v=mySim$QTN.position, lty = 2, lwd=1.5, col = "black")  #标出qtn位置
#cutoff=quantile(p,0.01,na.rm=T)  #计算p值分布中1%cutoff的p值,0.0002757605
#abline(h=-log10(cutoff),col="red") 
#0.01/length(p)
abline(h=-log10(0.01/length(p)),col="red")  #标出Bonferroni矫正，typeI=0.01的位置


