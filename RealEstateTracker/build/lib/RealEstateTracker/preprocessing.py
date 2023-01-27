from math import remainder
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import RobustScaler
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_log_error
from xgboost import XGBRegressor

def surface(df):
    # dropping nulls
    df_nonull = df[df['surface'].notna()]
    # cleaning string
    new = df_nonull["surface"].str.split(" ", n = 1, expand = True)
    df_nonull["surface"] = new[0]
    # filter numbers
    df_nonull = df_nonull[df_nonull['surface'].str.isnumeric()]
    # to float
    df_nonull["surface"] = df_nonull["surface"].astype(float)
    df = df_nonull
    return df

def neighborhood(df):
    # new data frame with split value columns
    new = df["neighborhood"].str.split(" en ", n = 1, expand = True)

    # making separate housetype
    df["nhousetype"]= new[0]

    # making separate dirty neighborhood
    df["ndirty"]= new[1]

    # cleaning neighborhood
    new = df["ndirty"].str.split(" en ", n = 1, expand = True)
    df["neighborhood"] = new[1]
    df["neighborhood"] = df["neighborhood"].apply(lambda x: x.split(", ")[-1])
    df = df.drop(columns="ndirty")
    return df

def price(df):
    # cleaning string
    new = df["price"].str.split(" ", n = 1, expand = True)
    new[0] = new[0].str.replace(".","")
    df["price"] = new[0]
    # number filter
    df = df[df['price'].str.isnumeric()]
    # to float
    df["price"] = df["price"].astype(float)
    return df

def rooms(df):
    # rooms
    # cleaning string
    new = df["rooms"].str.split(" ", n = 1, expand = True)
    # to float
    new[0] = new[0].astype(float)
    df["rooms"] = new[0]
    df_clean = df
    return df_clean

def preprocess():
    # Returns a fully preprocessed data frame. Data should be in the raw_data folder.
    df = pd.read_csv("../raw_data/real_estate_data.csv",index_col="Unnamed: 0").drop(columns="Unnamed: 0.1")
    df = df.drop(columns=["elevator","heating","floor"])
    df = surface(df)
    df = neighborhood(df)
    df = price(df)
    df = rooms(df)
    return df.drop_duplicates().reset_index(drop = True)

def X_y(df):
    X = df.drop(columns="price")
    y = df[['price']]
    return X,y

def split(X,y, test_size = 0.2):
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=test_size)
    return X_train, X_test, y_train, y_test




### Preproc pipeline and model
# Preproc basic
preproc_basic = make_column_transformer((RobustScaler(), ['rooms','surface']),
                                        (OneHotEncoder(handle_unknown="ignore", sparse = False),['neighborhood','nhousetype']),
                                        remainder="passthrough")
# XGBregressor model
model_basic = make_pipeline(preproc_basic, XGBRegressor())





### Cross validation function
def customCrossValidation( model , X , y , cv = 5 , shuffle = True):
    scores = []
    kf = KFold(n_splits = cv , shuffle = True)

    if isinstance(y , pd.DataFrame):
        y = y.to_numpy()

    if isinstance(X , pd.DataFrame):
        X = X.to_numpy()


    for train_index , test_index in kf.split(X):
        print("TRAIN:", len(train_index), "TEST:", len(test_index))
        X_train , X_test = X[train_index] , X[test_index]
        y_train , y_test = np.log(y[train_index]) , y[test_index]
        model.fit(X_train , y_train)
        prediction = np.exp(model.predict(X_test))
        error = mean_squared_log_error(y_test , prediction)
        scores.append(error)
    return {"test_score" : np.array(scores) }


### Use crossvall function:
#or _ in range(20):
    #cv = customCrossValidation( model , X_train , y_train , cv = 5 )
   #score = cv["test_score"].mean()
    #print(score)
