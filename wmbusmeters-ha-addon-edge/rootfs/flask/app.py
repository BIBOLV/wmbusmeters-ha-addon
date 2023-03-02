import json, requests, os
from flask import Flask, jsonify, render_template, request
from waitress import serve

app = Flask(__name__)

CFG_GET_URL = "http://supervisor/addons/self/options/config"
CFG_SET_URL = "http://supervisor/addons/self/options"
RESTART_URL = "http://supervisor/addons/self/restart"
URL_HEADER = { "Authorization": "Bearer " + os.environ.get('SUPERVISOR_TOKEN'), "content-type": "application/json" }

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/save_json', methods=['POST'])
def save_json():
    request_json = request.json
	data = request_json['data']
    try:
        # Save the updated JSON back to the URL
        response = requests.post(CFG_SET_URL, headers=URL_HEADER, json=data)
        response.raise_for_status()

        # Call the addon restart API if the config update was successful
        response = requests.post(RESTART_URL, headers=URL_HEADER)
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        # Handle any errors that occur during the request
        error_message = str(e)
        return jsonify({'error': error_message}), 500

    except ValueError as e:
        # Handle any errors that occur while parsing the JSON data
        error_message = str(e)
        return jsonify({'error': error_message}), 400

    return jsonify({'message': 'Data saved successfully and addon restarted.'})


@app.route('/get_json')
def get_json():
    try:
        # Attempt to retrieve the JSON data from the URL
        response = requests.get(CFG_URL, headers=URL_HEADER)
        response.raise_for_status()
        data = response.json()

    except requests.exceptions.RequestException as e:
        # Handle any errors that occur during the request
        error_message = str(e)
        return jsonify({'error': error_message}), 500

    except ValueError as e:
        # Handle any errors that occur while parsing the JSON data
        error_message = str(e)
        return jsonify({'error': error_message}), 400

    return jsonify(data)

if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=5000)
