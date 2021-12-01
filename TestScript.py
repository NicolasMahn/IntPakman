import pickle
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import Neo4j.GetAddessesWithPackages as loader
import Neo4j.GetPostStation as ploader
import Neo4j.GetDistances as dloader

'''
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
'''
'''
distances = dloader.get_distance_station_addresses()
print(distances)
print(distances[0])
print(len(distances))

print('-------------------------------------------------------')

daddresses = dloader.get_distance_addresses_addresses()
print(daddresses)
print(daddresses[0])
print(len(daddresses))
print(type(daddresses))

print('-------------------------------------------------------')

distances.extend(daddresses)
print(distances)
print(distances[len(distances)-1])
print(len(distances))
'''
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
Example of one list element of the result_list
{'a1.id': '5', 'a2.id': '19', 'r.distance': '750', 'r.duration': '148'}
'''

print('-------------------------------------------------------')

'''
addresses = loader.get_addresses_with_packages()
station = ploader.get_post_station()
print(addresses)
print(len(addresses))
print(station)

addresses.append(station)
print(addresses)
'''