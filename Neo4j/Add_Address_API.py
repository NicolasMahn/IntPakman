from neo4j import GraphDatabase
import Passwords as con


class AddAddress:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def neo_transaction_create(self, address):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            session.write_transaction(
                self._create_address, address)

    def neo_transaction_match(self, address):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            session.write_transaction(
                self._match_addresses, address)

    @staticmethod
    def _create_address(tx, address):
        a_id = address.get("id")
        street = address.get("street")
        house_number = address.get("house_number")
        post_code = address.get("post_code")
        city = address.get("city")
        district = address.get("district")
        geojson_geometry = address.get("geojson_geometry")
        post_station_id = address.get("post_station_id")

        createQuery = """CREATE (a:Address{id:$id,street:$street,house_number:$house_number,post_code:$post_code,
                            city:$city,district:$district,geojson_geometry:$geojson_geometry,
                            post_station_id:$post_station_id})"""
        tx.run(createQuery, id=a_id, street=street, house_number=house_number, post_code=post_code, city=city,
               district=district, geojson_geometry=geojson_geometry, post_station_id=post_station_id)

    @staticmethod
    def _match_addresses(tx, address):
        post_station_id = address.get("post_station_id")

        matchQuery = """MATCH (p:PostStation), (a:Address)
                            WHERE p.id=$post_station_id AND a.post_station_id=$post_station_id
                            CREATE (a)-[r:PART_OF]->(p)"""

        tx.run(matchQuery, post_station_id=post_station_id)


def add_address_to_db(data):
    connector = AddAddress(con.get_uri(), con.get_user(), con.get_password())
    connector.neo_transaction_create(data)
    connector.neo_transaction_match(data)
