import Neo4j.GetDistances as db_loader
import Neo4j.GetAddessesWithPackages as db_loader_addresses
import Neo4j.GetPrioStatusPackages as db_loader_prio
import Travelling_Salesman as TSP
from collections import Counter
import numpy as np


def fix_values_in_list(input, number_of_knots):
    for item in input:
        if item.get('s.id') == str(1):
            item['s.id'] = str(0)
            number_of_knots += 1
        if item.get('r.distance') == str(0):  # distance is not allowed to be 0
            item['r.distance'] = str(1)
    return input, number_of_knots


def create_key_dict(input, key_dict, key_dict_back):
    """
    necessary because the TSP function expects the knots to be numerated from 0 to how many knots are existing.
    creates two dictionary. One has as the key the id of the address and as the value it has a new id calculated with
    a counter. The second dict is the other way around, to be able to convert it back later.
    :param input: data from db query
    :param key_dict: empty, needs to be created
    :param key_dict_back: empty, needs to be created
    :return: inpunt (unchanged), created key_dict, created key_dict_back
    """
    counter = 1
    for item in input:
        if 's.id' in item:
            key_dict[item.get('a.id')] = str(counter)
            key_dict_back[str(counter)] = item.get('a.id')
            counter += 1
    return input, key_dict, key_dict_back


def change_keys(input, key_dict):
    """
    Changes the address id to a new id defined in the key_dict. Two different dict types in this case. Need to check
    if the dict is from Post-Station to Address or from Address to Address
    :param input: data from DB
    :param key_dict: dict with the address id as input and the new id as value
    :return:
    """
    for item in input:
        if 's.id' in item:
            item['a.id'] = str(key_dict.get(item.get('a.id')))
        else:
            item['a1.id'] = str(key_dict.get(item.get('a1.id')))
            item['a2.id'] = str(key_dict.get(item.get('a2.id')))
    return input


def create_final_list(input):
    """
    Gets the preprocessed list of dict-elements and returns list of list elements
    :param input: data from DB with changed keys
    :return: list containing list-elements like: [[knot1, knot 2, distance]]
    """
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
    return final_list


def change_keys_back(result, key_dict_back):
    for i in range(len(result)):
        result[i] = str(key_dict_back.get(str(result[i])))
    return result


def get_final_input_list_and_key_dict():
    """
    Gets data from DB and executes data preparation steps needed to transform input into readable list for tsp.
    :return: list that contains list-elements with data like this: [[knot 1, knot 2, distance]], returns key_dict and
    key_dict_back
    """
    data = db_loader.get_distance_between_all()

    number_of_knots = 1
    key_dict = {'0': '0'}
    key_dict_back = {'0': '0'}

    data, number_of_knots = fix_values_in_list(data, number_of_knots)
    data, key_dict, key_dict_back = create_key_dict(data, key_dict, key_dict_back)
    data_with_changed_keys = change_keys(data, key_dict)
    final_list = create_final_list(data_with_changed_keys)
    return final_list, key_dict, key_dict_back


def change_keys_prio(input, key_dict):
    for item in input:
        item["a.id"] = key_dict.get(item["a.id"])

    return input


def clean_data_from_duplicate_addresses(input):
    """
    Removes duplicated addresses that recieve more than one package and returns prio 1 if any package has that prio,
    otherwise return prio 0 for this address.
    :param input: data from DB with changed keys
    :return: list with dict-elements like {"a.id":id, "p.prio":prio}
    """
    key_list = [item["a.id"] for item in input]
    unique_key_list = Counter(key_list).keys()

    new_list = []
    for element in unique_key_list:
        temp = []
        for item in input:
            if str(element) == item["a.id"]:
                temp.append(item)
        if len(temp) == 1:
            new_list.append(temp[0])
        elif len(temp) > 1:
            prio = False
            for x in temp:
                if x["p.prio"] == "1":
                    prio = True
            if prio:
                new_list.append({"a.id": temp[0]["a.id"], "p.prio": "1"})
            else:
                new_list.append({"a.id": temp[0]["a.id"], "p.prio": "0"})

    return new_list


def create_final_prio_list(input):
    """
    Gets the preprocessed list of dict-elements and returns list of list elements
    :param input: data from DB with changed keys and removed duplicates
    :return: list containing list-elements like: [[knot, prio]]
    """
    final_prio_list = []
    for item in input:
        final_prio_list.append([int(item["a.id"]), int(item["p.prio"])])

    return final_prio_list


def get_prio_list(key_dict):
    """
    Gets data from DB and executes data preparation steps needed to transform input into readable prio list for tsp.
    :param key_dict: dict with address id as key and new id als value / created before for final_list
    :return:list containing list-elements like: [[knot, prio]]
    """
    data = db_loader_prio.get_prio_status_packages()

    data_with_changed_keys = change_keys_prio(data, key_dict)
    data_cleand_from_duplicates = clean_data_from_duplicate_addresses(data_with_changed_keys)
    final_prio_list = create_final_prio_list(data_cleand_from_duplicates)
    return final_prio_list


def rearange_route(final_result):
    """
    Gets the result of the tsp algorithm with already changed keys and rearranges it, so the route always starts at the
    Post-Station.
    :param final_result: optimal route calculated by tsp algorithm
    :return: list with the rearranged route, starting at the Post-Station
    """
    index = [i for i, x in enumerate(final_result) if x == 0]
    list_end = final_result[0:index[0]]
    list_starting_with_zero = final_result[index[0]:len(final_result)]
    list_starting_with_zero.extend(list_end)
    route_list = list_starting_with_zero
    return route_list


def process_result(best_state, best_fitness, key_dict_back):
    """
    Gets the result of the tsp algorithm and changes the keys back to the address ids from the DB. Rearranges the route
    so it always starts at the Post-Station and gets the address information from the DB to match the route address id
    with the address information from the DB. Prints final route.
    :param best_state:
    :param best_fitness:
    :param key_dict_back:
    """
    final_result = change_keys_back(best_state, key_dict_back)
    final_result_list = final_result.tolist()
    route = rearange_route(final_result_list)

    print('The optimal route without prio is: ' + str(route))

    address_data = db_loader_addresses.get_addresses_with_packages()
    route_addresses = [{'city': 'Furtwangen im Schwarzwald', 'street': 'Robert-Gerwig-Platz',
                        'geojson_geometry': "{'type': 'Point', 'coordinates': [8.2075067, 48.05139]}", 'district': '1',
                        'post_code': '78120', 'house_number': '1', 'id': '7'}]
    for item in route:
        for ad in address_data:
            if int(ad['n']['id']) == item:
                address = ad['n']
                route_addresses.append(address)

    for item in route_addresses:
        print(item)


final_list, key_dict, key_dict_back = get_final_input_list_and_key_dict()
print(final_list)
final_prio_list = get_prio_list(key_dict)
print(final_prio_list)
# TSP
best_state, best_fitness = TSP.get_tsp_result(final_list, final_prio_list, fitness=True)

print(best_state)
print(best_fitness)

process_result(best_state, best_fitness, key_dict_back)
