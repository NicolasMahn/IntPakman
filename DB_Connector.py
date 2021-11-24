from neo4j import GraphDatabase


class HelloWorldExample:
    street = []
    house_number = []

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def print_delivered_adresses(self, message):
        with self.driver.session() as session:
            greeting = session.write_transaction(self._create_and_return_greeting, message)
            print(greeting)

    @staticmethod
    def _create_and_return_greeting(tx):
        result = tx.run("LOAD CSV FROM 'file:///adresses.csv' AS line"
        +"CREATE(: Artist"
        +"{name: line[1], year: toInteger(line[2])})", message=message)

    return result.single()[0]


if __name__ == "__main__":
    greeter = HelloWorldExample("bolt://localhost:7687", "neo4j", "test")
    greeter.print_delivered_adresses("hello, world")
    greeter.close()
