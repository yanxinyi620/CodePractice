# from sklearn.linear_model import SGDClassifier

import numpy as np
import matplotlib.pyplot as plt

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import accuracy_score


iris = load_iris()

iris_X = iris.data[:100, ]
iris_y = iris.target[:100, ]

X_train, X_test, y_train, y_test = train_test_split(iris_X, iris_y, test_size=0.3)
print(X_train.shape)
print(X_test.shape)

# sklearn
model = LogisticRegression()
model.fit(X_train, y_train)

y_test_pred = model.predict(X_test)
print(accuracy_score(y_test, y_test_pred))

# pred = model.predict_proba(X_test)
# print(pred)

print(model.coef_)
print(model.intercept_)


# SGD (二元)
def sgd(x, y, lr, max_iter):
    """
    sgd 函数, 求w
    :param x: 数据集的x属性list
    :param y: 数据集的y标签list
    :param alpha: 梯度下降学习率
    :param max_iter: 循环次数
    :return: w 随机梯度下降所求系数list
    """

    w = np.random.randn(2)
    _w = np.empty(2, dtype=float)
    _w = w
    
    m = x.shape[0]
    d = w.shape[0]
    cost = 0

    for i in range(max_iter):
        
        for k in range(m):
            for j in range(d):
                _w[j] = _w[j] - lr * (w[0] * x[k][0] + w[1] * x[k][1] - y[k]) * x[k][j]
        
        for j in range(d):
            w[j] = _w[j]
        
        _cost = 0
        for k in range(m):
            _cost += (w[0] * x[k][0] + w[1] * x[k][1] - y[k]) ** 2
        
        _cost = _cost/m
        if abs(cost - _cost) < 0.001:
            break
        cost = _cost
    
    return w


w = sgd(X_train[:,0:2], y_train, lr=0.1, max_iter=10)


