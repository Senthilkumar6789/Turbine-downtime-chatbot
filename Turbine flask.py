from flask import Flask, request, jsonify
import json
import pandas as pd

dataset = pd.read_csv(r'C:\Users\johns\Downloads\Turbine Downtime.csv')

app = Flask(__name__)

@app.get('/')
def sample_hook():
    return 'Hello From Flask'

@app.route('/webhook', methods=['POST'])
def webhook():
    
    request_data = request.get_json()

    intent_name = request_data['queryResult']['intent']['displayName']

    if intent_name == 'Reason_comments':
        Asset_name = request_data['queryResult']['parameters']['Asset_name']
        Asset_info = dataset[dataset['Reason_Comments'] == Asset_name]

        if not Asset_info.empty:
            response_text = f"{Asset_name}: {Asset_info['Reason_Comments'].values[0]}"
        else:
            response_text = f"Sorry no information about {Asset_name}."

    elif intent_name == 'Reason_ActionTaken':
        Asset_name = request_data['queryResult']['parameters']['Asset_name']
        Asset_info = dataset[dataset['Reason_ActionTaken'] == Asset_name]

        if not Asset_info.empty:
            response_text = f"{Asset_name}: {Asset_info['Reason_ActionTaken'].values[0]}"
        else:
            response_text = f"Sorry no information about {Asset_name}"

    else:
        response_text = "Not sure how to respond to this query"
        
    response = {
        'fulfillmentText': response_text
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

