import pickle
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import Neo4j.GetAddessesWithPackages as loader
import Neo4j.GetPostStation as ploader
import Neo4j.Get_distances_with_params as dloader
import data_gen.Generator_Packages_V2 as d_gen
import Neo4j.GetAllPackages as ploader
import Neo4j.AddPackages as db
import Neo4j.Add_Addresses as add_ad
import Neo4j.Get_all_addesses_with_params as get_ad



#add_ad.add_address_to_db('data/district2.csv')

data = get_ad.get_all_addresses(1, 2)
print(data)

#data = dloader.get_distance_station_addresses(1, 1, "2022-01-01") #"2022-01-01"
#print(data)
#print(len(data))

#d_gen.generate_random_package_data(35, "2022-01-02", "C://Users/leonr/Documents/Git/IntPakman/data/package_data/d1_2022-01-02.csv")
#db.add_packages_to_db('data/package_data/d1_2022-01-02.csv', 'Models/model_Classifier_without_volue_V2')


'''
def load_model(model_path, model):
    print('in method try loading model')
    model = pickle.load(open(model_path, 'rb'))
    return model



model = DecisionTreeClassifier()
path_model = 'Models/model_Classifier_without_volue_V2'
model = load_model(path_model, model)

test = {"length_cm":["120"],
        "width_cm":["98"],
        "height_cm":["50"],
        "weight_in_g":["2500"]
}
x = pd.DataFrame(test)
result = model.predict(x)[0]
print(result)


data = ploader.get_all_packages()
print(data)
print(data[0]['a']['id'])

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


distances = dloader.get_distance_station_addresses()
print(distances)
print(distances[0])
print(len(distances))

print('-------------------------------------------------------')

print('-------------------------------------------------------')

completeList = dloader.get_distance_between_all()
print(completeList)
print(len(completeList))
print(type(completeList[0]))

for item in completeList:
    if item.get('s.id') == str(1):
        item['s.id'] = str(0)
print(completeList)


for item in completeList:
    if item.get('a1.id') == str(3):
        print(item)
    if item.get('a2.id') == str(3):
        print(item)
'''
