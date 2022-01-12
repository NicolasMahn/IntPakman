from neo4j import GraphDatabase


class GetPrioStatusPackages:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def neo_transaction(self, post_station_id, district, date):
        with self.driver.session() as session:
            result = session.write_transaction(
                self._get_prio_status_packages, post_station_id, district, date)

            return result

    @staticmethod
    def _get_prio_status_packages(tx, post_station_id, district, date):
        query = """MATCH (a:Address)<-[:DELIVERED_TO]-(p:Package) 
                   WHERE a.district=$district 
                   RETURN a.id, p.prio"""
                   # AND a.post_station_id=$post_station_id AND p.date=$date
        result = tx.run(query, post_station_id=post_station_id, district=district, date=date)
        values = []
        for record in result:
            values.append(record.data())

        return values


def get_prio_status_packages(post_station_id: int, district: int, date: str):
    connector = GetPrioStatusPackages("bolt://192.52.37.239:7687", "neo4j", "test")
    return connector.neo_transaction(str(post_station_id), str(district), date)