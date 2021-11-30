from neo4j import GraphDatabase


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
    connector = GetAddressesWithPackages("bolt://192.52.37.239:7687", "neo4j", "test")
    return connector.neo_transaction()