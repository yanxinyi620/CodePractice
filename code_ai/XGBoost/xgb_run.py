import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import xgboost as xgb
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# 生成模拟数据集
data_start_time = time.time()
data_size = 1000000
feature_dim = 1000
X = np.random.rand(data_size, feature_dim)
y = np.random.randint(2, size=data_size)

'''
import sys
sys.getsizeof(X)
np.savetxt('X_100w_1000.csv', X, delimiter=',')

# 100w*1000维, 10亿浮点数, float64占据8字节(64位), 总计占用内存8G
# 保存维csv文件后, 默认fmt: str = '%.18e', 大约24位有效数字, 占用存储23G
'''

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
data_end_time = time.time()

# LGBMClassifier ---------------------------------------------
# 创建LGBMClassifier对象
model = lgb.LGBMClassifier(objective='binary', metric='binary_logloss', num_leaves=31, learning_rate=0.05, feature_fraction=0.9)

# 记录开始时间
start_time = time.time()

# 训练模型
train_start_time = time.time()
model.fit(X_train, y_train)
train_end_time = time.time()

# 预测测试集
predict_start_time = time.time()
y_pred = model.predict(X_test)
predict_end_time = time.time()

# 评估模型准确性
accuracy = accuracy_score(y_test, y_pred)
evaluation_end_time = time.time()

# 计算各阶段耗时
data_generation_time = data_end_time - data_start_time
training_time = train_end_time - train_start_time
prediction_time = predict_end_time - predict_start_time
evaluation_time = evaluation_end_time - predict_end_time
total_time = evaluation_end_time - start_time

# 打印结果
print(f"Data generation time: {data_generation_time:.2f} seconds")
print(f"Training time: {training_time:.2f} seconds")
print(f"Prediction time: {prediction_time:.2f} seconds")
print(f"Evaluation time: {evaluation_time:.2f} seconds")
print(f"Total time: {total_time:.2f} seconds")
print(f"Accuracy: {accuracy:.4f}")

'''
Data generation time: 6.12 seconds
Training time: 38.23 seconds
Prediction time: 0.17 seconds
Evaluation time: 0.02 seconds
Total time: 38.42 seconds
Accuracy: 0.4999
'''

# 获取模型参数
model_params = model.get_params()

# 输出模型参数
print("Model Parameters:")
for param, value in model_params.items():
    print(f"{param}: {value}")

# 获取模型信息
num_trees = model.booster_.num_trees()
tree_df = pd.DataFrame(model.booster_.trees_to_dataframe())

# 输出模型信息
print(f"Number of trees: {num_trees}")
print("Tree information:")
print(tree_df)

# 可视化每棵树的结构
lgb.plot_tree(model, tree_index=0, figsize=(20, 10), show_info=['split_gain'])
plt.show()


# XGBClassifier ---------------------------------------------
# 创建XGBoost分类器对象
model_xgb = xgb.XGBClassifier(objective='binary:logistic', learning_rate=0.05, max_depth=6, n_estimators=100)

# 记录开始时间
start_time = time.time()

# 训练模型
train_start_time = time.time()
model_xgb.fit(X_train, y_train)
train_end_time = time.time()

# 预测测试集
predict_start_time = time.time()
y_pred = model_xgb.predict(X_test)
predict_end_time = time.time()

# 评估模型准确性
accuracy = accuracy_score(y_test, y_pred)
evaluation_end_time = time.time()

# 计算各阶段耗时
training_time = train_end_time - train_start_time
prediction_time = predict_end_time - predict_start_time
evaluation_time = evaluation_end_time - predict_end_time
total_time = evaluation_end_time - start_time

# 打印结果
print(f"Training time: {training_time:.2f} seconds")
print(f"Prediction time: {prediction_time:.2f} seconds")
print(f"Evaluation time: {evaluation_time:.2f} seconds")
print(f"Total time: {total_time:.2f} seconds")
print(f"Accuracy: {accuracy:.4f}")

'''
Training time: 129.10 seconds
Prediction time: 0.31 seconds
Evaluation time: 0.01 seconds
Total time: 129.42 seconds
Accuracy: 0.4995
'''

# 获取模型参数
model_params = model_xgb.get_params()

# 输出模型参数
print("Model Parameters:")
for param, value in model_params.items():
    print(f"{param}: {value}")

# 可视化每棵树的结构
fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(20,10), dpi=800)
xgb.plot_tree(model_xgb, num_trees=0, ax=axes)
plt.show()
