import Neo4j.Get_distances_with_params as db_loader_distances
import Neo4j.Get_addesses_with_packages_with_params as db_loader_addresses
import Neo4j.Get_prio_status_packages_with_params as db_loader_prio
import Neo4j.Get_all_packages_with_params as db_loader_packages
import Neo4j.Get_post_station_with_params as db_loader_ps
import Route_Computation.Travelling_Salesman as TSP
from collections import Counter
import numpy as np
import pandas as pd
import webbrowser
from pymongo import MongoClient
import Passwords as credentials
import pymongo as mongo


def fix_values_in_list(input, number_of_knots):
    for item in input:
        if 's.id' in item:
            if item.get('s.id') != str(0):
                item['s.id'] = str(0)
                number_of_knots += 1
        if item.get('r.distance') == str(0):  # distance is not allowed to be 0
            item['r.distance'] = str(1)
        if item.get('r.duration') == str(0):  # duration is not allowed to be 0
            item['r.duration'] = str(1)
    return input, number_of_knots


def create_key_dict(input, key_dict, key_dict_back):
    """
    necessary because the TSP function expects the knots to be numerated from 0 to how many knots are existing.
    creates two dictionary. One has as the key the id of the address and as the value it has a new id calculated with
    a counter. The second dict is the other way around, to be able to convert it back later.
    :param input: data from db query
    :param key_dict: empty, needs to be created
    :param key_dict_back: empty, needs to be created
    :return: inpunt (unchanged), created key_dict: {'0': '0', '949': '1',...},
                                 created key_dict_back {'0': '0', '1': '949',...}
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


def create_final_list_distance(input):
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


def create_final_list_duration(input):
    """
    Gets the preprocessed list of dict-elements and returns list of list elements
    :param input: data from DB with changed keys
    :return: list containing list-elements like: [[knot1, knot 2, duration]]
    """
    final_list = []
    for item in input:
        if 's.id' in item:
            element = [int(item.get('s.id')),
                       int(item.get('a.id')),
                       int(item.get('r.duration'))]
            final_list.append(element)
        else:
            element = [int(item.get('a1.id')),
                       int(item.get('a2.id')),
                       int(item.get('r.duration'))]
            final_list.append(element)
    return final_list


def change_keys_back(result, key_dict_back):
    for i in range(len(result)):
        result[i] = str(key_dict_back.get(str(result[i])))
    return result


def get_final_input_list_and_key_dict(distance: bool, post_station_id: int, district: int, date: str):
    """
    Gets data from DB and executes data preparation steps needed to transform input into readable list for tsp. Can
    either use distance or duration as parameter for distance.
    :param date: date of the packages that should be used
    :param distance: if True, uses distance as parameter, if False uses duration as parameter in the list for tsp
    :param district: id of the district
    :param post_station_id: id of the post station
    :return: list that contains list-elements with data like this: [[knot 1, knot 2, distance]], returns key_dict and
    key_dict_back
    """
    data = db_loader_distances.get_distance_between_all(post_station_id, district, date)

    number_of_knots = 1
    key_dict = {'0': '0'}
    key_dict_back = {'0': '0'}

    data, number_of_knots = fix_values_in_list(data, number_of_knots)
    data, key_dict, key_dict_back = create_key_dict(data, key_dict, key_dict_back)
    data_with_changed_keys = change_keys(data, key_dict)
    if distance:
        final_list = create_final_list_distance(data_with_changed_keys)
    else:
        final_list = create_final_list_duration(data_with_changed_keys)
    return final_list, key_dict, key_dict_back, number_of_knots


def change_keys_prio(input, key_dict):
    for item in input:
        item["a.id"] = key_dict.get(item["a.id"])

    return input


def clean_data_from_duplicate_addresses(input):
    """
    Removes duplicates of addresses that receive more than one package and returns prio 1 if any package of that address
    is a prio package, otherwise returns prio 0 for this address.
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


def create_final_prio_dict(input):
    """
    Gets the preprocessed list of dict-elements and returns list of list elements
    :param input: data from DB with changed keys and removed duplicates
    :return: dict containing list-elements like: {knot: prio, knot: prio}
    """
    final_prio_dict = {0: 0}
    for item in input:
        final_prio_dict[int(item["a.id"])] = int(item["p.prio"])

    return final_prio_dict


