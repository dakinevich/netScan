import time
import threading
import os
from queue import Queue
import datetime

import shutil
import pyshark
import requests


app_url = os.getenv('APP_URL', "http://127.0.0.1:5000" )

task_queue = Queue()

def worker():
    while True:
        file_path = task_queue.get() 
        try:
            send_traffic(file_path)
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
        finally:
            task_queue.task_done() 

def send_traffic(file_path):
    filename = file_path.split('/')[-1] 
    response = None
    with open(file_path, 'rb') as file:
        files = {'file': (filename, file)}
        response = requests.post(app_url, files=files)
    if response:
        if response.status_code == 202:
            print("File uploaded successfully.")
            os.remove(file_path)
        else:
            print(f"Failed to upload file. Status code: {response.status_code}")
    else:
        print("Failed to get response")
    

def capture_traffic_loop():
    while True:
        try:
            time.sleep(5)
        except Exception as e:
            print(f"Breaking loop: {e}")
            break

        stump = ''.join([i if i.isdigit() else '_' for i in str(datetime.datetime.now())])
        source_file = "sample.pcapng"
        destination_dir = f"send_queue/"
        os.makedirs(destination_dir, exist_ok=True)
        destination_path = f"send_queue/{stump}.pcapng"
        shutil.copy(source_file, destination_path)
        task_queue.put(f'send_queue/{stump}.pcapng')

t = threading.Thread(target=worker)
t.start()
    

capture_traffic_loop()
t.join()