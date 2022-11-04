## Linear Regression
###############################
import random
import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score


def inference(w, b, x):
    pred_y = w * x + b
    return pred_y


def eval_loss(w, b, x_list, gt_y_list):
    avg_loss = 0.0
    for i in range(len(x_list)):
        avg_loss += 0.5 * (w * x_list[i] + b - gt_y_list[i]) ** 2
    avg_loss /= len(gt_y_list)
    return avg_loss


def gradient(pred_y, gt_y, x):
    diff = pred_y - gt_y
    dw = diff * x
    db = diff
    return dw, db


def cal_step_gradient(batch_x_list, batch_gt_y_list, w, b, lr):
    avg_dw, avg_db = 0, 0
    batch_size = len(batch_x_list)
    for i in range(batch_size):
        pred_y = inference(w, b, batch_x_list[i])
        dw, db = gradient(pred_y, batch_gt_y_list[i], batch_x_list[i])
        avg_dw += dw
        avg_db += db
    avg_dw /= batch_size
    avg_db /= batch_size
    w -= lr * avg_dw
    b -= lr * avg_db
    return w, b


def train(x_list, gt_y_list, batch_size, lr, max_iter):
    w = 0
    b = 0
    loss_list = []
    for i in range(max_iter):
        batch_idxs = np.random.choice(len(x_list), batch_size)
        batch_x = [x_list[j] for j in batch_idxs]
        batch_y = [gt_y_list[j] for j in batch_idxs]
        w, b = cal_step_gradient(batch_x, batch_y, w, b, lr)
        if i == 0 or (i+1) % 100 == 0:
            loss = eval_loss(w, b, x_list, gt_y_list)
            loss_list.append(loss)
            print(f'[iter-{i+1}], w: {"%.4f" % w}, b: {"%.4f" % b}, '
                  f'loss: {"%.8f" % loss}.')
            # if len(loss_list) >= 5 and loss_list[-2] < loss and \
            #     loss_list[-3] < loss and loss_list[-4] < loss:
            #     break
    return w, b, loss_list


def gen_sample_data(num_samples):
    w = random.randint(0, 10) + random.random()	 # for noise random.random[0, 1)
    b = random.randint(0, 5) + random.random()  # for noise random.random[0, 1)
    
    x_list = []
    y_list = []
    for i in range(num_samples):
        x = random.randint(0, 100) * random.random()
        y = w * x + b + random.random() * random.randint(-1, 1)
        x_list.append(x)
        y_list.append(y)
    
    return x_list, y_list, w, b


def run():
    x_list, y_list, w, b = gen_sample_data(num_samples=1000)
    lr = 0.001
    max_iter = 10000
    batch_size = 50
    _w, _b, loss_list = train(x_list, y_list, batch_size, lr, max_iter)
    print(f'true w: {[w]}, true b: {b}.')
    print(f'w: {[_w]}, b: {_b}.')
    
    pred_y = [inference(_w, _b, x) for x in x_list]
    mse = mean_squared_error(y_list, pred_y)
    r2 = r2_score(y_list, pred_y)
    print(f'mse score is: {mse}, r square is: {r2}!')
    

    if 'plot_loss':
        plt.scatter(np.array(range(int(max_iter/100)+1))*100, loss_list, s=3, c='r', marker='o')
        plt.show()


    if 'sklearn':
        model = LinearRegression()
        model.fit(np.array(x_list).reshape(-1, 1), y_list)
        print(f'w: {model.coef_}, b: {model.intercept_}.')

        y_pred = model.predict(X=np.array(x_list).reshape(-1, 1))
        mse = mean_squared_error(y_list, y_pred)
        r2 = r2_score(y_list, y_pred)
        print(f'mse score is: {mse}, r square is: {r2}!')


if __name__ == '__main__':
    run()

