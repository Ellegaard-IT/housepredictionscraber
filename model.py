import subprocess
import sys

import numpy as np

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
try:
    import xgboost
    print(xgboost.__version__)  
except:
    install("xgboost==1.0.1")
try:
    import sklearn
    print(sklearn.__version__)  
except:
    install("sklearn")

from xgboost import XGBRegressor
import pandas as pd
import numpy as np
from sklearn import preprocessing


np.set_printoptions(suppress=True)

try:
    training_data = pd.read_csv('Azure_test_data.csv')
    test_data = pd.read_csv('boliga_data_being_sold_best.csv')
except:
    raise Exception("The data to train or test the model cant be found!")

def GetModel():
    return XGBRegressor(n_estimators=600, max_depth=6, gamma=0, max_leaves=7, eta=0.4, subsample=0.6, colsample_bytree=0.8,reg_alpha=0.625,reg_lambda=0.8333333334)

training_data = training_data.loc[training_data['handelstype'] == 'Alm. frit salg']
training_data = training_data.drop_duplicates('url', keep='last')
allow = ["grundstorrelse"]
for col in training_data.columns:
    if allow.__contains__(str(col)):
        continue
    training_data = training_data[training_data[col] != 0]
    if col == "pris":
        training_data = training_data[training_data["pris"] > 100000]

#Salgsår og måned er ikke med i denne test!
training_data = training_data.drop(columns=['url','handelstype','boligtype','salgsar','salgsmaned','Unnamed: 0'])
test_data = test_data[training_data.columns]

def MakeAllNumbers(df):
    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col],errors='coerce')
        except:
            None
    return df
training_data = MakeAllNumbers(training_data)
test_data = MakeAllNumbers(test_data)

training_data = training_data.dropna()
test_data = test_data.dropna()

price = training_data['pris']
training_data = training_data.drop(columns=['pris'])
pred_price = test_data['pris']
test_data = test_data.drop(columns=['pris'])

x = training_data.to_numpy(dtype=float)
y = price.to_numpy(dtype=float)
test = test_data.to_numpy(dtype=float)

model = GetModel()
model.fit(x, y)

#Example:
#PredictionData = [2860.   87.    0.    3.    6. 2007.    0. 1583.   84.    1.    1.]
def XGBPrediction(predictionData = [],run_test = False):
    if run_test == True:
        preds = model.predict(test)
        result = pred_price.to_frame()
        result.insert(1,"pre_pris",preds.astype(int))
        result['pris'] = result.apply(lambda x: "{:,}".format(x['pris']), axis=1)
        result['pre_pris'] = result.apply(lambda x: "{:,}".format(x['pre_pris']), axis=1)
        print(result.head(10))
    else:
        return model.predict(predictionData)

def EvalModelPerformance():
    from sklearn.model_selection import cross_val_score
    from sklearn.model_selection import RepeatedKFold
    from numpy import absolute

    cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
    scores = cross_val_score(model, x, y, scoring='neg_root_mean_squared_error', cv=cv, n_jobs=-1)
    scores = absolute(scores)
    print('neg_root_mean_squared_error: %.3f (%.3f)' % (scores.mean(), scores.std()) )

XGBPrediction(run_test=True)
EvalModelPerformance()