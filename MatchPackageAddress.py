from neo4j import GraphDatabase
import pandas as pd


class MatchPackageAddress:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()


    def neo_transaction_match(self, packages):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            session.write_transaction(
                self._match_package, packages)


    @staticmethod
    def _match_package(tx, packages):
        for i in range(len(packages)):
            sendungsnummer = str(packages.loc[i, "Sendungsnummer"])
            length_cm = str(packages.loc[i, "length_cm"])
            width_cm = str(packages.loc[i, "width_cm"])
            height_cm = str(packages.loc[i, "height_cm"])
            weight_in_g = str(packages.loc[i, "weight_in_g"])
            fragile = str(packages.loc[i, "fragile"])
            perishable = str(packages.loc[i, "perishable"])
            street = str(packages.loc[i, "street"])
            house_number = str(packages.loc[i, "house_number"])
            post_code = str(packages.loc[i, "post_code"])
            city = str(packages.loc[i, "city"])

            '''
            matchQuery = "MATCH (p:Package), (a:Address) " \
                         "WHERE p.street=$street AND a.street=$street " \
                         "AND p.house_number=$house_number AND a.house_number=$house_number " \
                         "AND p.post_code=$post_code AND a.post_code=$post_code " \
                         "AND p.city=$city AND a.city=$city " \
                         "CREATE (p)-[r:DELIVERED_TO]->(a)"
            '''
            matchQuery = "MATCH (p:Package), (a:Address) " \
                         "WHERE p.street='Berliner Straße' AND a.street='Berliner Straße' " \
                         "AND p.house_number='17' AND a.house_number='17' " \
                         "CREATE (p)-[r:DELIVERED_TO]->(a)"
            tx.run(matchQuery, street=street, house_number=house_number, post_code=post_code, city=city)


if __name__ == "__main__":
    connector = MatchPackageAddress("bolt://localhost:7687", "neo4j", "test")
    packages = pd.read_csv('data/random_paketdaten.csv', sep=',')
    connector.neo_transaction_match(packages)