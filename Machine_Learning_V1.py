import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

data = pd.read_csv('data/paketdaten.csv', sep=';')

Xtrain, Xtest, ytrain, ytest = train_test_split(data.drop('', inplace=True), )