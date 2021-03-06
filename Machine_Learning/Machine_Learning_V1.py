import pickle
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, roc_curve
import matplotlib.pyplot as plt
from Machine_Learning import Visualization as v


def data_preparation(data):
    """
    Adds column volume and prio to the DataFrame.
    :param data: pd DataFrame with package data
    :return: package data with added columns volume and prio
    """
    data['volume'] = (data.length_cm * data.height_cm * data.width_cm)/1000
    #data.drop(columns='id', inplace=True)
    data['prio'] = np.where((data.volume > 8000) | (data.weight_in_g > 25000), 1, 0)

    return data


def get_visualizations(data, path):
    v.plot_data_overview(data, 'length_cm', path)
    v.plot_data_overview(data, 'width_cm', path)
    v.plot_data_overview(data, 'height_cm', path)
    v.plot_data_overview(data, 'weight_in_g', path)
    v.plot_data_overview(data, 'volume', path)
    v.plot_volume_weight_prio(data, path)


def evalute_model(model, Xtest, ytest):
    """
    Runs evaluations on the model. Confusion Matrix, tree details and roc curve.
    :param model: trained model with package data
    :param Xtest: test data to predict
    :param ytest: test data to check prediction
    :return:
    """
    pred = model.predict(Xtest)
    print('Confusion Matrix:')
    print(confusion_matrix(ytest, pred))
    '''
    print(export_text(model))
    feat_importance = model.tree_.compute_feature_importances()
    print(feat_importance)
    fig = plt.figure()
    sklearn.tree.plot_tree(model, max_depth=3)
    fig.show()
    '''
    pred_prob = model.predict_proba(Xtest)
    fpr, tpr, thresholds = roc_curve(ytest, pred_prob[:, 1])
    plt.plot(fpr, tpr)
    plt.plot([0, 1], [0, 1])
    plt.title('ROC-Curve')
    plt.xlabel('False positive rate')
    plt.ylabel('True positive rate')
    plt.show()
    #plt.savefig('data/plots/ROC.png')


def train_model(data):
    """
    Trains the Decision Tree Classifier model with the package data and runs evaluations on it.
    :param data: processed pd DataFrame with package data
    :return: Decision Tree Classifier model about the data
    """
    x_data1 = data.loc[:, ["length_cm", "width_cm", "height_cm", "weight_in_g"]]
    x_data2 = data.loc[:, ["length_cm", "width_cm", "height_cm", "weight_in_g", "volume"]]
    y_data = data.loc[:, ["prio"]]

    # Classification
    model = DecisionTreeClassifier()
    Xtrain, Xtest, ytrain, ytest = train_test_split(x_data2, y_data, test_size=0.2, random_state=42)

    model.fit(Xtrain, ytrain)
    evalute_model(model, Xtest, ytest)

    return model


def save_model(model, path):
    pickle.dump(model, open(path, 'wb'))


def run_machine_learning(path_data, path_plots, path_model, visualize=False, save_model_bool=False):
    """
    Runs the necessary methods to create a Decision Tree Classifier model of the package data.
    :param path_data: path to the package data
    :param path_plots: path to where the plots should be saved
    :param path_model: path to where the model should be saved
    :param visualize: Boolean, standard is set to false, if true, runs visualization and save them to the specified path
    :param save_model_bool: Boolean, standard is set to false, if true, saves the model to the specified path
    :return:
    """
    input_data = pd.read_csv(path_data, sep=',')
    cleaned_data = data_preparation(input_data)
    if visualize:
        get_visualizations(cleaned_data, path_plots)

    model = train_model(cleaned_data)
    if save_model_bool:
        save_model(model, path_model)


data_path = '../data/package_data/training_data_2022.csv'
plots_path = '../data/plots/simple_2022'
model_path = '../Models/model_Classifier_simple_V1'
run_machine_learning(data_path, plots_path, model_path)