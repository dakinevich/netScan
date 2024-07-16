from db_tools import Entity, DataBase
from typing import List
import pyshark
import datetime
import re as regex

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
es = readDumpFile('traffic_capture/sample.pcapng')
for e in es:
    print(e.asList())
exit(0)

db = DataBase()
en = Entity(None, 12,12,None)
db.add_record(en)
print([e.asList() for e in db.get_records()])