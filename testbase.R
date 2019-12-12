# R 基础
setwd("C:/Users/Yanxinyi/Desktop") 
getwd()

install.packages("reshape2") # get the package "reshape2" installed
remove.packages()            # 卸载包
# install.packages("ggplot2")  # get the package "ggplot2" installed
library("ggplot2")           # load the package "ggplot2"
data(package="ggplot2")      # what datasets are included in the ggplot2
library(help="ggplot2")      # information about ggplot2
detach("package:ggplot2")    # 移除包

# 创建列表
x <- c("welcome", "to", "gene", "my", "friends")
y <- 1:6

# 按照位置向量进行索引
x[1]         # 索取向量的第1个元素
x[1:3]       # 索取向量的前3个元素
x[c(1,3,4)]  # 索取向量的第1、3、4元素
x[-c(1,3,4)] # 索取向量的除1、3、4元素之外的所有元素

# 按照逻辑向量进行索引
y[y>2]	    # 提取向量y中大于2的元素
y[y>2&y<5]	# 提取向量y中大于2并且小于5的元素
y[y!=2]	    # 提取向量y中不等于2的元素

# 向量索引运算：
y[1:3]*2  # 向量索引后获得的仍是向量，可进行向量的运算


# --------------------------------------------------------------
# 数据清洗
# install.packages("dplyr")
library(dplyr)

data(iris)
class(iris)
head(iris)

filter(iris, Sepal.Length > 7)
filter(iris, Sepal.Length > 7 & Sepal.Width>3.0)

select(iris,Sepal.Width,Petal.Length,Species)
select(iris, contains("." ))
select(iris, ends_with("Length")) 
select(iris, starts_with("Sepal")) 
select(iris, Sepal.Length:Petal.Width)  
select(iris, -Species) 

arrange(iris,Sepal.Length) 
arrange(iris,Sepal.Length,desc(Sepal.Width))

mutate(iris, sepal = Sepal.Length + Sepal.Width)

summarise(iris, avg = mean(Sepal.Length))
summarise(group_by(iris,Species),sd=sd(Petal.Width))
iris %>% group_by(Species) %>% summarise(sd=sd(Petal.Width))


# --------------------------------------------------------------
# 数据处理
options(digits=2)
Student <- c( "John Davis", "Angela Williams ", "Bullwinkle Moose", "David Jones", "Janice Markhammer", "Cheryl Cushing", "Reuven Ytzrhak", "Greg Knox", "Joel England", "Mary Rayburn")
Math <- c(502, 600, 412, 358, 495, 512, 410, 625, 573, 522)
Science <- c(95, 99, 80, 82, 75, 85, 80, 95, 89, 86)
English <- c(25, 22, 18, 15, 20, 28, 15, 30, 27, 18)
roster <- data.frame(Student, Math, Science, English, stringsAsFactors=FALSE)
roster

z <- scale(roster[ ,2:4])
score <- apply(z, 1, mean)
roster <- cbind(roster, score)
y <- quantile(score, c(.8, .6, .4, .2))
roster$grade[score >= y[1] ] <- "A"
roster$grade[score < y[1] & score >= y[2] ] <- "B"
roster$grade[score < y[2] & score >= y[3] ] <- "C"
roster$grade[score < y[3] & score >= y[4] ] <- "D"
roster$grade[score < y[4]] <- "F"
roster

name <- strsplit((roster$Student), " ")
lastname <- sapply(name, "[", 2)
firstname <- sapply(name , "[", 1)
# "["是一个可以提取某个对象的一部分的函数, 在这里它是用来提取列表name各成分中的第一个或第二个元素
roster <- cbind(firstname, lastname, roster[, -1])
roster <- roster[order(lastname, firstname), ]
roster
