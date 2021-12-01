import Neo4j.GetDistances as db_loader
import travelling_salesman.Travelling_Salesman as TSP
import numpy as np

data = db_loader.get_distance_between_all()

number_of_knots = 1
key_dict = {'0': '0'}
key_dict_back = {'0': '0'}


def fix_values_in_list(input, number_of_knots):
    for item in input:
        if item.get('s.id') == str(1):
            item['s.id'] = str(0)
            number_of_knots += 1
        if item.get('r.distance') == str(0):  # distance is not allowed to be 0
            item['r.distance'] = str(1)
    return input, number_of_knots


def create_key_dict(input, key_dict, key_dict_back):
    counter = 1
    for item in input:
        if 's.id' in item:
            key_dict[item.get('a.id')] = str(counter)
            key_dict_back[str(counter)] = item.get('a.id')
            counter += 1
    return input, key_dict, key_dict_back


def change_keys(input, key_dict):
    for item in input:
        if 's.id' in item:
            item['a.id'] = str(key_dict.get(item.get('a.id')))
        else:
            item['a1.id'] = str(key_dict.get(item.get('a1.id')))
            item['a2.id'] = str(key_dict.get(item.get('a2.id')))
    return input


def create_final_list(input):
    final_list = []
    for item in input:
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
    return final_list


def change_keys_back(result, key_dict_back):
    for i in range(len(result)):
        result[i] = str(key_dict_back.get(str(result[i])))
    return result


def rearange_route(final_result):
    index = [i for i, x in enumerate(final_result) if x == 0]
    list_end = final_result[0:index[0]]
    list_starting_with_zero = final_result[index[0]:len(final_result)]
    list_starting_with_zero.extend(list_end)
    route_list = list_starting_with_zero
    return route_list


data, number_of_knots = fix_values_in_list(data, number_of_knots)
data, key_dict, key_dict_back = create_key_dict(data, key_dict, key_dict_back)
data_with_changed_keys = change_keys(data, key_dict)
final_list = create_final_list(data_with_changed_keys)

# TSP
best_state, best_fitness = TSP.get_optimal_path_and_best_fitness(final_list, number_of_knots)

print(best_state)
print(best_fitness)

final_result = change_keys_back(best_state, key_dict_back)
final_result_list = final_result.tolist()
route = rearange_route(final_result_list)
print('The optimal route is: ' + str(route))