from db_tools import Entity, DataBase
import requests


requests.post("http://host.docker.internal:5003/train_model")

exit(0)
db = DataBase()
db.DB_CONNECT_INFO = {
            "user": "root",
            "password": "root",
            "host": "localhost",
            "port": "3306",
            "database": "traffic"
        }

entities = db.custom_cursor("DELETE FROM traffic")

entities = db.custom_cursor("SELECT * FROM traffic")

print(entities)
exit(0)
rs = [r.asList() for r in entities]
print(rs)

import requests

url = 'http://localhost:5002/update_model'

response = requests.post(url)

if response.status_code == 200:
    print("Model updated successfully")
else:
    print(f"Failed to update model, received status code: {response.status_code}")



exit(0)