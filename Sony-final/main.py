from flask import Flask, jsonify, request
import json
import requests
 
app = Flask(__name__)
 
DATA_FILE = "data.json"
API_URL = "https://www.travel-advisory.info/api"
 
 
def load_data():
        with open(DATA_FILE, 'r') as file:
            data = json.load(file)
        return data
 
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok" })
 
@app.route('/diag', methods=['GET'])
def diag():
        response = requests.get(API_URL)
        #response.raise_for_status()
        api_status = {"api_status": {"code": response.status_code }}
        return jsonify(api_status)
 
@app.route('/convert', methods=['GET'])
def convert():
    country_name = request.args.get('countryName')
 
    if not country_name:
        return jsonify({"error": "Country name not provided"}), 400
 
    data = load_data()
 
    if not data:
        return jsonify({"error": "Error loading data"}), 500
 
    for country_code, country_data in data['data'].items():
        if country_data.get('name') == country_name:
            country_code = country_data.get('iso_alpha2', None)
            if country_code:
                return jsonify({"country_code": country_code})
            else:
                return jsonify({"error": "code not found for the country"}), 404
 
    return jsonify({"error": "Country not found"}), 404
 
 
if __name__ == '__main__':
    data = load_data()
    app.run(debug=True , host="0.0.0.0")