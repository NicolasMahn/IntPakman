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

    def neo_transaction_create(self, package, model):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            session.write_transaction(
                self._create_package, package, model)

    def neo_transaction_match(self, package):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            session.write_transaction(
                self._match_package, package)

    @staticmethod
    def _create_package(tx, package, model):
        pred_data = pd.DataFrame(columns=["length_cm", "width_cm", "height_cm", "weight_in_g"])
        pred_data.loc[0] = [
            package.get("length_cm"),
            package.get("width_cm"),
            package.get("height_cm"),
            package.get("weight_in_g")
        ]
        prio = str(model.predict(pred_data)[0])
        sendungsnummer = package.get("Sendungsnummer")
        length_cm = package.get("length_cm")
        width_cm = package.get("width_cm")
        height_cm = package.get("height_cm")
        weight_in_g = package.get("weight_in_g")
        fragile = package.get("fragile")
        perishable = package.get("perishable")
        street = package.get("street")
        house_number = package.get("house_number")
        post_code = package.get("post_code")
        city = package.get("city")
        date = package.get("date")

        createQuery = """CREATE (package:Package{sendungsnummer:$sendungsnummer,length_cm:$length_cm,
                            width_cm:$width_cm,height_cm:$height_cm,weight_in_g:$weight_in_g, fragile:$fragile,
                            perishable:$perishable,street:$street,house_number:$house_number,post_code:$post_code,
                            city:$city,prio:$prio,date:$date})"""
        tx.run(createQuery, sendungsnummer=sendungsnummer, length_cm=length_cm, width_cm=width_cm, height_cm=height_cm,
               weight_in_g=weight_in_g, fragile=fragile, perishable=perishable, street=street,
               house_number=house_number, post_code=post_code, city=city, prio=prio, date=date)

    @staticmethod
    def _match_package(tx, package):
        sendungsnummer = package.get("Sendungsnummer")
        street = package.get("street")
        house_number = package.get("house_number")
        post_code = package.get("post_code")
        city = package.get("city")

        matchQuery = """MATCH (p:Package), (a:Address)
                            WHERE p.street=$street AND a.street=$street
                            AND p.house_number=$house_number AND a.house_number=$house_number
                            AND p.post_code=$post_code AND a.post_code=$post_code
                            AND p.city=$city AND a.city=$city
                            AND p.sendungsnummer=$sendungsnummer
                            CREATE (p)-[r:DELIVERED_TO]->(a)"""

        tx.run(matchQuery, street=street, house_number=house_number, post_code=post_code, city=city,
               sendungsnummer=sendungsnummer)


def add_packages_to_db(data):
    connector = AddPackages("bolt://192.52.37.239:7687", "neo4j", "test")
    model = DecisionTreeClassifier()
    path_model = 'Models/model_Classifier_without_volue_V2'
    model = load_model(path_model, model)
    connector.neo_transaction_create(data, model)
    connector.neo_transaction_match(data)
