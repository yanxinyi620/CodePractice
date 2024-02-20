import xgboost as xgb
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# 加载波士顿房价数据集
boston = load_boston()
X = boston.data
y = boston.target

# 划分数据集为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 将数据转换为DMatrix格式，XGBoost专用的数据结构
dtrain = xgb.DMatrix(X_train, label=y_train)
dtest = xgb.DMatrix(X_test, label=y_test)

# 定义模型参数
params = {
    'objective': 'reg:squarederror',  # 回归任务
    'max_depth': 3,
    'learning_rate': 0.1,
    'n_estimators': 100
}

# 训练XGBoost模型
model = xgb.train(params, dtrain)

# 在测试集上进行预测
y_pred = model.predict(dtest)

# 计算均方根误差（RMSE）
rmse = mean_squared_error(y_test, y_pred, squared=False)
print(f"Root Mean Squared Error (RMSE): {rmse}")
