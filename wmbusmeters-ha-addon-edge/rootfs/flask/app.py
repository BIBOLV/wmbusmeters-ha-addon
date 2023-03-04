import json, requests, os
from flask import Flask, jsonify, render_template, request
from waitress import serve

app = Flask(__name__, static_url_path='')

cfgfile = '/data/options.json'
RESTART_URL = "http://supervisor/addons/self/restart"
URL_HEADER = { "Authorization": "Bearer " + os.environ.get('SUPERVISOR_TOKEN'), "content-type": "application/json" }

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/save_json', methods=['POST'])
def save_json_to_file():
    try:
        request_json = request.json
        data = request_json['data']
        with open(cfgfile, 'w') as file:
            json.dump(data, file, indent=True)

    except ValueError as e:
        error_message = str(e)
        return jsonify({'error': error_message}), 400

    return jsonify({'message': 'Data saved successfully and addon restarted.'})

    response = requests.post(RESTART_URL, headers=URL_HEADER)


@app.route('/get_json')
def get_json():
    try:
        with open(cfgfile, 'r') as file:
            data = json.load(file)
            return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    #serve(app, host="127.0.0.1", port=5000)
    app.debug = True
    app.run(host="127.0.0.1")