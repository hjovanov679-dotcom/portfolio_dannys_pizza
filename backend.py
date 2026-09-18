import os
from html import escape

import resend
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__, static_folder=".", static_url_path="")

@app.after_request
def allowed_configured_frontend(response):
    allowed_origin = os.getenv("ALLOWED_ORIGIN")
    if allowed_origin and request.headers.get("Origin") == allowed_origin:
        response.headers["Access-Control-Allow-Origin"] = allowed_origin
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    return response

@app.get("/")
def home():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/api/send-confirmation", methods=["POST", "OPTIONS"])
def send_confirmation():
    if request.method == "OPTIONS":
        return "", 204

    data=request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()
    email = str(data.get("email", "")).strip()
    guests = str(data.get("guests", "")).strip()
    date = str(data.get("date", "")).strip()
    notes = str(data.get("notes", "")).strip()

    safe_name = escape(name)
    safe_email = escape(email)
    safe_guests = escape(guests)
    safe_date = escape(date)
    safe_notes = escape(notes)

    if not email or "@" not in email:
        return jsonify({"message": "Vul een geldig e-mailadres in!"}), 400
    resend.api_key = os.getenv("RESEND_API_KEY")

    sender = os.getenv("EMAIL_FROM", "Danny's Pizzas <onboarding@resend.dev>")
    recipient_name = escape(name or "there")

    customer_mail = {
        "from": sender,
        "to": [os.environ["DEMO_EMAIL_TO"]],
        "subject": "bevesteging reservering",
        "text": (
            f"Thank you for your reservation at Danny's Pizzas {safe_name} with {safe_guests} amount of guests on {safe_date}. We look forward serving you!"
        )
    }

    try: resend.Emails.send(customer_mail)
    except Exception as error:
        print(error)
        return jsonify({
            "message": "de email konden niet worden verstuurd"
        }), 500
    return jsonify({
        "message": "Reservering ontvangen!"
    }), 200

