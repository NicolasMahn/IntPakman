from neo4j import GraphDatabase
import Neo4j.DB_Connection as con


class GetAllPackages:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def neo_transaction(self, post_station_id, district, date):
        with self.driver.session() as session:
            result = session.write_transaction(
                self._get_packages, post_station_id, district, date)

            return result

    @staticmethod
    def _get_packages(tx, post_station_id: int, district: int, date: str):
        query = """MATCH (a:Address)<-[:DELIVERED_TO]-(p:Package) 
                   WHERE a.district=$district AND a.post_station_id=$post_station_id AND p.date=$date 
                   RETURN a, p"""
        result = tx.run(query, post_station_id=post_station_id, district=district, date=date)
        values = []
        for record in result:
            values.append(record.data())

        return values


def get_all_packages(post_station_id: int, district: int, date: str):
    connector = GetAllPackages(con.get_uri(), con.get_user(), con.get_password())
    return connector.neo_transaction(str(post_station_id), str(district), date)