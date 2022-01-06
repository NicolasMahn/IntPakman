import asyncio
import flask
from flask import request

import travelling_salesman.GetOptimalRoute as get_route
import Neo4j.Add_Packages_API as db

app = flask.Flask(__name__)

'''
async def execute_trigger(post_station_id, district):
    get_route.get_optimal_route(post_station_id, district, show_in_browser=True)
'''


@app.route('/compute-route/', methods=['GET', 'POST'])
def trigger_route_computation():
    if 'post_station_id' and 'district' in request.args:
        #asyncio.set_event_loop(asyncio.new_event_loop())
        #loop = asyncio.get_event_loop()
        #loop.run_until_complete(execute_trigger(int(request.args.get('post_station_id')), int(request.args.get('district'))))
        get_route.get_optimal_route(int(request.args.get('post_station_id')), int(request.args.get('district')), show_in_browser=True)
        return 'Success'
    else:
        return 'Error: Please check the parameter if the naming is correct and all parameters are committed!'


def check_input(data):
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
    data = request.get_json()
    if check_input(data):
        try:
            print('Try to write data')
            db.add_packages_to_db(data)
            return 'Success'
        except:
            return 'Error: Data could not be saved to the database! Please tray again later and make sure your json object has all necessary fields!'
    else:
        return 'Error: Your package data seems to be incomplete. Please make sure your json object has all necessary fields!'


app.run()