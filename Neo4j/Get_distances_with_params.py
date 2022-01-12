from neo4j import GraphDatabase


class GetDistances:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def neo_transaction_station_addresses(self, post_station_id, district):
        with self.driver.session() as session:
            result = session.write_transaction(
                self._get_distance_station_addresses, post_station_id, district)

            return result

    @staticmethod
    def _get_distance_station_addresses(tx, post_station_id, district):
        query = """MATCH (s:PostStation)-[r:DISTANCE_TO]->(a:Address) 
                   WHERE s.id=$post_station_id AND a.district=$district 
                   RETURN s.id,a.id,r.distance,r.duration""" #AND a.post_station_id=$post_station_id
        result = tx.run(query, post_station_id=post_station_id, district=district)
        values = []
        for record in result:
            values.append(record.data())

        return values

    def neo_transaction_addresses_addresses(self, post_station_id, district):
        with self.driver.session() as session:
            result = session.write_transaction(
                self._get_distance_addresses_addresses, post_station_id, district)

            return result

    @staticmethod
    def _get_distance_addresses_addresses(tx, post_station_id, district):
        query = """MATCH (a1:Address)-[r:DISTANCE_TO]->(a2:Address) 
                   WHERE a1.district=$district AND a2.district=$district 
                   RETURN a1.id,a2.id,r.distance,r.duration"""
        result = tx.run(query, post_station_id=post_station_id, district=district)
        values = []
        for record in result:
            values.append(record.data())

        return values


def get_distance_station_addresses(post_station_id: int, district: int):
    connector = GetDistances("bolt://192.52.37.239:7687", "neo4j", "test")
    return connector.neo_transaction_station_addresses(str(post_station_id), str(district))


def get_distance_addresses_addresses(post_station_id: int, district: int):
    connector = GetDistances("bolt://192.52.37.239:7687", "neo4j", "test")
    return connector.neo_transaction_addresses_addresses(str(post_station_id), str(district))


def get_distance_between_all(post_station_id: int, district: int):
    reslut_list = get_distance_station_addresses(post_station_id, district)
    reslut_list.extend(get_distance_addresses_addresses(str(post_station_id), str(district)))
    return reslut_list
