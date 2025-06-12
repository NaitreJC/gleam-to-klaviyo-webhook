from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

KLAVIYO_API_KEY = "pk_16a7765a5f4349e917377a37f9fdc115cf"  # your real key
KLAVIYO_LIST_ID = "TzK4Ps"  # your actual list ID

@app.route("/", methods=["POST"])
def subscribe_user():
    data = request.json
    email = data.get("email")
    first_name = data.get("first_name", "")
    last_name = data.get("last_name", "")

    if not email:
        return jsonify({"error": "Missing email"}), 400

    payload = {
        "profiles": [
            {
                "email": email,
                "first_name": first_name,
                "last_name": last_name
            }
        ]
    }

    headers = {
        "Authorization": f"Bearer {KLAVIYO_API_KEY}",
        "Content-Type": "application/json",
        "revision": "2023-10-15"
    }

    res = requests.post(
        f"https://a.klaviyo.com/api/lists/{KLAVIYO_LIST_ID}/relationships/profiles/",
        headers=headers,
        json=payload
    )

    if res.status_code in [200, 202]:
        return jsonify({"success": True})
    else:
        return jsonify({"error": res.json()}), res.status_code
