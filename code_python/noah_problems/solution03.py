'''
@Author: yanxinyi620@163.com
@Date: 2020-04-18
@Title：Logistic
'''

# Logistic 回归算法（分类问题）
# 根据数据特征，进行分类
# 分类函数： g(z) = 1/(1+e-z) (sigmoid)
# 特征变量： z = w0x0 + w1x1 + ... + wnxn = wTx
# 预测函数： h(z) = hw(x) = 1/(1+e-wTx)
# 利用梯度上升求解：pass

import numpy as np
import matplotlib.pyplot as plt


# sigmoid函数
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

# 初始化数据
def init_data():
    
    data_x1 = [3, 5, 8, 10, 5, 6, 4, 3, 9]
    data_x2 = [0.8, 0.5, 0.2, 0.3, 0.4, 1.3, 0.4, 1.1, 0.8]
    data_y = [0, 0, 1, 1, 1, 0, 0, 0, 1]
    data = np.array([data_x1, data_x2, data_y]).T

    dataMatIn = data[:, 0:-1]
    classLabels = data[:, -1]
    # 特征数据集，添加1构造常数项 x0
    dataMatIn = np.insert(dataMatIn, 0, 1, axis=1)  
    return dataMatIn, classLabels


# 梯度上升
def gradientAscent(dataMatIn, classLabels):
    dataMatrix = np.mat(dataMatIn)
    labelMat = np.mat(classLabels).transpose()
    n = np.shape(dataMatrix)[1]
    weights = np.ones((n, 1))  #初始化回归系数（n, 1)
    alpha = 0.001 #步长
    maxCycle = 2000  #最大循环次数

    for i in range(maxCycle):
        h = sigmoid(dataMatrix * weights)  #sigmoid 函数
        weights = weights + alpha * dataMatrix.transpose() * (labelMat - h)  #梯度
    return weights


# 计算结果绘图
def plotBestFIt(weights):
    dataMatIn, classLabels = init_data()
    n = np.shape(dataMatIn)[0]
    xcord1 = []
    ycord1 = []
    xcord2 = []
    ycord2 = []
    for i in range(n):
        if classLabels[i] == 1:
            xcord1.append(dataMatIn[i][1])
            ycord1.append(dataMatIn[i][2])
        else:
            xcord2.append(dataMatIn[i][1])
            ycord2.append(dataMatIn[i][2])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xcord1, ycord1,s=30, c='red', marker='s')
    ax.scatter(xcord2, ycord2, s=30, c='green')
    x = np.arange(3, 10, 0.1)
    y = (-weights[0, 0] - weights[1, 0] * x) / weights[2, 0]  #matix
    ax.plot(x, y)
    plt.xlabel('X1')
    plt.ylabel('X2')
    plt.show()


# 计算结果
if __name__ == '__main__':
    dataMatIn, classLabels = init_data()
    r = gradientAscent(dataMatIn, classLabels)
    print(r)
    plotBestFIt(r)


