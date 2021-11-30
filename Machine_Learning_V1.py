import pickle

import numpy as np
import pandas as pd
import sklearn.tree
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, roc_curve
import matplotlib.pyplot as plt
import Visualization as v


def data_preparation(data):
    data['volume'] = (data.length_cm * data.height_cm * data.width_cm)/1000
    #data.drop(columns='id', inplace=True)
    data['prio'] = np.where((data.volume > 3000) | (data.weight_in_g > 25000), 1, 0)
    #data.loc[(data.volume > 3000) | (data.weight_in_g > 25000), ['prio']] = int(1)
    #data['prio'] = data.[](1 if (data.volume > 3000) | (data.weight_in_g > 25000) else 0)]

    return data


input_data = pd.read_csv('data/random_package_data_train.csv', sep=',', decimal=',')
'''
#Visualization
v.plot_data_overview(input_data, 'length_cm')
v.plot_data_overview(input_data, 'width_cm')
v.plot_data_overview(input_data, 'height_cm')
v.plot_data_overview(input_data, 'weight_in_g')
'''
#Datapreparation
cleaned_data = data_preparation(input_data)
#v.plot_data_overview(cleaned_data, 'volume')
#v.plot_volume_weight_prio(cleaned_data)


x_data1 = cleaned_data.loc[:, ["length_cm", "width_cm", "height_cm", "weight_in_g"]]
x_data2 = cleaned_data.loc[:, ["length_cm", "width_cm", "height_cm", "weight_in_g", "volume"]]
y_data = cleaned_data.loc[:, ["prio"]]

#Classification
model = DecisionTreeClassifier()
Xtrain, Xtest, ytrain, ytest = train_test_split(x_data1, y_data, test_size=0.2, random_state=42)

model.fit(Xtrain, ytrain)
pred = model.predict(Xtest)
print(confusion_matrix(ytest, pred))
print(export_text(model))
feat_importance = model.tree_.compute_feature_importances()
print(feat_importance)
fig = plt.figure()
sklearn.tree.plot_tree(model, max_depth=3)
fig.show()


'''
#save model to file
path = 'Models/model_Classifier_without_volue'
pickle.dump(model, open(path, 'wb'))
'''

pred_prob = model.predict_proba(Xtest)
fpr, tpr, thresholds = roc_curve(ytest, pred_prob[:,1])
plt.plot(fpr, tpr)
plt.plot([0,1],[0,1])
plt.title('ROC-Curve')
plt.xlabel('False positive rate')
plt.ylabel('True positive rate')
plt.show()
#plt.savefig('C:/Users/leonr/Desktop/ROC1.png')