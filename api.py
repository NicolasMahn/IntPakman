import asyncio
import flask
from flask import request

import Route_Computation.GetOptimalRoute as get_route
import Neo4j.Add_Packages_API as db_package
import Neo4j.Add_Address_API as db_address

app = flask.Flask(__name__)

'''
async def execute_trigger(post_station_id, district):
    get_route.get_optimal_route(post_station_id, district, show_in_browser=True)
'''


def str2bool(v):
    return str(v).lower() in ("yes", "true", "t", "1")


@app.route('/compute-route', methods=['GET', 'POST'])
def trigger_route_computation():
    """
    API to trigger route computation. Uses the parameters (some are optional and are initialized with default values) to
    call the get_optimal_route Method from the GetOptimalRoute.py script.
    :return: Returns Success if method-call was successful, else returns error message
    """
    distance = True
    prio = True
    evaluate = False
    curve = False
    if 'post_station_id' and 'district' and 'date' in request.args:
        if 'distance' in request.args:
            distance = str2bool(request.args.get('distance'))
        if 'prio' in request.args:
            prio = str2bool(request.args.get('prio'))
        if 'evaluate' in request.args:
            evaluate =str2bool(request.args.get('evaluate'))
        if 'curve' in request.args:
            curve = str2bool(request.args.get('curve'))
        get_route.get_optimal_route(int(request.args.get('post_station_id')), int(request.args.get('district')),
                                    str(request.args.get('date')), distance, prio, evaluate, curve)
        #asyncio.set_event_loop(asyncio.new_event_loop())
        #loop = asyncio.get_event_loop()
        #loop.run_until_complete(execute_trigger(int(request.args.get('post_station_id')), int(request.args.get('district'))))
        return 'Success'
    else:
        return 'Error: Please check the parameter if the naming is correct and all parameters are committed!'


def check_input_package(data):
    """
    Checks if the json object has the specified Attributes.
    :param data: json object from the POST-Method
    :return: boolean: True if the Attributes are equal and False if not.
    """
    check = False
    for element in list(data.keys()):
        if element in ['Sendungsnummer', 'length_cm', 'width_cm', 'height_cm', 'weight_in_g', 'fragile',
                       'perishable', 'house_number', 'street', 'post_code', 'city', 'date']:
            check = True
        else:
            check = False
            break
    if len(list(data.keys())) != 12:
        check = False
    return check


@app.route('/add-package', methods=['POST'])
def add_package_data():
    """
    Takes package data as json object. Checks if the json object has all necessary fields and adds the package data to
    the Neo4j graphdatabase. 
    :return: Returns Success if method-call was successful, else returns error message
    """
    data = request.get_json()
    if check_input_package(data):
        try:
            db_package.add_packages_to_db(data)
            return 'Success'
        except:
            return 'Error: Data could not be saved to the database! Please tray again later and make sure your json object has all necessary fields!'
    else:
        return 'Error: Your package data seems to be incomplete. Please make sure your json object has all necessary fields!'


def check_input_address(data):
    """
    Checks if the json object has the specified Attributes.
    :param data: json object from the POST-Method
    :return: boolean: True if the Attributes are equal and False if not.
    """
    check = False
    for element in list(data.keys()):
        if element in ['id', 'house_number', 'street', 'post_code', 'city', 'district', 'geojson_geometry',
                       'post_station_id']:
            check = True
        else:
            check = False
            break
    if len(list(data.keys())) != 8:
        check = False
    return check


@app.route('/add-address', methods=['POST'])
def add_address_to_db():
    """
    Takes address data as json object. Checks if the json object has all necessary fields and adds the address data to
    the Neo4j graphdatabase.
    :return: Returns Success if method-call was successful, else returns error message
    """
    data = request.get_json()
    if check_input_address(data):
        try:
            db_address.add_address_to_db(data)
            return 'Success'
        except:
            return 'Error: Data could not be saved to the database! Please tray again later and make sure your json object has all necessary fields!'
    else:
        return 'Error: Your address data seems to be incomplete. Please make sure your json object has all necessary fields!'


app.run(debug=True)