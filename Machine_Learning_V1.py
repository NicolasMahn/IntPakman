import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

data = pd.read_csv('data/paketdaten.csv', sep=';')

fig = plt.figure()
plt.scatter(data.id, data.gewicht_in_g)
fig.show()

Xtrain, Xtest, ytrain, ytest = train_test_split(data.drop('', inplace=True), )