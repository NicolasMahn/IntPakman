import pandas as pd
import numpy as np

adresses = pd.read_csv('C:/Users/leonr/Documents/Git/IntPakman/data/adresses.csv', sep=';', decimal=',')

weight_low = np.arange(50, 2500, 10, int)
weight_middle = np.arange(2500, 5000, 10, int)
weight_high = np.arange(5000, 31500, 10, int)

length_low = np.arange(1, 100, 1, int)
length_middle = np.arange(100, 180, 1 , int)
length_high = np.arange(180, 300, 1, int)

width_low = np.arange(1, 100, 1, int)
width_middle = np.arange(100, 160, 1 , int)
width_high = np.arange(160, 280, 1, int)

height_low = np.arange(1, 70, 1, int)
height_middle = np.arange(70, 140, 1 , int)
height_high = np.arange(140, 220, 1, int)


def get_weight():
    weight = 0
    x = np.random.choice([1,2,3], 1, p=[0.6, 0.2, 0.2])
    if x == 1:
        weight = np.random.choice(weight_low, 1)[0]
    elif x == 2:
        weight = np.random.choice(weight_middle, 1)[0]
    elif x == 3:
        weight = np.random.choice(weight_high, 1)[0]
    return weight


def get_length():
    length = 0
    x = np.random.choice([1,2,3], 1, p=[0.65, 0.25, 0.1])
    if x == 1:
        length = np.random.choice(length_low, 1)[0]
    elif x == 2:
        length = np.random.choice(length_middle, 1)[0]
    elif x == 3:
        length = np.random.choice(length_high, 1)[0]
    return length


def get_width():
    width = 0
    x = np.random.choice([1,2,3], 1, p=[0.65, 0.25, 0.1])
    if x == 1:
        width = np.random.choice(width_low, 1)[0]
    elif x == 2:
        width = np.random.choice(width_middle, 1)[0]
    elif x == 3:
        width = np.random.choice(width_high, 1)[0]
    return width


def get_height():
    height = 0
    x = np.random.choice([1,2,3], 1, p=[0.65, 0.25, 0.1])
    if x == 1:
        height = np.random.choice(height_low, 1)[0]
    elif x == 2:
        height = np.random.choice(height_middle, 1)[0]
    elif x == 3:
        height = np.random.choice(height_high, 1)[0]
    return height


random_data = pd.DataFrame(columns=["Sendungsnummer", "length_cm", "width_cm", "height_cm", "weight_in_g", "fragile", "perishable",
                                    "house_number", "street", "post_code", "city", "id"])

'''
for i in range(0, 20):
    rand_add = np.random.randint(0, len(adresses))
    random_data.loc[i] = [(i+1), get_length(), get_width(), get_height(), get_weight(),
                          np.random.choice([0, 1], 1, p=[0.85, 0.15])[0], np.random.choice([0, 1], 1, p=[0.85, 0.15])[0],
                          adresses.iloc[rand_add,1], adresses.iloc[rand_add,2], adresses.iloc[rand_add,3], adresses.iloc[rand_add,4], rand_add]
'''

def generate_random_package_data(number, path):
    for i in range(0, number):
        rand_add = np.random.randint(0, len(adresses))
        random_data.loc[i] = [(i + 1), get_length(), get_width(), get_height(), get_weight(),
                              np.random.choice([0, 1], 1, p=[0.85, 0.15])[0],
                              np.random.choice([0, 1], 1, p=[0.85, 0.15])[0],
                              adresses.iloc[rand_add, 1], adresses.iloc[rand_add, 2], adresses.iloc[rand_add, 3],
                              adresses.iloc[rand_add, 4], rand_add]
    random_data.to_csv(path)


generate_random_package_data(20, "C:/Users/leonr/Documents/Git/IntPakman/data/random_paketdaten.csv")