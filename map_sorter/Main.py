import json
from util import Cleric


def read_map(map):
    data = Cleric.read_json(map)
    features = data["features"]
    return features


def main():

    unique_addresses = set()
    addresses = []
    header = ["id",
              "house_number", "street", "post_code", "city",
              "district",
              "geojson_geometry"]
    addresses.append(header)

    map = input("Please enter full directory to the map in geojson format")
    if map == "":
        map = '../map_sorter/map_data/furtwangen.geojson'
    map = read_map(map)

    city_hardcode = input("What is the city of your map?")
    if city_hardcode == "":
        city_hardcode = "Furtwangen im Schwarzwald"
    postcode_hardcode = input("What is the post code of your map?")
    if postcode_hardcode == "":
        postcode_hardcode = "78120"

    addr_geojson = get_addr(map)

    id_ = 0

    for addr in addr_geojson:

        geojson_geometry = addr["geometry"]

        properties = addr["properties"]

        if "addr:housenumber" in properties.keys():
            house_number = properties["addr:housenumber"]
        else:
            continue
        if  "addr:street" in properties.keys():
            street = properties["addr:street"]
        else:
            continue

        if "addr:postcode" in properties.keys():
            post_code = properties["addr:postcode"]
        else:
            post_code = postcode_hardcode
        if "addr:city" in properties.keys():
            city = properties["addr:city"]
        else:
            city = city_hardcode

        str = f"{house_number}{street}{post_code}{city}"

        if str not in unique_addresses:
            addresses.append([id_,
                             house_number, street, post_code, city,
                             1, #district
                             geojson_geometry,
                             ])
            unique_addresses.add(str)

        id_+=1

    # # juste to make test2.js and centers.geojson
    # Cleric.write_json(center_geojson, '../map_sorter/map_data/centers.geojson')
    # Cleric.write("var line2 = "  + str({"type": "FeatureCollection", "features": center_geojson}), '../map_sorter/leaflet_test/test2.js')

    Cleric.write_semicolon_csv(addresses, '../data/adresses.csv')





# #calculates centroid of poligon
# def get_center(shape):
#
#     if shape["type"] == "Point":
#         return {"longitude": shape["coordinates"][0],
#                 "latitude": shape["coordinates"][1]}
#
#     else:
#         if shape["type"] == "MultiPolygon":
#             coordinates = shape["coordinates"][0][0]
#         else:
#             coordinates = shape["coordinates"]
#         k = 0
#         lo = 0.0
#         la = 0.0
#         for coordinate in coordinates:
#             #print(coordinate)
#             lo += coordinate[0]
#             la += coordinate[1]
#             k += 1
#
#         return {"longitude": lo/k,
#                 "latitude": la/k}






# def get_streets(map):
#
#     street_attributes = Cleric.read_csv('../map_sorter/map_data/street_attributes.csv')[0]
#
#     #test = []
#     streets = {}
#
#     for m in map:
#         geometry = m["geometry"]
#         if "MultiPolygon" in geometry["type"]:
#             properties = m["properties"]
#             if "highway" in properties.keys():
#                 if "name" in properties.keys():
#                     new_m = {"type": m["type"],
#                              "geometry": {"type": "LineString",
#                                           "coordinates": m["geometry"]["coordinates"]},
#                              "properties": properties}
#                     streets[properties["name"]] = new_m
#
#         if "LineString" in geometry["type"]:
#             properties = m["properties"]
#             if "highway" in properties.keys():
#                 #if properties["highway"] in street_attributes:
#                 if "name" in properties.keys():
#                     streets[properties["name"]] = m
#                     #test.append(m)
#
#     #  only needed to generate all_streets.geojson file and test.js
#     # test_geojson = {"type": "FeatureCollection",
#     #                 "features": test}
#     # Cleric.write_json(streets, '../map_sorter/map_data/all_streets.geojson')
#     # Cleric.write("var line3 = " + str(json.dumps(test_geojson)), '../map_sorter/leaflet_test/test3.js')
#
#     return streets



def get_addr(map):

    addr_attributes = Cleric.read_csv('../map_sorter/map_data/addr_attributes.csv')[0]
    #print(addr_attributes)

    addr = []

    for m in map:
        properties = m["properties"].keys()
        addr_exist = False
        for p in properties:
            if p in addr_attributes:
                addr_exist = True
        if addr_exist:
            addr.append(m)


    #  only needed to generate all_addr.geojson file and test.js

    test_geojson = {"type": "FeatureCollection",
                    "features": addr}
    Cleric.write_json(test_geojson, '../map_sorter/map_data/all_addr.geojson')
    Cleric.write("var line = " + str(json.dumps(test_geojson)), '../map_sorter/leaflet_test/test.js')

    return addr


if __name__ == "__main__":
    main()
