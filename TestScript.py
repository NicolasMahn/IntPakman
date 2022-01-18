import Neo4j.GetAddessesWithPackages as loader
import Neo4j.GetPostStation as ploader
import Neo4j.Get_distances_with_params as dloader
import Data_Generator.Generator_Packages_V2 as d_gen
import Neo4j.GetAllPackages as ploader
import Neo4j.AddPackages as db
import Neo4j.Add_Addresses as add_ad
import Neo4j.Get_all_addesses_with_params as get_ad



#add_ad.add_address_to_db('data/address_data_furtwangen/district4.csv')

#data = get_ad.get_all_addresses(1, 2)
#print(data)

#data = dloader.get_distance_station_addresses(1, 1, "2022-01-01") #"2022-01-01"
#print(data)
#print(len(data))

d_gen.generate_random_package_data(35, "2022-01-05", "C://Users/leonr/Documents/Git/IntPakman/data/package_data/d1_2022-01-05.csv")
db.add_packages_to_db('data/package_data/d1_2022-01-05.csv', 'Models/model_Classifier_without_volue_V2')

