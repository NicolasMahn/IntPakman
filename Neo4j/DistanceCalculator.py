from neo4j import GraphDatabase
import requests, json
import Neo4j.GetAddessesWithPackages as address_loader
import Neo4j.GetPostStation as station_loader


def calculate_distance(node_a, node_b):
    post_code_origin = node_a["post_code"]
    post_code_destination = node_b["post_code"]
    street_origin = node_a["street"]
    street_destination = node_b["street"]
    house_number_origin = node_a["house_number"]
    house_number_destination = node_b["house_number"]
    city_origin = node_a["city"]
    city_destination = node_b["city"]

    api_key = "AIzaSyBZ_8OLOi5gI_IYgjJnVHF9iDn0CJRx9Xs"
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?"
    source = house_number_origin + "+" + street_origin + "+" + post_code_origin + "+" + city_origin
    dest = post_code_destination + "+" + street_destination + "+" + house_number_destination + "+" + city_destination

    r = requests.get(url + 'origins=' + source +
                     '&destinations=' + dest +
                     '&key=' + api_key)

    x = r.json()
    print(x)
    distance = str(x["rows"][0]["elements"][0]["distance"]["value"])
    duration = str(x["rows"][0]["elements"][0]["duration"]["value"])
    return distance, duration


class DistanceCalculator:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def add_relationship(self, results):
        with self.driver.session() as session:
            session.write_transaction(
                self._add_distance, results)

    @staticmethod
    def _add_distance(tx, results):
        distance_list = []
        for x in range(len(results)):
            entry = results[0]
            id_a = entry["n"]["id"]
            results.pop(0)
            distance_list = results
            for y in range(len(distance_list)):
                distance, duration = calculate_distance(entry["n"], distance_list[y]["n"])
                id_b = distance_list[y]["n"]["id"]
                query = """MATCH(a:Address),(b:Address) 
                           WHERE a.id = $id_a AND b.id = $id_b
                           CREATE (a)-[r:DISTANCE_TO {distance: $distance, duration: $duration}]->(b)-
                           [d:DISTANCE_TO {distance:$distance, duration: $duration}]->(a) """
                tx.run(query, id_a=id_a, id_b=id_b, distance=distance, duration=duration)

    def add_relationship_station(self, results, station):
        with self.driver.session() as session:
            session.write_transaction(
                self._add_distance_station, results, station)

    @staticmethod
    def _add_distance_station(tx, results, station):
        id_s = station[0]["s"]["id"]
        for i in range(len(results)):
            distance, duration = calculate_distance(station[0]["s"], results[i]["n"])
            id_a = results[i]["n"]["id"]
            query = """MATCH(a:Address),(s:PostStation) 
                           WHERE a.id = $id_a AND s.id = $id_s
                           CREATE (s)-[r:DISTANCE_TO {distance: $distance, duration: $duration}]->(a)-
                           [d:DISTANCE_TO {distance:$distance, duration: $duration}]->(s) """
            tx.run(query, id_a=id_a, id_s=id_s, distance=distance, duration=duration)


if __name__ == "__main__":
    connector = DistanceCalculator("bolt://192.52.37.239:7687", "neo4j", "test")
    addresses = address_loader.get_addresses_with_packages()
    connector.add_relationship(addresses)
    addresses = address_loader.get_addresses_with_packages()
    station = station_loader.get_post_station()
    connector.add_relationship_station(addresses, station)
