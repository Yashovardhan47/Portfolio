import os
import ssl

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# =====================================================
# EMAIL CONFIG
# =====================================================

# ENV VARIABLES FROM RENDER
SMTP_USER      = os.getenv("SMTP_USER")
SMTP_PASSWORD  = os.getenv("SMTP_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

# DEBUG
print("SMTP_USER:", SMTP_USER)
print("RECEIVER_EMAIL:", RECEIVER_EMAIL)

# =====================================================
# HOME ROUTE — serves index.html from root directory
# =====================================================

@app.route("/")
def home():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), "index.html")

# =====================================================
# SEND EMAIL ROUTE
# =====================================================

@app.route("/send-email", methods=["POST"])
def send_email():

    try:

        if not SMTP_USER or not SMTP_PASSWORD or not RECEIVER_EMAIL:
            return jsonify({"success": False, "error": "Environment variables missing"}), 500

        data = request.get_json()

        if not data:
            return jsonify({"success": False, "error": "No JSON data received"}), 400

        name    = data.get("name", "").strip()
        email   = data.get("email", "").strip()
        message = data.get("message", "").strip()

        if not name or not email or not message:
            return jsonify({"success": False, "error": "All fields are required"}), 400

        body = f"""
New Portfolio Message

Name:    {name}
Email:   {email}

Message:
{message}
"""

        msg = MIMEMultipart()
        msg["From"]    = SMTP_USER
        msg["To"]      = RECEIVER_EMAIL
        msg["Subject"] = f"Portfolio Contact from {name}"
        msg.attach(MIMEText(body, "plain"))

        # SSL on port 465 — reliable on all cloud hosts
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, RECEIVER_EMAIL, msg.as_string())

        print("EMAIL SENT SUCCESSFULLY")
        return jsonify({"success": True, "message": "Email sent successfully"})

    except Exception as e:
        print("FULL ERROR:", str(e))
        return jsonify({"success": False, "error": str(e)}), 500

# =====================================================
# RUN APP
# =====================================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)