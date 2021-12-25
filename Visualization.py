import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def data_details(data):
    data.info()
    data.weight_in_g.describe()
    data.length_cm.describe()
    data.height_cm.describe()
    data.width_cm.describe()
    data.volume.describe()


def plot_data_overview(data, column, path):
    """
    Plots an overview of all instances in the DataFrame of a specific column and saves a png file of the plot
    :param data: pd DataFrame with package data
    :param column: specified column of the DataFrame
    :return: saves png file of the plot to folder
    """
    fig = plt.figure()
    plt.scatter(data["Sendungsnummer"], data[column])
    plt.title('Overview of ' + str(column))
    plt.xlabel("Package id")
    plt.ylabel(column)
    fig.show()
    fig.savefig(path + str(column) + '_V2.png')


def plot_volume_weight_prio(data, path):
    """
    Creates a plot that shows the relation between weight and Volume and the prioritisation
    :param data: pd DataFrame with package data
    :return: saves png file of the plot to folder
    """
    fig = plt.figure()
    prio = pd.DataFrame(columns=["Sendungsnummer", "length_cm", "width_cm", "height_cm", "weight_in_g", "fragile", "perishable",
                                    "house_number", "street", "post_code", "city", "volume", "prio"])
    counter_prio = 0
    no_prio = pd.DataFrame(columns=["Sendungsnummer", "length_cm", "width_cm", "height_cm", "weight_in_g", "fragile", "perishable",
                                    "house_number", "street", "post_code", "city", "volume", "prio"])
    counter_no_prio = 0
    for i in range(len(data)):
        if data.loc[i, "prio"] == 1:
            prio.loc[counter_prio] = data.loc[i, :]
            counter_prio += 1
        else:
            no_prio.loc[counter_no_prio] = data.loc[i, :]
            counter_no_prio += 1

    plt.scatter(prio.volume, prio.weight_in_g, c="r", label="Prio")
    plt.scatter(no_prio.volume, no_prio.weight_in_g, c="b", label="No prio")
    plt.xlabel("Volume in cm³")
    plt.ylabel("Weight in g")
    plt.title("Volume/Weight/Prio")
    plt.legend()
    fig.show()
    fig.savefig(path + 'volume_weight_prio_V2.png')
