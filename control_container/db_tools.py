import mysql.connector
import pyshark
from typing import List
import datetime
import re as regex


class Entity:

    def __init__(self, id=None, unix_time=None, source_ip=None, destination_ip=None, protocol=None, byte_size=None, anomaly_marker=None):
        self.id:int = id
        self.unix_time: datetime.datetime = unix_time
        self.source_ip:str = source_ip
        self.destination_ip:str = destination_ip
        self.protocol:str = protocol
        self.byte_size:int = byte_size
        self.anomaly_marker:int = anomaly_marker
    
    @classmethod
    def fromDB(cls, query: list):
        return cls(*query)

    def asList(self):
        return  [self.id, self.unix_time, self.source_ip, self.destination_ip, self.protocol, self.byte_size, self.anomaly_marker]


    

class DataBase:
    def __init__(self):
        self.DB_CONNECT_INFO = {
            "user": "root",
            "password": "root",
            "host": "host.docker.internal",
            "port": "3306",
            "database": "traffic"
        }

    def get_records(self)-> List[Entity]:
        records = []
        try:
            with mysql.connector.connect(**self.DB_CONNECT_INFO) as connection:
                cursor = connection.cursor()
                cursor.execute('SELECT * FROM traffic')
                records = cursor.fetchall()
                records = [Entity.fromDB(q) for q in records]
        except Exception as e:
            print(f"An error occurred: {e}")

        return records


    def add_record(self, record: Entity) -> None:
        try:
            with mysql.connector.connect(**self.DB_CONNECT_INFO) as connection:
                cursor = connection.cursor()
                query = """
                    INSERT INTO traffic (UnixTime, SourceIp, DestinationIp, Protocol, ByteSize, AnomalyMarker)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                values = (record.unix_time, record.source_ip, record.destination_ip, record.protocol, record.byte_size, record.anomaly_marker)
                
                cursor.execute(query, values)
                connection.commit() 
            
                print("New record added successfully.")
        
        except Exception as e:
            print(f"An error occurred: {e}")

    def add_records(self, records: list) -> None:
        try:
            with mysql.connector.connect(**self.DB_CONNECT_INFO) as connection:
                cursor = connection.cursor()
                for record in records:
                    query = """
                        INSERT INTO traffic (UnixTime, SourceIp, DestinationIp, Protocol, ByteSize, AnomalyMarker)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    values = (record.unix_time, record.source_ip, record.destination_ip, record.protocol, record.byte_size, record.anomaly_marker)
                    
                    cursor.execute(query, values)
                connection.commit()
            
                print(f"{len(records)} records added successfully.")
        
        except Exception as e:
            print(f"An error occurred: {e}")


    def delete_record_by_id(self, record_id)->None:
        try:
            with mysql.connector.connect(**self.DB_CONNECT_INFO) as connection:
                cursor = connection.cursor()
                query = "DELETE FROM traffic WHERE RecordID = %s"
                values = (record_id,)
                
                cursor.execute(query, values)
                connection.commit() 
                
                print(f"{cursor.rowcount} record(s) deleted")
                
        except Exception as e:
            print(f"An error occurred: {e}")
            
    def edit_record_by_id(self, record_id, record: Entity) -> None:
        try:
            with mysql.connector.connect(**self.DB_CONNECT_INFO) as connection:
                cursor = connection.cursor()
                
                # Construct the UPDATE query based on the Entity class attributes
                query = """
                    UPDATE traffic
                    SET UnixTime = %s, SourceIp = %s, DestinationIp = %s, Protocol = %s, ByteSize = %s, AnomalyMarker = %s
                    WHERE RecordID = %s
                """
                # Prepare the values tuple from the Entity instance attributes
                values = (record.unix_time, record.source_ip, record.destination_ip, record.protocol, record.byte_size, record.anomaly_marker, record_id)
                
                cursor.execute(query, values)
                connection.commit() 
            
                print(f"{cursor.rowcount} record(s) updated")

        except Exception as e:
            print(f"An error occurred: {e}")

    def edit_records(self, records):
        try:
            with mysql.connector.connect(**self.DB_CONNECT_INFO) as connection:
                cursor = connection.cursor()
                rowcount=0
                for record in records:
                    if record.id:
                        query = """
                            UPDATE traffic
                            SET UnixTime = %s, SourceIp = %s, DestinationIp = %s, Protocol = %s, ByteSize = %s, AnomalyMarker = %s
                            WHERE RecordID = %s
                        """
                        values = (record.unix_time, record.source_ip, record.destination_ip, record.protocol, record.byte_size, record.anomaly_marker, record.id)

                        cursor.execute(query, values)
                        rowcount+=cursor.rowcount

                connection.commit()

                print(f"{rowcount} record(s) updated")

        except Exception as e:
            print(f"An error occurred: {e}")

    def custom_cursor(self, query) -> List[Entity]:
        try:
            with mysql.connector.connect(**self.DB_CONNECT_INFO) as connection:
                cursor = connection.cursor()
                cursor.execute(query)
                result = cursor.fetchall()
                result = [Entity.fromDB(q) for q in result]
                cursor.close()
                return result
        
        except Exception as e:
            print(f"An error occurred: {e}")
            return []
        

def readDumpFile(file_path: str) -> List[Entity]:
    entities = []  
    try:
        with pyshark.FileCapture(file_path) as cap:
            for record in cap:
                unix_time = float(record.frame_info.time_epoch)
                unix_time_str = datetime.datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d %H:%M:%S')
                source_ip = record.ip.src
                destination_ip = record.ip.dst
                if 'IPV6 Layer' in str(record.layers):
                    protocol = regex.search(r'(Next Header:)(.*)', str(record.ipv6))
                    protocol_type = protocol.group(2).strip().split(' ')[0]
                    protocol_number = protocol.group(2).strip().split(' ')[1]
                elif 'IP Layer' in str(record.layers):
                    protocol = regex.search(r'(Protocol:)(.*)', str(record.ip))
                    protocol_type = protocol.group(2).strip().split(' ')[0]
                    protocol_number = protocol.group(2).strip().split(' ')[1]
                byte_size = int(record.length) 
                anomaly_marker = None

                entity = Entity(unix_time=unix_time_str, source_ip=source_ip, destination_ip=destination_ip, protocol=protocol_number, byte_size=byte_size, anomaly_marker=anomaly_marker)
                entities.append(entity)
    except Exception as e:
        print(f"An error occurred while reading the dump file: {e}")
    return entities



