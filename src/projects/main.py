


from random import random


import sys
import time
from twitter.api import TwitterHTTPError
from urllib.error import URLError
from http.client import BadStatusLine
import pandas as pd
import json 
from params import Parameters as params
import pickle
import sklearn
# To make it more readable, lets store
# the OAuth credentials in strings first.

from twitter import *



CONSUMER_KEY = params.keys['API_keys']
CONSUMER_SECRET = params.keys['API_secret_key']
OAUTH_TOKEN = params.keys['Access_token']
OAUTH_TOKEN_SECRET = params.keys['Access_token_secret']

#key_secret = '{}:{}'.format(CONSUMER_SECRET, OAUTH_TOKEN_SECRET).encode('ascii')
#b64_encoded_key = base64.b64encode(key_secret)
#b64_encoded_key = b64_encoded_key.decode('ascii')

#fetching data
cort_df = pd.read_csv(r'../mining/followers_cortez_analysis.csv')
cren_df = pd.read_csv(r'../mining/followers_crenshaw_analysis.csv')


dataset_cortez=cort_df.drop(columns=['ID'])
dataset_cren=cren_df.drop(columns=['ID'])

dataset_cortez=dataset_cortez.loc[(dataset_cortez!=0).any(1)]
dataset_cren=dataset_cren.loc[(dataset_cren!=0).any(1)]

dataset_cortez['main'] = 'cortez'
dataset_cren['main'] = 'crenshaw'


dataset_total = dataset_cortez.append(dataset_cren)
dataset_total = dataset_total.sample(frac=1).reset_index(drop=True)
X = dataset_total.iloc[:,0:21] #df1 = df.iloc[:,0:2]
y = dataset_total.iloc[:, [21]]

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# Fitting Logistic Regression to the Training set
from sklearn.linear_model import LogisticRegression
classifier = LogisticRegression(random_state = 0)
classifier.fit(X_train, y_train)


filename = 'model.sav'
pickle.dump(classifier, open(filename,'wb'))


