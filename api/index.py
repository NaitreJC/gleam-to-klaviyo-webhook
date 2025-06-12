from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Your Klaviyo API Key and List ID
KLAVIYO_API_KEY = "pk_16a7765a5f4349e917377a37f9fdc115cf"
KLAVIYO_LIST_ID = "TzK4Ps"

@app.route("/", methods=["GET"])
def index():
    return "Klaviyo Webhook Listener is running."

@app.route("/gleam-webhook", methods=["POST"])
def gleam_webhook():
    data = request.json
    email = data.get("email")
    name = data.get("name", "")

    if not email:
        return jsonify({"error": "Email missing from payload"}), 400

    payload = {
        "profiles": [
            {
                "email": email,
                "first_name": name
            }
        ]
    }

    headers = {
        "Authorization": f"Klaviyo-API-Key {KLAVIYO_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        f"https://a.klaviyo.com/api/lists/{KLAVIYO_LIST_ID}/profiles/",
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"error": response.text}), response.status_code
