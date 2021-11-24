import pandas as pd

addresses = pd.read_csv('C:/Users/leonr/Documents/Git/IntPakman/data/adresses.csv', sep=';', decimal=',')

addresses.drop(columns=["id", "longitude", "latitude", "distance_from_others"], inplace=True)

#new_addresses = addresses.drop_duplicates()

addresses.to_csv("C:/Users/leonr/Documents/Git/IntPakman/data/adresses_new1.csv", index=False)
