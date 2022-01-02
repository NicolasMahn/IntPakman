from pymongo import MongoClient
import pymongo

client = MongoClient("mongodb+srv://intpakman:veryhard@cluster0.lalug.mongodb.net/routenplaner?retryWrites=true&w=majority")
db = client.routenplaner
collection = db['routen']
print("Connected to db")

#client = MongoClient(
#    "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false")
#db = client.IntPakMan
#collection = db['route']
#for item in collection.find():
#    print(item)

item_1 = {
"_id" : "U1IT00001",
"item_name" : "Blender",
"max_discount" : "10%",
"batch_number" : "RR450020FRG",
"price" : 340,
"category" : "kitchen appliance"
}

collection.insert_many([item_1])

for item in collection.find():
    print(item)