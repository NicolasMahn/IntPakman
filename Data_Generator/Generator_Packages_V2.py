import pandas as pd
import numpy as np

adresses = pd.read_csv('data/address_data_furtwangen/district1.csv', sep=';')

"""
Declare range of values for the features weight, length, width and height
"""
weight_low = np.arange(50, 2500, 10, int)
weight_middle = np.arange(2500, 5000, 10, int)
weight_high = np.arange(5000, 20000, 10, int)
weight_extremely_high = np.arange(20000, 31500, 10, int)

length_low = np.arange(10, 100, 1, int)
length_middle = np.arange(100, 180, 1, int)
length_high = np.arange(180, 300, 1, int)

width_low = np.arange(5, 100, 1, int)
width_middle = np.arange(100, 160, 1, int)
width_high = np.arange(160, 280, 1, int)

height_low = np.arange(1, 70, 1, int)
height_middle = np.arange(70, 140, 1, int)
height_high = np.arange(140, 220, 1, int)


def get_weight():
    """
    First chooses between a value (1, 2, 3 or 4) for x, the value of x is responsible for choosing between the
    different range of values of weight.
    :return: return the weight
    """
    weight = 0
    x = np.random.choice([1, 2, 3, 4], 1, p=[0.6, 0.2, 0.16, 0.04])
    if x == 1:
        weight = np.random.choice(weight_low, 1)[0]
    elif x == 2:
        weight = np.random.choice(weight_middle, 1)[0]
    elif x == 3:
        weight = np.random.choice(weight_high, 1)[0]
    elif x == 4:
        weight = np.random.choice(weight_extremely_high, 1)[0]
    return weight


def get_length(weight):
    """
    First randomly chooses a value for x (between 1 and 3), the value of x is responsible for choosing between the
    different range of values of length. The random choosing of x is different for different values of the weight.
    :param weight: value between 0 and 3 depending on the weight, for weight = low -> 0, for weight = high -> 3
    :return: returns the length depending on the value of the weight, length is an int for the metric cm
    """
    length = 0
    x = 0
    if weight == 0:
        x = np.random.choice([1, 2, 3], 1, p=[0.65, 0.25, 0.1])
    elif weight == 1:
        x = np.random.choice([1, 2, 3], 1, p=[0.45, 0.5, 0.05])
    elif weight == 2:
        x = np.random.choice([1, 2, 3], 1, p=[0.05, 0.85, 0.1])
    elif weight == 3:
        x = np.random.choice([1, 2, 3], 1, p=[0.05, 0.45, 0.5])

    # ------------------
    if x == 1:
        length = np.random.choice(length_low, 1)[0]
    elif x == 2:
        length = np.random.choice(length_middle, 1)[0]
    elif x == 3:
        length = np.random.choice(length_high, 1)[0]
    return length


def get_width(weight):
    """
    First randomly chooses a value for x (between 1 and 3), the value of x is responsible for choosing between the
    different range of values of width. The random choosing of x is different for different values of the weight.
    :param weight: value between 0 and 3 depending on the weight, for weight = low -> 0, for weight = high -> 3
    :return: returns the width depending on the value of the weight, width is an int for the metric cm
    """
    width = 0
    x = 0
    if weight == 0:
        x = np.random.choice([1, 2, 3], 1, p=[0.65, 0.25, 0.1])
    elif weight == 1:
        x = np.random.choice([1, 2, 3], 1, p=[0.45, 0.45, 0.1])
    elif weight == 2:
        x = np.random.choice([1, 2, 3], 1, p=[0.05, 0.85, 0.1])
    elif weight == 3:
        x = np.random.choice([1, 2, 3], 1, p=[0.05, 0.45, 0.5])

    # ------------------
    if x == 1:
        width = np.random.choice(width_low, 1)[0]
    elif x == 2:
        width = np.random.choice(width_middle, 1)[0]
    elif x == 3:
        width = np.random.choice(width_high, 1)[0]
    return width


def get_height(weight):
    """
    First randomly chooses a value for x (between 1 and 3), the value of x is responsible for choosing between the
    different range of values of height. The random choosing of x is different for different values of the weight.
    :param weight: value between 0 and 3 depending on the weight, for weight = low -> 0, for weight = high -> 3
    :return: returns the height depending on the value of the weight, height is an int for the metric cm
    """
    height = 0
    x = 0
    if weight == 0:
        x = np.random.choice([1, 2, 3], 1, p=[0.65, 0.25, 0.1])
    elif weight == 1:
        x = np.random.choice([1, 2, 3], 1, p=[0.45, 0.45, 0.1])
    elif weight == 2:
        x = np.random.choice([1, 2, 3], 1, p=[0.05, 0.85, 0.1])
    elif weight == 3:
        x = np.random.choice([1, 2, 3], 1, p=[0.05, 0.45, 0.5])

    # ------------------
    if x == 1:
        height = np.random.choice(height_low, 1)[0]
    elif x == 2:
        height = np.random.choice(height_middle, 1)[0]
    elif x == 3:
        height = np.random.choice(height_high, 1)[0]
    return height


def get_package_data():
    """
    First randomly chooses a weight and then gets the values for length, width and height depending on the value of
    the weight.
    :return: the randomly generated attributes weight, length, width and height of a package
    """
    weight = get_weight()
    weight_trasformed = 0
    if weight < 5000:
        weight_trasformed = 0
    elif weight >= 5000 and weight < 15000:
        weight_trasformed = 1
    elif weight >= 15000 and weight < 25000:
        weight_trasformed = 2
    elif weight >= 25000:
        weight_trasformed = 3

    length = get_length(weight_trasformed)
    width = get_width(weight_trasformed)
    height = get_height(weight_trasformed)

    return weight, length, width, height


def generate_random_package_data(number, date, path):
    """
    Generates a pd DataFrame with package data and saves it in a csv file to the specified path. Considers that some
    addresses receive multiple packages.
    :param number: amount of packages to create in dataset
    :param date: date for the packages to be created
    :param path: path specifying where to save the csv file
    :return: saves the created DataFrame in a csv file to the specified path
    """
    old_adress_id = 0

    random_data = pd.DataFrame(
        columns=["Sendungsnummer", "length_cm", "width_cm", "height_cm", "weight_in_g", "fragile", "perishable",
                 "house_number", "street", "post_code", "city", "date"])

    for i in range(0, number):
        rand_double_package = np.random.choice([0, 1], 1, p=[0.85, 0.15])[0]
        if rand_double_package == 0:
            rand_add = np.random.randint(0, len(adresses))
            weight, length, width, height = get_package_data()
            random_data.loc[i] = [(i + 1), length, width, height, weight,
                                  np.random.choice([0, 1], 1, p=[0.85, 0.15])[0],
                                  np.random.choice([0, 1], 1, p=[0.85, 0.15])[0],
                                  adresses.iloc[rand_add, 1], adresses.iloc[rand_add, 2], adresses.iloc[rand_add, 3],
                                  adresses.iloc[rand_add, 4], date]
            old_adress_id = rand_add
        else:
            weight, length, width, height = get_package_data()
            random_data.loc[i] = [(i + 1), length, width, height, weight,
                                  np.random.choice([0, 1], 1, p=[0.85, 0.15])[0],
                                  np.random.choice([0, 1], 1, p=[0.85, 0.15])[0],
                                  adresses.iloc[old_adress_id, 1], adresses.iloc[old_adress_id, 2],
                                  adresses.iloc[old_adress_id, 3], adresses.iloc[old_adress_id, 4], date]

    random_data.to_csv(path, index=False)


#generate_random_package_data(200, "2021-12-15", "../data/random_package_data_V2.csv")
