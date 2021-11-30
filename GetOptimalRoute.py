import Neo4j.GetDistances as db_loader
import travelling_salesman.Travelling_Salesman as TSP
import numpy as np

data = db_loader.get_distance_between_all()
final_list = []
number_of_knots = 1
#key_dict = {'old_key': 0, 'new_key': 0}
key_dict = {'0': '0'}
counter = 1

def fix_values_in_list(input, number_of_knots):
    for item in input:
        if item.get('s.id') == str(1):
            item['s.id'] = str(0)
            number_of_knots += 1
        if item.get('r.distance') == str(0): #distance is not allowed to be 0
            item['r.distance'] = str(1)
    return input, number_of_knots


data, number_of_knots = fix_values_in_list(data, number_of_knots)

for item in data:
    if 's.id' in item:
        #key_dict.append({'old_key': int(item.get('a.id')), 'new_key': counter})
        key_dict[item.get('a.id')] = str(counter)
        counter += 1


for item in data:
    if 's.id' in item:
        item['a.id'] = str(key_dict.get(item.get('a.id')))
    else:
        item['a1.id'] = str(key_dict.get(item.get('a1.id')))
        item['a2.id'] = str(key_dict.get(item.get('a2.id')))


for item in data:
    if 's.id' in item:
        element = [int(item.get('s.id')),
                   int(item.get('a.id')),
                   int(item.get('r.distance'))]
        final_list.append(element)
    else:
        element = [int(item.get('a1.id')),
                   int(item.get('a2.id')),
                   int(item.get('r.distance'))]
        final_list.append(element)

print(final_list)

#TSP
best_state, best_fitness = TSP.get_optimal_path_and_best_fitness(final_list, number_of_knots)

print(best_state)
print(best_fitness)