from neo4j import GraphDatabase
import Passwords as con


class GetPrioStatusPackages:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def neo_transaction(self):
        with self.driver.session() as session:
            result = session.write_transaction(
                self._get_prio_status_packages)

            return result

    @staticmethod
    def _get_prio_status_packages(tx):
        query = "MATCH (a:Address)<-[:DELIVERED_TO]-(p:Package) RETURN a.id, p.prio"
        result = tx.run(query)
        values = []
        for record in result:
            values.append(record.data())

        return values


def get_prio_status_packages():
    connector = GetPrioStatusPackages(con.get_uri(), con.get_user(), con.get_password())
    return connector.neo_transaction()