import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing
#import xgboost as xgb
 
train = pd.read_csv('C:\\Users\\Nj_neeraj\\Documents\\Data_Science\\b\\loanprediction\\train.csv')
test = pd.read_csv('C:\\Users\\Nj_neeraj\\Documents\\Data_Science\\b\\loanprediction\\test.csv')
cat_vbl = {'Gender','Married','Dependents','Self_Employed','Property_Area'}
num_vbl = {'LoanAmount','Loan_Amount_Term','Credit_History'}
for var in num_vbl:
    train[var] = train[var].fillna(value = train[var].mean())
    test[var] = test[var].fillna(value = test[var].mean())
train['Credibility'] = train['ApplicantIncome'] / train['LoanAmount']
test['Credibility'] = test['ApplicantIncome'] / test['LoanAmount']


train = train.fillna(value = -999)
test = test.fillna(value = -999)
print ("Filled Missing Values")
print ("Starting Label Encode")
for var in cat_vbl:
    lb = preprocessing.LabelEncoder()
    full_data = pd.concat((train[var],test[var]),axis=0).astype('str')
    lb.fit( full_data )
    train[var] = lb.transform(train[var].astype('str'))
    test[var] = lb.transform(test[var].astype('str'))
print (test['Dependents'].unique())

features = {'Credibility','Gender','Married','Dependents','Self_Employed','Property_Area','ApplicantIncome','CoapplicantIncome','LoanAmount','Loan_Amount_Term','Credit_History'}
 
x_train = train[list(features)].values
y_train = train['Loan_Status'].values
x_test = test[list(features)].values
 

rf = RandomForestClassifier(n_estimators=100,oob_score = True, max_features = "auto",random_state=10,min_samples_split=2, min_samples_leaf=2)

rf.fit(x_train, y_train)
print ("Starting to predict on the dataset")
rec= rf.predict(x_test)
print ("Prediction Completed")
test['Loan_Status'] = rec
test.to_csv('C:\\Users\\Nj_neeraj\\Documents\\Data_Science\\b\\loanprediction\\sub.csv',columns=['Loan_ID','Loan_Status'],index=False)
