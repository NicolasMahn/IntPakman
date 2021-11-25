import pickle
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import Neo4j.GetAddessesWithPackages as loader

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

print(loader.get_addresses_with_packages())
print(len(loader.get_addresses_with_packages()))