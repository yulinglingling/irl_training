import numpy as np
from sklearn.linear_model import LinearRegression

# 示例数据
x1 = np.array([1, 2, 3, 4, 5])
y1 = np.array([2, 4, 6, 8, 10])
x2 = np.array([9, 14, 19, 24, 29])
y2 = np.array([5, 10, 15, 20, 25])

# 重新调整数据形状
virtual = np.column_stack((x1, y1))

# 创建线性回归模型
model_x = LinearRegression()
model_y = LinearRegression()

# 拟合模型
model_x.fit(virtual, x2)
model_y.fit(virtual, y2)

# 输出模型的方程式
def print_linear_regression_equation(model, feature_names):
    coef = model.coef_
    intercept = model.intercept_
    equation = "y = {:.2f}".format(intercept)
    for i, feature_name in enumerate(feature_names):
        equation += " + {:.2f} * {}".format(coef[i], feature_name)
    return equation

# 打印 x2 的方程式
feature_names = ["x1", "y1"]
print("Equation for predicting x2:")
print(print_linear_regression_equation(model_x, feature_names))

# 打印 y2 的方程式
print("Equation for predicting y2:")
print(print_linear_regression_equation(model_y, feature_names))

# 使用模型进行预测
new_x1 = np.array([6])
new_y1 = np.array([13])
new_virtual = np.column_stack((new_x1, new_y1))

x_pred = model_x.predict(new_virtual)
y_pred = model_y.predict(new_virtual)

# 输出预测结果
print("Predicted x2 value:", x_pred[0])
print("Predicted y2 value:", y_pred[0])
