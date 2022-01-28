from neo4j import GraphDatabase
import Passwords as con


class GetDistances:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def neo_transaction_station_addresses(self, post_station_id, district, date):
        with self.driver.session() as session:
            result = session.write_transaction(
                self._get_distance_station_addresses, post_station_id, district, date)

            return result

    @staticmethod
    def _get_distance_station_addresses(tx, post_station_id, district, date):
        '''query = """MATCH (s:PostStation)-[r:DISTANCE_TO]->(a:Address)
                   WHERE s.id=$post_station_id AND a.district=$district AND a.post_station_id=$post_station_id
                   RETURN s.id,a.id,r.distance,r.duration"""'''
        query = """MATCH (s:PostStation)-[r:DISTANCE_TO]->(a:Address)<-[r2:DELIVERED_TO]-(p2:Package {date:$date}) 
                   WHERE s.id=$post_station_id AND a.district=$district AND a.post_station_id=$post_station_id
                   RETURN DISTINCT s.id,a.id,r.distance,r.duration"""
        result = tx.run(query, post_station_id=post_station_id, district=district, date=date)
        values = []
        for record in result:
            values.append(record.data())

        return values

    def neo_transaction_addresses_addresses(self, post_station_id, district, date):
        with self.driver.session() as session:
            result = session.write_transaction(
                self._get_distance_addresses_addresses, post_station_id, district, date)

            return result

    @staticmethod
    def _get_distance_addresses_addresses(tx, post_station_id, district, date):
        query = """MATCH (p1:Package {date:$date})-[r1:DELIVERED_TO]->(a1:Address)-[r:DISTANCE_TO]->(a2:Address)<-[r2:DELIVERED_TO]-(p2:Package {date:$date}) 
                   WHERE a1.district=$district AND a2.district=$district AND a1.post_station_id=$post_station_id AND a2.post_station_id=$post_station_id 
                   RETURN DISTINCT a1.id,a2.id,r.distance,r.duration"""
        result = tx.run(query, post_station_id=post_station_id, district=district, date=date)
        values = []
        for record in result:
            values.append(record.data())

        return values


def get_distance_station_addresses(post_station_id: int, district: int, date: str):
    connector = GetDistances(con.get_uri(), con.get_user(), con.get_password())
    return connector.neo_transaction_station_addresses(str(post_station_id), str(district), date)


def get_distance_addresses_addresses(post_station_id: int, district: int, date: str):
    connector = GetDistances(con.get_uri(), con.get_user(), con.get_password())
    return connector.neo_transaction_addresses_addresses(str(post_station_id), str(district), date)


def get_distance_between_all(post_station_id: int, district: int, date: str):
    reslut_list = get_distance_station_addresses(post_station_id, district, date)
    reslut_list.extend(get_distance_addresses_addresses(str(post_station_id), str(district), date))
    return reslut_list
