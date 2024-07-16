from flask import Flask, jsonify, request
import os 
import shutil
import datetime
import requests
import multiprocessing

train_model_event = multiprocessing.Event()

app = Flask(__name__)

def train_model_task(train_model_event):
    train_model_event.wait()
    content = str(datetime.datetime.now())
    print(content)
    file_path = "checkpoints_local/model.txt"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    try:
        with open(file_path, 'w') as file:
            file.write(content)
        print(f"File '{file_path}' has been successfully created and written.")
    except IOError as e:
        print(f"Failed to create or write to the file: {e}")

    try:
        source_path = 'checkpoints_local/model.txt'
        destination_path = 'checkpoints_volume/model.txt'  
        shutil.copy(source_path, destination_path)
        print('model written sucsessfilly')
    except Exception as e:
        print(f"An error while updating model: {e}")
    try:
        requests.post("http://host.docker.internal:5002/update_model")
    except Exception as e:
        print(f"An error while sending post signal to 5002 port: {e}")


@app.route('/train_model', methods=['POST'])
def train_model():
    train_model_event.set()
    print("POST arriver (train_model)")
    return jsonify({"message": "Model train event triggered"}), 200



if __name__ == '__main__':
    p = multiprocessing.Process(target=train_model_task, args=(train_model_event,))
    p.start()

    app.run(port=5003, debug=True, host='0.0.0.0')
    p.kill()

