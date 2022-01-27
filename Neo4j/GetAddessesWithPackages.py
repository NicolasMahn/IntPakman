from neo4j import GraphDatabase
import Neo4j.DB_Connection as con


class GetAddressesWithPackages:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def neo_transaction(self):
        with self.driver.session() as session:
            result = session.write_transaction(
                self._get_addresses)

            return result

    @staticmethod
    def _get_addresses(tx):
        query = "MATCH (n:Address)<-[:DELIVERED_TO]-(:Package) WITH DISTINCT n RETURN n"
        result = tx.run(query)
        values = []
        for record in result:
            values.append(record.data())

        return values


def get_addresses_with_packages():
    connector = GetAddressesWithPackages(con.get_uri(), con.get_user(), con.get_password())
    return connector.neo_transaction()