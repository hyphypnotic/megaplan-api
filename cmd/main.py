from flask import Flask, request
import requests
import logging
from dotenv import load_dotenv
import os

load_dotenv('cmd/config.env')
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.getenv('MP_ACCESS_TOKEN')}"
}
MEGAPLAN_URL = os.getenv('MEGAPLAN_URL')

def create_client_data(data):
    return {
        'contentType': 'ContractorCompany',
        'name': data['from'],
        "contactInfo":[{"contentType":"ContactInfo","type":"phone","value":data['from']}],
    }

def create_comment(client_data, data):
    return {
        "contentType":"Comment",
        "content":data["text"],
        "subject":client_data,
        "transportMessages": [
            {"contentType":"WhatsappMessage",
            'from':data['from'],
            'to':data['to'],
            'text':data['text'],}
        ]
    }

def check_client_existence(client_name):
    url = f"{MEGAPLAN_URL}/contractorCompany"
    params = {"name":client_name}
    response = requests.get(url, json=params, headers=HEADERS)
    data = dict(response.json())
    if data.get("data"):
        logging.info("Full response from API(getting clients): %s", data)
        for client in data['data']:
            if client['name'] == client_name:
                logging.info("Client '%s' found. ID: %s", client_name, client['id'])
                return True, client['id']
    logging.info("Client '%s' not found.", client_name)
    return False, None

@app.route('/webhook', methods = ["POST"])
def whatsapp_to_megaplan():
    try:
        data = dict(request.json)
        client_data = create_client_data(data)
        comment = create_comment(client_data, data)
        logging.info("Received message from %s: %s", client_data['name'], data["text"])
        client_exists, client_id = check_client_existence(client_data["name"])
        if client_exists:
            requests.post(f"{MEGAPLAN_URL}/contractorCompany/{client_id}/comments", json=comment, headers=HEADERS)
        else:
            response = requests.post(f"{MEGAPLAN_URL}/contractorCompany", json=client_data, headers=HEADERS)
            clientCompany = dict(response.json())
            logging.info(clientCompany)
            requests.post(f"{MEGAPLAN_URL}/contractorCompany/{clientCompany['data']['id']}/comments", json=comment, headers=HEADERS)
        return {}
    except Exception as e:
        logging.error("An error occurred: %s", str(e))
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run(port=8080)