import util
import ast
import numpy as np

MAX_LO = 8.2302962
MAX_LA = 48.066499
MID_LO = 8.2033782
MID_LA = 48.056221
MIN_LO = 8.1764602
MIN_LA = 48.041943

# Geometric middle coordinates
# MAX: 8.2302962    48.0664989
# MID: 8.2033782    48.0542213
# MIN: 8.1764602    48.0419438

def main():

    adresses = util.read_semicolon_csv('../data/adresses.csv')
    header = adresses.pop(0)
    header.append("post_station_id")

    left_top = [MIN_LO, MAX_LA]
    left_mid = [MIN_LO, MID_LA]
    left_bot = [MIN_LO, MIN_LA]

    mid_top = [MID_LO, MAX_LA]
    mid_mid = [MID_LO, MID_LA]
    mid_bot = [MID_LO, MIN_LA]

    right_top = [MAX_LO, MAX_LA]
    right_mid = [MAX_LO, MID_LA]
    right_bot = [MAX_LO, MIN_LA]

    district1_count = 0
    district2_count = 0
    district3_count = 0
    district4_count = 0
    districtr_count = 0

    district1 = []
    district2 = []
    district3 = []
    district4 = []
    districtr = []

    for adress in adresses:

        adress.append(1)  # post_station_id

        geojson = ast.literal_eval(adress[6])
        coordinates = get_center(geojson)

        if coordinates[0] > MID_LO:
            if coordinates[1] > MID_LA:
                district2_count+=1
                adress[5] = 2
                district2.append(adress)
            else:
                district4_count+=1
                adress[5] = 4
                district4.append(adress)
        else:
            if coordinates[1] > MID_LA:
                district1_count+=1
                adress[5] = 1
                district1.append(adress)
            else:
                district3_count+=1
                adress[5] = 3
                district3.append(adress)

        if np.random.choice(100, 1)[0] < 3 and districtr_count < 50:
            districtr_count += 1
            cp_adress = adress.copy()
            cp_adress[5] = 5
            districtr.append(cp_adress)




    sum = district1_count + district2_count + district3_count + district4_count
    print("District 1: "+ str(district1_count) +"   "+ str(round(100/sum*district1_count, 2)) +"%")
    print("District 2: "+ str(district2_count) +"   "+ str(round(100/sum*district2_count, 2)) +"%")
    print("District 3: "+ str(district3_count) +"   "+ str(round(100/sum*district3_count, 2)) +"%")
    print("District 4: "+ str(district4_count) +"   "+ str(round(100/sum*district4_count, 2)) +"%")
    print("Random District: "+ str(districtr_count) +"   "+ str(round(100/sum*districtr_count, 2)) +"%")

    district1.insert(0, header)
    district2.insert(0, header)
    district3.insert(0, header)
    district4.insert(0, header)
    districtr.insert(0, header)

    util.write_semicolon_csv(district1, "../data/district1.csv")
    util.write_semicolon_csv(district2, "../data/district2.csv")
    util.write_semicolon_csv(district3, "../data/district3.csv")
    util.write_semicolon_csv(district4, "../data/district4.csv")
    util.write_semicolon_csv(districtr, "../data/districtR.csv")



#calculates centroid of poligon
def get_center(shape):

    if shape["type"] == "Point":
        return [shape["coordinates"][0], shape["coordinates"][1]]

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

        return [round(lo/k, 7), round(la/k, 7)]


if __name__ == "__main__":
    main()