def get_prio_list(key_dict, post_station_id: int, district: int, date: str):
    """
    Gets data from DB and executes data preparation steps needed to transform input into readable prio list for tsp.
    :param date: date of the packages that should be used
    :param district: id of the district
    :param post_station_id: id of the post station
    :param key_dict: dict with address id as key and new id als value / created before for final_list
    :return:list containing list-elements like: [[knot, prio]]
    """
    data = db_loader_prio.get_prio_status_packages(post_station_id, district, date)

    data_with_changed_keys = change_keys_prio(data, key_dict)
    data_cleaned_from_duplicates = clean_data_from_duplicate_addresses(data_with_changed_keys)
    final_prio_dict = create_final_prio_dict(data_cleaned_from_duplicates)
    return final_prio_dict


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


def process_result(best_state, best_fitness, key_dict_back, post_station, post_station_id: int, district: int,
                   date: str):
    """
    Gets the result of the tsp algorithm and changes the keys back to the address ids from the DB. Rearranges the route
    so it always starts at the Post-Station (0) and gets the address information from the DB to match the route address
    ids with the address information from the DB. Returns the final route.
    :param date: date of the packages that should be used
    :param district: id of the district
    :param post_station_id: id of the post station
    :param post_station: Address information of post station
    :param best_state:
    :param best_fitness:
    :param key_dict_back: dict with new id  as key and address id als value / created before for final_list
    :return: final route starting at the Post-Station, tpye: [0, 4, 9, 2...]
    """
    route = change_keys_back(best_state, key_dict_back)

    print('The optimal route is: ' + str(route))

    address_data = db_loader_addresses.get_addresses_with_packages(post_station_id, district, date)
    route_addresses = [post_station]
    for item in route:
        for ad in address_data:
            if int(ad['n']['id']) == item:
                address = ad['n']
                route_addresses.append(address)

    return route, route_addresses


def match_packages_to_route(route, post_station, post_station_id: int, district: int, date: str):
    """
    Loads package data from db and matches the address and package data equivalent to the order of the route list
    (input) to the dict.
    :param date: date of the packages that should be used
    :param district: id of the district
    :param post_station_id: id of the post station
    :param post_station: Address information of post station
    :param route: final route starting at the Post-Station, tpye: [0, 1, 3, 2...]
    :return: final route information: list of dicts containing all package and address data in the dict
    """
    package_data = db_loader_packages.get_all_packages(post_station_id, district, date)
    final_route_information = [post_station]

    for id in route:
        for item in package_data:
            if item['a']['id'] == str(id):
                element = item['p']
                element['district'] = item['a']['district']
                element['a_id'] = item['a']['id']
                element['geojson_geometry'] = item['a']['geojson_geometry']
                final_route_information.append(element)

    return final_route_information


def print_to_html(df):
    """
    Uses the input df to create a html table. Opens default browser and displays the html table.
    :param df: pd DataFrame containing the route information
    """
    with open('route.html', 'w') as fo:
        fo.write(df.to_html())
    webbrowser.open('route.html')


def route_into_pd_dataframe(route):
    """
    Uses the input information, creates a pd DataFrame and returns it.
    :param route: containing all package and address data in a dict
    :return: pd DataFrame containing the route information.
    """
    routeDF = pd.DataFrame(
        columns=["Sendungsnummer", "street", "house_number", "post_code", "city", "district", "length_cm", "width_cm",
                 "height_cm", "weight_in_g", "fragile", "perishable", "date", "geojson_geometry", "a_id"])

    for i, item in enumerate(route):
        if i > 0:
            routeDF.loc[i] = [item["sendungsnummer"], item["street"], item["house_number"], item["post_code"],
                              item["city"], item["district"], item["length_cm"], item["width_cm"], item["height_cm"],
                              item["weight_in_g"], item["fragile"], item["perishable"], "",  # item["date"],
                              item["geojson_geometry"], item["a_id"]]
        else:
            routeDF.loc[i] = ["", item["street"], item["house_number"], item["post_code"], item["city"],
                              "", "", "", "", "", "", "", "", item["geojson_geometry"], ""]

    return routeDF


