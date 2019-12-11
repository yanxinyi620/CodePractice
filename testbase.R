install.packages("reshape2") # get the package "reshape2" installed
remove.packages()            # 卸载包
install.packages("ggplot2")  # get the package "ggplot2" installed
library("ggplot2")           # load the package "ggplot2"
data(package="ggplot2")      # what datasets are included in the ggplot2
library(help="ggplot2")      # information about ggplot2
detach("package:ggplot2")    # 移除包


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
