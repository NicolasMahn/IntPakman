from neo4j import GraphDatabase


class GetPostStation:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def neo_transaction(self, post_station_id):
        with self.driver.session() as session:
            result = session.write_transaction(
                self._get_addresses, post_station_id)

            return result

    @staticmethod
    def _get_addresses(tx, post_station_id):
        query = """MATCH (s:PostStation) 
                   WHERE s.id=$post_station_id
                   RETURN s"""
        result = tx.run(query, post_station_id=post_station_id)
        values = []
        for record in result:
            values.append(record.data())

        return values


def get_post_station(post_station_id: int):
    connector = GetPostStation("bolt://192.52.37.239:7687", "neo4j", "test")
    return connector.neo_transaction(str(post_station_id))