import pickle
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import Neo4j.GetAddessesWithPackages as loader
import Neo4j.GetPostStation as ploader

model = DecisionTreeClassifier()

path = 'Models/model_Classifier_without_volue'
model = pickle.load(open(path, 'rb'))

test = {"length_cm":["120"],
        "width_cm":["98"],
        "height_cm":["50"],
        "weight_in_g":["2500"]
}
x = pd.DataFrame(test)
result = model.predict(x)[0]

addresses = loader.get_addresses_with_packages()
station = ploader.get_post_station()
print(addresses)
print(len(addresses))
print(station)

addresses.append(station)
print(addresses)