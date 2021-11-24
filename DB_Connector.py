from neo4j import GraphDatabase


class DBConnector:
    street = []
    house_number = []

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def neo_transaction(self, address):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._create_address, address)

    @staticmethod
    def _create_address(tx, address):
        street = address["street"]
        house_number = address["house_number"]
        id = address["id"]
        post_code = address["post_code"]
        city = address["city"]
        district = address["district"]
        geojson_geometry = address["geojson_geometry"]

        query = "CREATE (adress:Address_Test{id:$id,street:$street,house_number:$house_number,post_code:$post_code," \
                "city:$city,district:$district,geojson_geometry:$geojson_geometry}) "
        tx.run(query, street=street, house_number=house_number, id=id, post_code=post_code, district=district,
               city=city, geojson_geometry=geojson_geometry)

if __name__ == "__main__":
    connector = DBConnector("bolt://localhost:7687", "neo4j", "test")
    connector.neo_transaction(
        {"street": "Katzensteig", "house_number": "2", "id": "5", "post_code": "78120", "city": "Furtwangen",
         "district": "1", "geojson_geometry": "test"})
