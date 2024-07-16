from flask import Flask, jsonify, request
import os
import multiprocessing
from db_tools import Entity, DataBase
import tensorflow
import random
import time
import shutil

update_model_event = multiprocessing.Event()

app = Flask(__name__)

def neural_network(update_model_event):
    while True:
        time.sleep(1)
        if update_model_event.is_set():
            print("Updating model")
            try:
                source_path = 'checkpoints_volume/model.txt'  
                destination_path = 'checkpoints_local/model.txt'
                shutil.copy(source_path, destination_path)
                with open(destination_path, 'r') as f:
                    lines = f.readlines()
                    print('new model with content: ', lines)
                print('model updated sucsessfilly')
            except Exception as e:
                print(f"An error while updating model: {e}")
            #TODO  replace model(checkpoints/model.txt) with file in docker volume (/checkpoints/model.txt)
            update_model_event.clear()

        db = DataBase()
        entities = db.custom_cursor("SELECT * FROM traffic WHERE AnomalyMarker IS NULL")
        if entities:
            for i in range(len(entities)):
                anomaly =  random.random()>0.9
                entities[i].anomaly_marker = anomaly
            db.edit_records(entities)





@app.route('/update_model', methods=['POST'])
def update_model():
    update_model_event.set()
    print("POST arriver (update_model)")
    return jsonify({"message": "Model update event triggered"}), 200



if __name__ == '__main__':
    p = multiprocessing.Process(target=neural_network, args=(update_model_event,))
    p.start()

    app.run(port=5002, debug=True, host='0.0.0.0')
    p.kill()