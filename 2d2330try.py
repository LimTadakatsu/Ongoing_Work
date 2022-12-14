# -*- coding: utf-8 -*-
"""2D2330try.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1B1nQ3ZiUPEDawuvs1a4UMtZgu3j8XRuE
"""

import pandas as pd
import numpy as np
import matplotlib
import seaborn as sns
import requests
import io
import matplotlib.pyplot as plt
from sklearn import preprocessing

url = "https://api.finmindtrade.com/api/v4/data"
parameter = {
    "dataset": "TaiwanStockPrice",
    "data_id": "2330",
    "start_date": "2020-04-02"
    #參考登入，獲取金鑰
}
resp = requests.get(url, params=parameter)
data = resp.json()
data = pd.DataFrame(data["data"])
print(data)

datax = data.drop(labels=["stock_id","date"],axis=1)

corr = datax[["Trading_Volume","Trading_money","close","spread","Trading_turnover"]].corr()
plt.figure(figsize=(8,8))
sns.heatmap(corr,square=True,annot=True,cmap="RdBu_r")

#調整成浮點數
np.set_printoptions(suppress=True) #suppress=True表示不以科學記號表示數字
datax["Trading_money"]
#日期自動編碼
le = preprocessing.LabelEncoder()
le.fit(data['date'])
datay=le.transform(data['date'])

y=data["close"]
x=datay
x=np.array(x)
x = x.reshape((-1,1))  
print(x)
one_array=[y]
y=np.array(one_array).reshape(-1,1)
# y=sum(y,[])
# print(y)

print(len(x))
print(len(y))

plt.scatter(x,y,s=10)
plt.xlabel("x")
plt.ylabel("y")

from sklearn.ensemble import RandomForestRegressor

randomForestModel = RandomForestRegressor(n_estimators=100,criterion="mse")
randomForestModel.fit(x,y.ravel())
# predicted=randomForestModel.predict(x) #線性用


#多項式用
lenx=len(x)
x_test = np.linspace(-0.1,lenx,lenx)[:,None]
predicted=randomForestModel.predict(x_test)
plt.scatter(x.ravel(),y)
plt.plot(x_test,predicted,label='n_estimators=100', color='r')
plt.legend(loc='best')
plt.figure(figsize=(10,10))
plt.show()

#模型評估

from sklearn import metrics
print("R2 score:",randomForestModel.score(x,y))
mse= metrics.mean_squared_error(y,predicted)
print("Mse score:",mse)

plt.scatter(x,y,s=10,label="True")
plt.scatter(x,predicted,color="r",s=10,label="predicted")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.show()