def evaluate_route(route, post_station_id: int, district: int, date: str):
    """
    Calculates the distance and the duration of the route and returns them.
    :param district: id of the district
    :param post_station_id: id of the post station
    :param route: containing all package and address data in a dict
    :return: total_distance and total_duration as int
    """
    distance_data = db_loader_distances.get_distance_between_all(post_station_id, district, date)
    total_distance = 0
    total_duration = 0
    first = True
    second = False
    last_element = {}

    for element in route:
        if not first:
            if second:
                for item in distance_data:
                    if 's.id' in item:
                        if item.get("a.id") == element["a_id"]:
                            total_distance += int(item.get("r.distance"))
                            total_duration += int(item.get("r.duration"))
                second = False

            else:
                for item in distance_data:
                    if item.get("a1.id") == last_element["a_id"] and item.get("a2.id") == element["a_id"]:
                        total_distance += int(item.get("r.distance"))
                        total_duration += int(item.get("r.duration"))
                    elif item.get("a2.id") == last_element["a_id"] and item.get("a1.id") == element["a_id"]:
                        total_distance += int(item.get("r.distance"))
                        total_duration += int(item.get("r.duration"))

        if first:
            first = False
            second = True
        last_element = element

    # for the distance and duration back to the post station
    for item in distance_data:
        if 's.id' in item:
            if item.get("a.id") == last_element["a_id"]:
                total_distance += int(item.get("r.distance"))
                total_duration += int(item.get("r.duration"))

    print('Total distance: ' + str(total_distance) + ' meter')
    print('Total duration: ' + str(total_duration) + ' seconds, ' + str(total_duration/60) + ' min')


def save_route_in_mongo_db(final_route_information, post_station_id, district, date):
    """
    Creates dict with key informationa and adds final_route_information as data. Saves the dict into a MongoDB database.
    :param date: date of the packages that should be used
    :param post_station_id: id of the post station
    :param final_route_information:  containing all package and address data
    :param district: district identifier
    """

    final_dict = {"post_station": post_station_id,
                  "district": district,
                  "date": date,
                  "route_data": final_route_information}

    connection_string = credentials.get_mongodb_connection_string()
    client = MongoClient(connection_string)
    db = client.routenplaner
    collection = db['routen']
    collection.insert_one(final_dict)
    print('[LOG]: Successfully stored route information in DB')


def get_optimal_route(post_station_id: int, district: int, date: str, distance=True, prio=True, evaluate=False,
                      curve=False):
    """
    Runs the necessary methods to get the optimal route for the packages in the db. Saves the result in a MongoDB
    database.
    :param curve: If ste to True, prints the fitness curve of tsp to console
    :param date: date of the packages that should be used
    :param distance: if true uses distance for tsp, if false uses duration for tsp
    :param evaluate: if true runs evaluation on computed route, if false not
    :param post_station_id: id of the post station
    :param district: number of the district
    :param prio: if set to True, runs the get_optimal_route with prio list, else without
    :return: prints optimal route with all information about packages and addresses to the console
    """
    final_list, key_dict, key_dict_back, number_of_knots = get_final_input_list_and_key_dict(distance, post_station_id,
                                                                                             district, date)
    post_station = db_loader_ps.get_post_station(post_station_id)
    print(post_station[0]['s'])
    # print(final_list)
    final_route_information = np.NAN
    fitness_curve = np.NAN

    # TSP without prio
    if not prio:
        best_state, best_fitness, fitness_curve = TSP.get_tsp_result_without_prio(final_list, number_of_knots,
                                                                                  fitness=True, curve=True)
        print('TSP without prio and distance = ' + str(distance) + ' :')
        print(best_state)
        print(best_fitness)

        route, route_addresses = process_result(best_state, best_fitness, key_dict_back, post_station[0]['s'],
                                                post_station_id, district, date)

        final_route_information = match_packages_to_route(route, post_station[0]['s'],
                                                          post_station_id, district, date)

    if prio:
        final_prio_list = get_prio_list(key_dict, post_station_id, district, date)
        print(final_prio_list)
        best_state, best_fitness, fitness_curve = TSP.get_tsp_result(final_list, final_prio_list, fitness=True,
                                                                     curve=True)
        print('TSP with prio and distance = ' + str(distance) + ' :')
        print(best_state)
        print(best_fitness)

        route, route_addresses = process_result(best_state, best_fitness, key_dict_back, post_station[0]['s'],
                                                post_station_id, district, date)

        final_route_information = match_packages_to_route(route, post_station[0]['s'],
                                                          post_station_id, district, date)

        save_route_in_mongo_db(final_route_information, post_station_id, district, date)

    if evaluate:
        evaluate_route(final_route_information, post_station_id, district, date)

    if curve:
        print('Curve fitness:')
        print(fitness_curve)
