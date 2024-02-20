import xgboost as xgb
import lightgbm as lgb
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# 加载乳腺癌数据集（二分类任务）
cancer = load_breast_cancer()
X = cancer.data
y = cancer.target

# 划分数据集为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# XGBClassifier ---------------------------------------------
# 定义模型参数
params = {
    'objective': 'binary:logistic',  # 二分类任务
    'max_depth': 3,
    'learning_rate': 0.1,
    'n_estimators': 10
}

# 创建XGBoost分类器
model = xgb.XGBClassifier(**params)

# 训练XGBoost模型
model.fit(X_train, y_train)

# 在测试集上进行预测
y_pred = model.predict(X_test)

# 计算准确度
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")

# 打印分类报告
print("Classification Report:\n", classification_report(y_test, y_pred))


# LGBMClassifier ---------------------------------------------
# 定义模型参数
params = {
    'objective': 'binary',
    'metric': 'binary_error',  # 二分类任务的评价指标
    'max_depth': 3,
    'learning_rate': 0.1,
    'n_estimators': 10
}

# 创建LightGBM分类器
model = lgb.LGBMClassifier(**params)

# 训练LightGBM模型
model.fit(X_train, y_train)

# 在测试集上进行预测
y_pred = model.predict(X_test)

# 计算准确度
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")

# 打印分类报告
print("Classification Report:\n", classification_report(y_test, y_pred))
