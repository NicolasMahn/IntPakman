from neo4j import GraphDatabase


class GetAddressesWithPackages:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def neo_transaction(self, post_station_id, district, date):
        with self.driver.session() as session:
            result = session.write_transaction(
                self._get_addresses, post_station_id, district, date)

            return result

    @staticmethod
    def _get_addresses(tx, post_station_id, district, date):
        query = """MATCH (n:Address)<-[:DELIVERED_TO]-(p:Package) 
                   WHERE n.district=$district AND n.post_station_id=$post_station_id AND p.date=$date 
                   WITH DISTINCT n RETURN n"""
                   # AND n.post_station_id=$post_station_id AND p.date=$date
        result = tx.run(query, post_station_id=post_station_id, district=district, date=date)
        values = []
        for record in result:
            values.append(record.data())

        return values


def get_addresses_with_packages(post_station_id: int, district: int, date: str):
    connector = GetAddressesWithPackages("bolt://192.52.37.239:7687", "neo4j", "test")
    return connector.neo_transaction(str(post_station_id), str(district), date)