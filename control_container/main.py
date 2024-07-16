from flask import Flask, jsonify, request
import os
import multiprocessing
from multiprocessing import Queue
from db_tools import Entity, DataBase, readDumpFile
import pyshark


task_queue = Queue()

app = Flask(__name__)

def worker(task_queue):
    while True:
        file_path = task_queue.get()
        if file_path is None: 
            break
        try:
            prepare_file(file_path)
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")


def prepare_file(file_path):
    entities = readDumpFile(file_path)
    db = DataBase()
    db.add_records(entities)

    os.remove(file_path)
    print(f"File {file_path} deleted.")



@app.route('/', methods=['POST'])
def upload_traffic():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and file.filename.endswith('.pcapng'):
        
        uploads_dir = "uploads_queue"
        if not os.path.exists(uploads_dir):
            os.makedirs(uploads_dir)

        file.save(f"uploads_queue/{file.filename}")
        task_queue.put(f"uploads_queue/{file.filename}")
        print(f"Uploaded file: {file.filename}")
        return jsonify({"message": "Traffic data added to queue."}), 202
    else:
        return jsonify({"error": "Invalid file type. Only.pcapng files are allowed."}), 400

@app.route('/get_analytics', methods=['GET'])
def get_analytics():
    db = DataBase()
    records = db.get_records()
    records = [r.asList() for r in records]
    return jsonify(records), 200

if __name__ == '__main__':
    task_queue = Queue()
    p = multiprocessing.Process(target=worker, args=(task_queue,))
    p.start()

    app.run(port=5000, debug=True, host='0.0.0.0')

    p.join()