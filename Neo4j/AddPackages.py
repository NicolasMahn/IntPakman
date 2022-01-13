from neo4j import GraphDatabase
import pandas as pd
import pickle
from sklearn.tree import DecisionTreeClassifier


def load_model(model_path, model):
    model = pickle.load(open(model_path, 'rb'))
    return model


class AddPackages:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def neo_transaction_create(self, packages, model):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            session.write_transaction(
                self._create_package, packages, model)


    def neo_transaction_match(self, packages):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            session.write_transaction(
                self._match_package, packages)


    @staticmethod
    def _create_package(tx, packages, model):
        for i in range(len(packages)):
            pred_data = pd.DataFrame(columns=["length_cm", "width_cm", "height_cm", "weight_in_g"])
            pred_data.loc[0] = [
                packages.loc[i, "length_cm"],
                packages.loc[i, "width_cm"],
                packages.loc[i, "height_cm"],
                packages.loc[i, "weight_in_g"]
            ]
            prio = str(model.predict(pred_data)[0])
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
            date = str(packages.loc[i, "date"])

            createQuery = """CREATE (package:Package{sendungsnummer:$sendungsnummer,length_cm:$length_cm,
                            width_cm:$width_cm,height_cm:$height_cm,weight_in_g:$weight_in_g, fragile:$fragile,
                            perishable:$perishable,street:$street,house_number:$house_number,post_code:$post_code,
                            city:$city,prio:$prio,date:$date})"""
            tx.run(createQuery, sendungsnummer=sendungsnummer, length_cm=length_cm, width_cm=width_cm, height_cm=height_cm,
                   weight_in_g=weight_in_g, fragile=fragile, perishable=perishable, street=street,
                   house_number=house_number, post_code=post_code, city=city, prio=prio, date=date)


    @staticmethod
    def _match_package(tx, packages):
        for i in range(len(packages)):
            sendungsnummer = str(packages.loc[i, "Sendungsnummer"])
            street = str(packages.loc[i, "street"])
            house_number = str(packages.loc[i, "house_number"])
            post_code = str(packages.loc[i, "post_code"])
            city = str(packages.loc[i, "city"])


            matchQuery = """MATCH (p:Package), (a:Address)
                            WHERE p.street=$street AND a.street=$street
                            AND p.house_number=$house_number AND a.house_number=$house_number
                            AND p.post_code=$post_code AND a.post_code=$post_code
                            AND p.city=$city AND a.city=$city
                            AND p.sendungsnummer=$sendungsnummer
                            CREATE (p)-[r:DELIVERED_TO]->(a)"""

            tx.run(matchQuery, street=street, house_number=house_number, post_code=post_code, city=city,
                   sendungsnummer=sendungsnummer)


def load_data(path_data):
    return pd.read_csv(path_data, sep=',')


def add_packages_to_db(path_data, path_model):
    connector = AddPackages("bolt://192.52.37.239:7687", "neo4j", "test")
    packages = load_data(path_data)
    model = DecisionTreeClassifier()
    model = load_model(path_model, model)
    connector.neo_transaction_create(packages, model)
    connector.neo_transaction_match(packages)