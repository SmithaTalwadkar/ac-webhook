from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


AC_API_URL = "https://chop.api-us1.com"
AC_API_KEY = "0469ca239ca1c379f57ddfaf5079c5abeb4acebc2b12d3562525ff6c2c9486d4ba29a5ac"


def resubscribe_contact(email):
    headers = {
        "Api-Token": AC_API_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "contact": {
            "email": email,
            "status": 1 
        }
    }

    response = requests.post(AC_API_URL, json=data, headers=headers)
    return response.status_code, response.text


@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        contacts = data.get("contacts", [])

        for contact in contacts:
            email = contact.get("email")
            if email:
                status, response_text = resubscribe_contact(email)
                print(f"Re-subscribed: {email} - Status: {status}")

        return jsonify({"message": "Contacts processed"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)