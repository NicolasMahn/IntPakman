import json
from util import Cleric


def read_map(map):
    data = Cleric.read_json(map)
    features = data["features"]
    return features


def main():

    center_geojson = []

    adresses = []
    header = ["id",
              "house_number", "street", "post_code", "city",
              "sequence",
              "district",
              "geojson_geometry",
              "longitude",
              "latitude",
              "distance_from_others"]
    adresses.append(header)

    #input directory of map data

    map = read_map('../map_sorter/map_data/furtwangen.geojson')

    addr_geojson = get_addr(map)

    streets = get_streets(map)

    id_ = 0

    for ag in addr_geojson:

        geojson_geometry = ag["geometry"]

        properties = ag["properties"]

        if "addr:housenumber" and "addr:street" in properties.keys():
            house_number = properties["addr:housenumber"]
            street = properties["addr:street"]
        else:
            break
        if "addr:postcode" in properties.keys():
            post_code = properties["addr:postcode"]
        else:
            post_code = "78120"
        if "addr:city" in properties.keys():
            city = properties["addr:city"]
        else:
            city = "Furtwangen im Schwarzwald"

        center = get_center(geojson_geometry)

        #for tests only
        center_geojson.append({"type": "Feature",
                               "geometry": {"type": "Point",
                                            "coordinates": [center["longitude"],
                                                            center["latitude"]]}})

        print(street)
        probable_door = get_door(center, streets[street])

        adresses.append([id_,
                         house_number, street, post_code, city,
                         None, #priority
                         1, #district
                         geojson_geometry,
                         None, #longitude
                         None, #latitude
                         None, #distance_from_others
                         ])

        id_+=1

    # juste to make test2.js and centers.geojson
    Cleric.write_json(center_geojson, '../map_sorter/map_data/centers.geojson')
    Cleric.write("var line2 = "  + str({"type": "FeatureCollection", "features": center_geojson}), '../map_sorter/leaflet_test/test2.js')

    Cleric.write_semicolon_csv(adresses, '../data/adresses.csv')


def get_door(point, street):

    street_coordinates = street["geometry"]["coordinates"]
    print(len(street_coordinates))
    for i in range(0, len(street_coordinates)-1):
        #print(i)
        pass



    return None


#calculates centroid of poligon
def get_center(shape):

    if shape["type"] == "Point":
        return {"longitude": shape["coordinates"][0],
                "latitude": shape["coordinates"][1]}

    else:
        if shape["type"] == "MultiPolygon":
            coordinates = shape["coordinates"][0][0]
        else:
            coordinates = shape["coordinates"]
        k = 0
        lo = 0.0
        la = 0.0
        for coordinate in coordinates:
            #print(coordinate)
            lo += coordinate[0]
            la += coordinate[1]
            k += 1

        return {"longitude": lo/k,
                "latitude": la/k}






def get_streets(map):

    street_attributes = Cleric.read_csv('../map_sorter/map_data/street_attributes.csv')[0]

    #test = []
    streets = {}

    for m in map:
        geometry = m["geometry"]
        if "MultiPolygon" in geometry["type"]:
            properties = m["properties"]
            if "highway" in properties.keys():
                if "name" in properties.keys():
                    new_m = {"type": m["type"],
                             "geometry": {"type": "LineString",
                                          "coordinates": m["geometry"]["coordinates"]},
                             "properties": properties}
                    streets[properties["name"]] = new_m

        if "LineString" in geometry["type"]:
            properties = m["properties"]
            if "highway" in properties.keys():
                #if properties["highway"] in street_attributes:
                if "name" in properties.keys():
                    streets[properties["name"]] = m
                    #test.append(m)

    #  only needed to generate all_streets.geojson file and test.js
    # test_geojson = {"type": "FeatureCollection",
    #                 "features": test}
    # Cleric.write_json(streets, '../map_sorter/map_data/all_streets.geojson')
    # Cleric.write("var line3 = " + str(json.dumps(test_geojson)), '../map_sorter/leaflet_test/test3.js')

    return streets



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
            else:
                addr_exist = False
                break
        if addr_exist:
            addr.append(m)


    #  only needed to generate all_addr.geojson file and test.js

    # test_geojson = {"type": "FeatureCollection",
    #                 "features": addr}
    # Cleric.write_json(test_geojson, '../map_sorter/map_data/all_addr.geojson')
    # Cleric.write("var line = " + str(json.dumps(test_geojson)), '../map_sorter/leaflet_test/test.js')

    return addr


if __name__ == "__main__":
    main()
