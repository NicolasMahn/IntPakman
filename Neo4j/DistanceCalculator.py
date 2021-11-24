from neo4j import GraphDatabase
import requests, json


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
    return str(x["rows"][0]["elements"][0]["distance"]["value"])


class DistanceCalculator:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def neo_transaction(self):
        with self.driver.session() as session:
            result = session.write_transaction(
                self._get_addresses)

            return result

    def add_relationship(self, results):
        with self.driver.session() as session:
            session.write_transaction(
                self._add_distance, results)

    @staticmethod
    def _get_addresses(tx):
        query = "MATCH(n:Address) RETURN n"
        result = tx.run(query)
        values = []
        for record in result:
            values.append(record.data())

        return values


    @staticmethod
    def _add_distance(tx, results):
        distance_list = []
        for x in range(len(results)):
            entry = results[0]
            id_a = entry["n"]["id"]
            results.pop(0)
            distance_list = results
            for y in range(len(distance_list)):
                distance = calculate_distance(entry["n"], distance_list[y]["n"])
                id_b = distance_list[y]["n"]["id"]
                query = """MATCH(a:Address),(b:Address) 
                           WHERE a.id = $id_a AND b.id = $id_b
                           CREATE (a)-[r:DISTANCE_TO {distance: $distance}]->(b)-[d:DISTANCE_TO {distance:$distance}]->(a) """
                tx.run(query, id_a=id_a, id_b=id_b, distance=distance)


if __name__ == "__main__":
    connector = DistanceCalculator("bolt://localhost:7687", "neo4j", "test")
    addresses = connector.neo_transaction()
    connector.add_relationship(addresses)