from neo4j import GraphDatabase
import pandas as pd


class AddAddresses:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def neo_transaction_create(self, addresses):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            session.write_transaction(
                self._create_address, addresses)

    def neo_transaction_match(self, addresses):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            session.write_transaction(
                self._match_addresses, addresses)

    @staticmethod
    def _create_address(tx, addresses):
        for i in range(len(addresses)):
            a_id = str(addresses.loc[i, "id"])
            street = str(addresses.loc[i, "street"])
            house_number = str(addresses.loc[i, "house_number"])
            post_code = str(addresses.loc[i, "post_code"])
            city = str(addresses.loc[i, "city"])
            district = str(addresses.loc[i, "district"])
            geojson_geometry = str(addresses.loc[i, "geojson_geometry"])
            post_station_id = str(addresses.loc[i, "post_station_id"])

            createQuery = """CREATE (a:Address{id:$id,street:$street,house_number:$house_number,post_code:$post_code,
                            city:$city,district:$district,geojson_geometry:$geojson_geometry,
                            post_station_id:$post_station_id})"""
            tx.run(createQuery, id=a_id, street=street, house_number=house_number, post_code=post_code, city=city,
                   district=district, geojson_geometry=geojson_geometry, post_station_id=post_station_id)

    @staticmethod
    def _match_addresses(tx, addresses):
        for i in range(len(addresses)):
            post_station_id = str(addresses.loc[i, "post_station_id"])

            matchQuery = """MATCH (p:PostStation), (a:Address)
                            WHERE p.id=$post_station_id AND a.post_station_id=$post_station_id
                            CREATE (a)-[r:PART_OF]->(p)"""

            tx.run(matchQuery, post_station_id=post_station_id)


def load_data(path_data):
    return pd.read_csv(path_data, sep=';')


def add_address_to_db(path_data):
    connector = AddAddresses("bolt://192.52.37.239:7687", "neo4j", "test")
    addresses = load_data(path_data)
    connector.neo_transaction_create(addresses)
    #connector.neo_transaction_match(addresses)
