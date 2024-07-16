from flask import Flask, render_template, jsonify
import requests

import time
import os


app_url = os.getenv('APP_URL', "http://127.0.0.1:5000" )

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/intermediary', methods=['GET'])
def intermediary():
    try:
        response = requests.get(f'{app_url}/get_analytics')
        response.raise_for_status()
        data = response.json()
        return jsonify(data)
    except Exception as e:
        print(f"Request failed: {e}")
        return jsonify({"error": "Failed requesting get_analytics"}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True, host='0.0.0.0')
