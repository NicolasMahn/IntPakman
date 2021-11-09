import json
import csv


def read_json(directory):
    f = open(directory, "r")
    data = json.loads(f.read())
    f.close()
    return data


def read_csv(directory):
    f = open(directory, "r")
    file_data = csv.reader(f)
    data = []
    for fd in file_data:
        data.append(fd)
    f.close()
    return data

def write_json(l, directory):
    f = open(directory, 'w', encoding='UTF8')
    j = json.dumps(l, indent = 4)
    f.write(j)

def write_csv(l, directory):
    f = open(directory, 'w', encoding='UTF8')
    writer = csv.writer(f)
    writer.writerow(l)
    f.close()

def write_s_csv(l, directory):
    f = open(directory, 'w', encoding='UTF8')
    writer = csv.writer(f, delimiter=';')
    writer.writerow(l)
    f.close()

def write(l, directory):
    f = open(directory, 'w', encoding='UTF8')
    f.write(l)
    f.close()


def main():

    adresses = []
    header = ["id",
              "house_number", "street", "post_code", "city",
              "priority",
              "district",
              "as_geojson",
              "distance_from_others"]
    adresses.append(header);

    addr_geojson = get_addr('../map_sorter/map_data/furtwangen.geojson')

    for ag in addr_geojson:


    #add code

    write_s_csv(adresses, '../data/adresses.geojson')



def get_addr(map):
    data = read_json(map)
    # print(data.keys())
    features = data["features"]

    test = read_csv('../map_sorter/map_data/addr_attributes.csv')[0]
    print(test)

    test_features = []

    for f in features:
        properties = f["properties"].keys()
        in_test = False
        for p in properties:
            if p in test:
                in_test = True
        if in_test:
            test_features.append(f)

    #  only needed to generate addr_attributes.geojson file and test.js
    # test_geojson = {"type": "FeatureCollection",
    #                 "features": test_features}
    # write_json(test_geojson, '../map_sorter/map_data/all_addr.geojson')
    # write("var line = " + str(json.dumps(test_geojson)), '../map_sorter/leaflet_test/test.js')

    return test_features


if __name__ == "__main__":
    main()
