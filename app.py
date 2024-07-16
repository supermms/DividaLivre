import os
import logging
from whatsapp import WhatsApp, Message
from dotenv import load_dotenv
from flask import Flask, render_template

app = Flask(__name__)

# Load .env file
load_dotenv("./.env")

# Access token for your WhatsApp business account app
whatsapp_token = os.getenv("WHATSAPP_TOKEN")

# Verify Token defined when configuring the webhook
VERIFY_TOKEN = "batmanbatman"

messenger = WhatsApp(os.getenv("TOKEN"),
                     phone_number_id=os.getenv("PHONE_NUMBER_ID"))


# Required webhook verifictaion for WhatsApp
# info on verification request payload:
# https://developers.facebook.com/docs/graph-api/webhooks/getting-started#verification-requests
def verify(request):
    # Parse params from the webhook verification request
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    # Check if a token and mode were sent
    if mode and token:
        # Check the mode and token sent are correct
        if mode == "subscribe" and token == VERIFY_TOKEN:
            # Respond with 200 OK and challenge token from the request
            print("WEBHOOK_VERIFIED")
            return challenge, 200
        else:
            # Responds with '403 Forbidden' if verify tokens do not match
            print("VERIFICATION_FAILED")
            return jsonify({"status": "error", "message": "Verification failed"}), 403
    else:
        # Responds with '400 Bad Request' if verify tokens do not match
        print("MISSING_PARAMETER")
        return jsonify({"status": "error", "message": "Missing parameters"}), 400



@app.route('/')
def hello_world():
    return render_template('index.html')

# Accepts POST and GET requests at /webhook endpoint
@app.route("/webhook", methods=["POST", "GET"])
def webhook():
    if request.method == "GET":
        return verify(request)
    elif request.method == "POST":
        return handle_message(request)


@app.route('/peido', methods=['GET'])
    logging.info('peido')

if __name__ == "__main__":
 app.run()