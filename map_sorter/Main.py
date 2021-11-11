
from util import Cleric


def read_map(map):
    data = Cleric.read_json(map)
    features = data["features"]
    return data


def main():

    adresses = []
    header = ["id",
              "house_number", "street", "post_code", "city",
              "sequence",
              "district",
              "geojson_geometry",
              "distance_from_others"]
    adresses.append(header)

    #input directory of map data

    map = read_map('../map_sorter/map_data/furtwangen.geojson')

    addr_geojson = get_addr(map)

    streets_geojson = get_streets(map)

    id_ = int(Cleric.read('../map_sorter/map_data/id.txt'))

    for ag in addr_geojson:

        geojson_geometry = ag["geometry"]

        properties = ag["properties"]

        house_number = None
        street = None
        post_code = None
        city = None

        if "addr:housenumber" in properties:
            house_number = properties["addr:housenumber"]
        if "addr:street" in properties:
            street = properties["addr:street"]
        if "addr:postcode" in properties:
            post_code = properties["addr:postcode"]
        if "addr:city" in properties:
            city = properties["addr:city"]

        adresses.append([id_,
                         house_number, street, post_code, city,
                         None, #priority
                         None, #district
                         geojson_geometry,
                         None, #distance_from_others
                         ])

        id_+=1

    Cleric.write(str(id_), '../map_sorter/map_data/id.txt')

    #print(adresses)
    Cleric.write_semicolon_csv(adresses, '../data/adresses.csv')


def get_streets(map):
    pass #return streets



def get_addr(map):

    addr_attributes = Cleric.read_csv('../map_sorter/map_data/addr_attributes.csv')[0]
    #print(addr_attributes)

    addr = []

    for f in map:
        properties = f["properties"].keys()
        addr_exist = False
        for p in properties:
            if p in addr_attributes:
                addr_exist = True
        if addr_exist:
            addr.append(f)

    #  only needed to generate addr_attributes.geojson file and test.js

    # test_geojson = {"type": "FeatureCollection",
    #                 "features": addr_features}
    # Cleric.write_json(test_geojson, '../map_sorter/map_data/all_addr.geojson')
    # Cleric.write("var line = " + str(json.dumps(test_geojson)), '../map_sorter/leaflet_test/test.js')

    return addr


if __name__ == "__main__":
    main()
