import numpy as np
import pandas as pd


def grad_desc(X, y, learning_rate=0.01, epochs=1000, eps=0.0000000001, measure='gd'):
    '''
    This funchtion is used to calculate parameters of linear regression by gradient descend method
    :param X:  sample matrix, shape(n_samples, n_features)
    :param y: matrix-like, shape (n_samples, 1)
    :param learning_rate: learning rate, 0.01 by default
    :param epochs: times of iteration, 1000 by default
    :param eps: the small positive number used in Adagrad prevent zero denominator
    :param return: the parameters of linear regression
    :param gd_type: measures to do gradient descend, can choose 'gd' or 'Adagrad'
    '''
    n = X.shape[0] # 样本数量
    dim = X.shape[1] + 1 # 特征数量，+1是因为有常数项
    x = np.concatenate((np.ones([n, 1]), X), axis = 1).astype(float)
    # 同样由于有常数项，x矩阵需要多加一列1
    y = np.matrix(y).reshape(-1, 1).astype(float) # y转化为列向量，方便矩阵运算
    w = np.zeros([dim, 1]) # 初始化参数
    
    ## 常规的梯度下降法
    if measure == 'gd':
        for i in range(epochs):
            loss = np.sum(np.power(np.dot(x, w) - y, 2))/n
            if (i % 100 == 0):
                print(str(i) + ":" + str(loss))
            gradient = 2 * np.dot(x.transpose(), np.dot(x, w) - y)/n
            w = w - learning_rate * gradient
    
    ## Adagrad法
    if measure == 'Adagrad':
        adagrad = np.zeros([dim, 1])
        for i in range(epochs):
            loss = np.sum(np.power(np.dot(x, w) - y, 2))/n
            if (i % 100 == 0):
                print(str(i) + ":" + str(loss))
            gradient = 2 * np.dot(x.transpose(), np.dot(x, w) - y)/n
            adagrad += np.square(gradient)
            w = w - learning_rate * gradient / np.sqrt(adagrad + eps)
    return w


def predict(w, test_X, test_y):
    '''
    This function is use to calculate the MSE of a given linear regression model
    :param w: matrix-like, shape (n_features+1, 1)
    :test_X: test sample matrix, shape(n_samples, n_features)
    :test_y: true targets of test set, matrix-like, shape (n_samples, 1)
    '''
    test_X = np.concatenate((np.ones([test_X.shape[0], 1]), test_X), axis = 1).astype(float)
    test_y = np.matrix(test_y).reshape(-1, 1).astype(float)
    predict_y = np.dot(test_X, w)
    mse = np.sqrt(np.average(np.square(predict_y - test_y)))
    return mse, predict_y


if __name__ == '__main__':
    # 导入deabetes数据集
    from sklearn.datasets import load_diabetes
    from sklearn.utils import shuffle

    diabetes = load_diabetes()
    X = diabetes.data
    y = diabetes.target

    # np.savetxt('c:\\Users\\yanxi\\Desktop\\x.csv', X, delimiter=',', fmt='%f')
    # np.savetxt('c:\\Users\\yanxi\\Desktop\\y.csv', y, delimiter=',', fmt='%d')

    # 划分训练集和测试集
    offset = int(X.shape[0] * 0.9)
    X_train, y_train = X[:offset], y[:offset]
    X_test, y_test = X[offset:], y[offset:]
    y_train = y_train.reshape((-1,1))
    y_test = y_test.reshape((-1,1))
    print('X_train=', X_train.shape)
    print('X_test=', X_test.shape)
    print('y_train=', y_train.shape)
    print('y_test=', y_test.shape)
    
    # 使用grad_desc()函数求解
    w = grad_desc(X_train, y_train, learning_rate=0.03,epochs=10000, measure='gd')
    mse, predict_y = predict(w, X_test, y_test)
    print('使用grad_desc()函数的MSE: ', mse)

    # 利用sklearn的线性回归api来做对比
    import sklearn.linear_model as sl
    import sklearn.metrics as sm
    model = sl.LinearRegression()
    model.fit(X_train, y_train)
    pred_y = model.predict(X_test)
    print('使用sklearn线性模型函数的MSE: ', sm.mean_absolute_error(y_test, pred_y))
