from neo4j import GraphDatabase


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
        query = "MATCH(n:Address_Test) RETURN n"
        result = tx.run(query)
        values = []
        for record in result:
            values.append(record.data())

        return values
    @staticmethod
    def calculate_distance(node_a, node_b):
        print("tbd")


    @staticmethod
    def _add_distance(tx, results):
        distance_list = []
        for x in range(len(results)):
            entry = results[0]
            id_a = entry["n"]["id"]
            results.pop(0)
            distance_list = results
            for y in range(len(distance_list)):
                distance = tx.calculate_distance(entry["n"], distance_list[y]["n"])
                id_b = distance_list[y]["n"]["id"]
                query = """MATCH(a:Address_Test),(b:Address_Test) 
                           WHERE a.id = $id_a AND b.id = $id_b
                           CREATE (a)-[r:DISTANCE_TO {distance: $distance}]->(b)-[d:DISTANCE_TO {distance:$distance}]->(a) """
                tx.run(query, id_a=id_a, id_b=id_b, distance=distance)


if __name__ == "__main__":
    connector = DistanceCalculator("bolt://localhost:7687", "neo4j", "test")
    addresses = connector.neo_transaction()
    connector.add_relationship(addresses)
