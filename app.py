import os
from flask import Flask, request, jsonify
from cloudant.client import Cloudant
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load credentials from environment variables
CLOUDANT_URL = os.getenv("CLOUDANT_URL")
CLOUDANT_API_KEY = os.getenv("CLOUDANT_API_KEY")
CLOUDANT_DB_NAME = os.getenv("CLOUDANT_DB_NAME")

client = Cloudant.iam(None, CLOUDANT_API_KEY, url=CLOUDANT_URL, connect=True)
database = client.create_database(CLOUDANT_DB_NAME, throw_on_exists=False)

@app.route('/')
def home():
    return "Hello from Flask backend!"

@app.route('/tickets', methods=['POST'])
def create_ticket():
    data = request.json
    doc = database.create_document(data)
    if doc.exists():
        return jsonify({"message": "Ticket created", "id": doc['_id']}), 201
    else:
        return jsonify({"error": "Failed to create ticket"}), 500

@app.route('/tickets', methods=['GET'])
def list_tickets():
    tickets = []
    for doc in database:
        if '_id' in doc and '_rev' in doc:
            tickets.append(doc)
    return jsonify(tickets)

if __name__ == '__main__':
    app.run(debug=True)
