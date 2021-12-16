import data_gen.Generator_Packages_V2 as package_generator
import Machine_Learning_V1 as ml
import Neo4j.AddPackages as db
#import travelling_salesman.GetOptimalRoute as get_route_tsp

# generate training data
package_generator.generate_random_package_data(5000, '2021-12-16', 'data/package_data/training_data_model_2021_12_16.csv')

# run machine learning on training data
ml.run_machine_learning('data/package_data/training_data_model_2021_12_16.csv', 'C:/Users/leonr/Desktop',
                        'C:/Users/leonr/Desktop/model', visualize=True, save_model_bool=True)

# generate package data for db
package_generator.generate_random_package_data(50, '2021-12-16', 'data/package_data/db_data_packages_2021_12_16.csv')

# add packages to db
#db.add_packages_to_db('data/package_data/db_data_packages_2021_12_16.csv', 'C:/Users/leonr/Desktop/model')

# get optimal route
#get_route_tsp.get_optimal_route(show_in_browser=True)