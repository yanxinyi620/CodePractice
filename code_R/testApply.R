# apply 系列
# apply，lapply，sapply，tapply


data <- data.frame(V1=1:10,V2=2:11)

rowSums(data) # 向量化函数

apply(data,1,sum)

result = c()
for(i in seq(nrow(data))){
  result = c(result, c(data[i, 1] + data[i, 2]))
}


# 求平方和 （apply 自定义函数）
myFun <- function(x) sum(x^2)
apply(data, 1, myFun)

result = c()
for(i in seq(nrow(data))){
  result = c(result, c(data[i, 1]*data[i, 1] + data[i, 2]*data[i, 2]))
}



# merge 函数
id1 <- c(2, 3, 4, 5, 7)
heights <- c(62, 65, 71, 71, 67)
df1 <- data.frame(id = id1, heights)

id2 <- c(1, 2, 6:10)
weights <- c(147, 113, 168, 135, 142, 159, 160)
df2 <- data.frame(id = id2, weights)

df1
df2

merge(df1, df2, all = FALSE)
merge(df1, df2, all = TRUE)

intersect(df1$id, df2$id)



