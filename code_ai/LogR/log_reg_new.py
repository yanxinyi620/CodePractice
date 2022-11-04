import numpy as np
import matplotlib.pyplot as plt

from sklearn.datasets import make_classification, load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression


def classify(h, threshold=0.5):
    h[np.argwhere(h < threshold)] = 0
    h[np.argwhere(h >= threshold)] = 1
    return h


def inference(x, theta):
    if x.ndim == 1:
        x.reshape(1, len(x))
    if theta.ndim == 1:
        theta.reshape(len(theta), 1)
    g = np.matmul(x, theta)
    h = np.divide(np.exp(g), np.exp(g) + 1)
    return h


def eval_loss(x, y, theta):
    if y.ndim == 1:
        y.reshape(1, len(y))
    h = inference(x, theta)
    loss = np.mean(-y * np.log(h) - (1 - y) * np.log(1 - h))
    return loss


def update(x, y, theta, lr):
    if y.ndim == 1:
        y = y.reshape(len(y), 1)
    h = inference(x, theta)
    if x.ndim == 1:
        x.reshape(1, len(x))
    deriv = np.matmul(x.T, h - y) / x.shape[0]
    theta -= lr * deriv
    return theta


def train(x, y, lr, batch_size, max_iter):
    if not isinstance(x, np.ndarray):
        x = np.array(x)
    if not isinstance(y, np.ndarray):
        y = np.array(y)
    n = x.shape[0]
    # theta = np.zeros((x.shape[1], 1))
    theta = np.zeros((x.shape[1] + 1, 1))
    loss_list = []
    for i in range(max_iter):
        idx = np.random.choice(range(n), size=batch_size, replace=False)
        # x_, y_ = x[idx], y[idx]
        b_ = np.ones(batch_size)
        x_, y_ = np.insert(x[idx], x.shape[1], b_, axis=1), y[idx]
        # lr_i = lr / (1 + 0.001*i)
        lr = lr * 0.999
        theta = update(x_, y_, theta, lr)
        loss = eval_loss(x_, y_, theta)
        loss_list.append(loss)
        if i == 0 or (i+1) % 100 == 0:
            # print(f'[iter-{i+1}], w: {[float("%.4f" % i) for i in theta]}, '
            #       f'loss: {"%.8f" % loss}.')
            print(f'[iter-{i+1}], loss: {"%.8f" % loss}.')
        # print(loss)
        # if loss > loss_list[_ - 1]:
        #     break
    return loss_list, theta


def load_dataset(name=None):

    if name == 'iris':
        iris = load_iris()
        iris_X = iris.data[:100, ]
        iris_y = iris.target[:100, ]
        X_train, X_test, y_train, y_test = train_test_split(iris_X, iris_y, test_size=0.3)
        print(X_train.shape)
        print(X_test.shape)
    else:
        sample_size = 2000
        features = 15
        classes = 2
        X, y = make_classification(sample_size, features, n_classes=classes,
                                   n_informative=2, n_redundant=0, n_repeated=0, 
                                   shuffle=True, random_state=100)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
        print(X_train.shape)
        print(X_test.shape)

    return X_train, X_test, y_train, y_test


def main():

    # load dataset
    # X_train, X_test, y_train, y_test = load_dataset(name='iris')
    X_train, X_test, y_train, y_test = load_dataset()

    # Hyper parameters
    lr = 0.01
    batch_size = 50
    max_iters = 10000

    # train model
    train_loss, theta = train(X_train, y_train, lr, batch_size, max_iters)
    
    # predict X_test
    # h = inference(X_test, theta)
    b_ = np.ones(X_test.shape[0])
    h = inference(np.insert(X_test, X_test.shape[1], b_, axis=1), theta)
    y_pred = classify(h, 0.5)
    
    # evaluation
    acc = accuracy_score(y_test, y_pred)
    print(f'accuracy score is: {"%.4f" % acc}!')
    print(f'w: {[float("%.8f" % i) for i in theta]}.')


    if 'plot_loss':
        plt.scatter(range(max_iters), train_loss, s=2, c='r', marker='o')
        plt.show()


    if 'sklearn':
        model = LogisticRegression()
        model.fit(X_train, y_train)

        y_pred = model.predict(X=X_test)
        acc = accuracy_score(y_test, y_pred)
        print(f'accuracy score is: {"%.4f" % acc}!')
        print(f'w: {model.coef_}, b: {model.intercept_}.')

        # theta = model.coef_.reshape(-1, 1)
        # loss = eval_loss(X_train, y_train, theta)
        theta = np.append(model.coef_ , model.intercept_).reshape(-1, 1)
        b_ = np.ones(X_train.shape[0])
        loss = eval_loss(np.insert(X_train, X_train.shape[1], b_, axis=1), y_train, theta)
        print(f'sklearn loss: {loss}.')


if __name__ == "__main__":
    main()
