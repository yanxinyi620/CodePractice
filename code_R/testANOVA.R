data=read.csv('RunWH005878.csv',header = T,stringsAsFactors = F)

x = data$GC_test
y = data$GC_control

# t.test
t.test(x = x, y = y, alternative = c("two.sided"), mu = 0, paired = FALSE, var.equal = FALSE, conf.level = 0.95)
# t.test 等方差配对样本
t.test(x = x, y = y, alternative = c("two.sided"), paired = T, var.equal = T, conf.level = 0.95)

# Performs one- and two-sample Wilcoxon tests on vectors of data; the latter is also known as ‘Mann-Whitney’ test.
# wilcox.test/Mann-Whitney U test
wilcox.test(x = x, y = y, alternative = "two.sided", paired = FALSE, exact = NULL, correct = TRUE, conf.int = F, conf.level = 0.95)
# 配对样本 wilcox.test/Mann-Whitney U test
wilcox.test(x = x, y = y, alternative = "two.sided", paired = T, conf.int = T, conf.level = 0.95)

# install.packages("BSDA")
library("BSDA")
# z.test sigma 值不确定
z.test(x = x, y = y, alternative = "two.sided", mu = 0, sigma.x = sd(x), sigma.y = sd(y), conf.level = 0.95)


# Poisson {stats} 泊松分布系列函数说明
dpois(x, lambda, log = FALSE)
ppois(q, lambda, lower.tail = TRUE, log.p = FALSE)
qpois(p, lambda, lower.tail = TRUE, log.p = FALSE)
rpois(n, lambda)

# dpois 泊松分布中某个值对应的频率，当 lambda 很大时与正态分布相似，lambda为阈值时累积概率 ≈ 0.5
dpois(5, 10, log = FALSE)
sum(dpois(c(0:9), 10, log = FALSE))+0.5*dpois(10, 10, log = FALSE)
sum(dpois(c(0:99), 100, log = FALSE))+0.5*dpois(100, 100, log = FALSE)

# ppois 泊松分布中某个值对应的累积频率，当 lambda 很大时与正态分布相似，ppois(lambda, lambda) ≈ 0.5
ppois(10, 10, lower.tail = TRUE, log.p = FALSE)
ppois(100, 100, lower.tail = TRUE, log.p = FALSE)
sum(dpois(c(0:10), 10, log = FALSE))

# qpois 泊松分布中某个频率对应的频数，与 ppois 功能相反
qpois(0.5, 10, lower.tail = TRUE, log.p = FALSE)
a = qpois(0.5, 10, lower.tail = TRUE, log.p = FALSE)
ppois(a, 10, lower.tail = TRUE, log.p = FALSE)

# rpois 从已知 lambda 的泊松分布中随机生成值，可以用于绘制密度曲线和模拟泊松分布
rpois(10, 10)
hist(rpois(100000, 10000))
plot(density(rpois(100000, 10000)))


# poisson.test 进行泊松检验，分布曲线只与第一个数 lambda 相关，第二个数默认为1
poisson.test(100, 1000, alternative = "greater",conf.level = 0.95)
poisson.test(10, 100, alternative = "greater",conf.level = 0.95)
poisson.test(10, alternative = "greater",conf.level = 0.95)
# 总结：
a = poisson.test(10, 100, alternative = "greater",conf.level = 0.95)
a = a$conf.int[1]
b = poisson.test(10, 10, alternative = "greater",conf.level = 0.95)
b = b$conf.int[1]
b == a*100/10
# 总结：poisson.test ≈ qpois
poisson.test(10, alternative = "greater",conf.level = 0.95)
a = poisson.test(10, alternative = "greater",conf.level = 0.95)
a = floor(a$conf.int[1])
a == qpois(0.05, 10, lower.tail = TRUE, log.p = FALSE)


data <- PlantGrowth
head(data)
group_data <- split(data[,1], data[,2])
unlist(lapply(group_data, function(x){shapiro.test(x)$p.value})) # 正态性检验

library(car)
qqPlot(group_data[[1]])
leveneTest(weight~group, data = data) # 方差齐性检验，使用car包的leveneTest()，可看出，P值大于0.05，满足方差齐性
outlierTest(lm(weight~group, data=data))
summary(aov(weight~group, data = data))

pvalue <- summary(aov(weight~group, data = data))[[1]][,"Pr(>F)"][1]
pvalue

