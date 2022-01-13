from neo4j import GraphDatabase


class GetAllAddresses:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def neo_transaction(self, post_station_id, district):
        with self.driver.session() as session:
            result = session.write_transaction(
                self._get_addresses, post_station_id, district)

            return result

    @staticmethod
    def _get_addresses(tx, post_station_id, district):
        query = """MATCH (n:Address) 
                   WHERE n.district=$district AND n.post_station_id=$post_station_id
                   WITH DISTINCT n RETURN n"""
        result = tx.run(query, post_station_id=post_station_id, district=district)
        values = []
        for record in result:
            values.append(record.data())

        return values


def get_all_addresses(post_station_id: int, district: int):
    connector = GetAllAddresses("bolt://192.52.37.239:7687", "neo4j", "test")
    return connector.neo_transaction(str(post_station_id), str(district))