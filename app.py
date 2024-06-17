from flask import Flask, request, jsonify, render_template
import dialogflow_v2 as dialogflow
import os
from google.oauth2 import service_account

app = Flask(__name__)

# Set up the path to your service account key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service-account-file.json"

# Initialize Dialogflow client
credentials = service_account.Credentials.from_service_account_file("service-account-file.json")
client = dialogflow.SessionsClient(credentials=credentials)

# Dialogflow detect intent function
def detect_intent_texts(project_id, session_id, texts, language_code):
    session = client.session_path(project_id, session_id)
    for text in texts:
        text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = client.detect_intent(session=session, query_input=query_input)
        return response.query_result.fulfillment_text

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    session_id = req.get('session')
    text = req.get('queryResult').get('queryText')
    response_text = detect_intent_texts('even-metrics-422217-p3', session_id, [text], 'en')
    return jsonify({'fulfillmentText': response_text})

if __name__ == '__main__':
    app.run(debug=True)
