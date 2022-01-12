from neo4j import GraphDatabase


class GetDistances:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def neo_transaction_station_addresses(self):
        with self.driver.session() as session:
            result = session.write_transaction(
                self._get_distance_station_addresses)

            return result

    @staticmethod
    def _get_distance_station_addresses(tx):
        query = 'MATCH (s:PostStation)-[r:DISTANCE_TO]->(a:Address) WHERE s.id="1" AND a.id="9" RETURN s.id,a.id,r.distance,r.duration'
        #query = 'MATCH (s:PostStation)-[r:DISTANCE_TO]->(a:Address) RETURN s.id,a.id,r.distance,r.duration'
        result = tx.run(query)
        values = []
        for record in result:
            values.append(record.data())

        return values


    def neo_transaction_addresses_addresses(self):
        with self.driver.session() as session:
            result = session.write_transaction(
                self._get_distance_addresses_addresses)

            return result

    @staticmethod
    def _get_distance_addresses_addresses(tx):
        query = 'MATCH (a1:Address)-[r:DISTANCE_TO]->(a2:Address) RETURN a1.id,a2.id,r.distance,r.duration'
        result = tx.run(query)
        values = []
        for record in result:
            values.append(record.data())

        return values


def get_distance_station_addresses():
    connector = GetDistances("bolt://192.52.37.239:7687", "neo4j", "test")
    return connector.neo_transaction_station_addresses()


def get_distance_addresses_addresses():
    connector = GetDistances("bolt://192.52.37.239:7687", "neo4j", "test")
    return connector.neo_transaction_addresses_addresses()


def get_distance_between_all():
    reslut_list = get_distance_station_addresses()
    reslut_list.extend(get_distance_addresses_addresses())
    return reslut_list