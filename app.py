import os

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__, template_folder=".")
CORS(app)

# =====================================================
# EMAIL CONFIG
# =====================================================

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587

# GET FROM RENDER ENVIRONMENT VARIABLES
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

# =====================================================
# HOME ROUTE
# =====================================================

@app.route("/")
def home():
    return render_template("new.html")

# =====================================================
# SEND EMAIL ROUTE
# =====================================================

@app.route("/send-email", methods=["POST"])
def send_email():

    try:
        data = request.get_json()

        name = data.get("name")
        email = data.get("email")
        message = data.get("message")

        # ==========================
        # VALIDATION
        # ==========================

        if not name or not email or not message:
            return jsonify({
                "success": False,
                "error": "All fields are required"
            }), 400

        # ==========================
        # EMAIL BODY
        # ==========================

        body = f"""
New Portfolio Message

Name: {name}

Email: {email}

Message:
{message}
"""

        # ==========================
        # MIME MESSAGE
        # ==========================

        msg = MIMEMultipart()

        msg["From"] = SMTP_USER
        msg["To"] = RECEIVER_EMAIL
        msg["Subject"] = f"Portfolio Contact from {name}"

        msg.attach(MIMEText(body, "plain"))

        # ==========================
        # SMTP SERVER
        # ==========================

        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)

        server.ehlo()

        server.starttls()

        server.ehlo()

        server.login(
            SMTP_USER,
            SMTP_PASSWORD
        )

        server.sendmail(
            SMTP_USER,
            RECEIVER_EMAIL,
            msg.as_string()
        )

        server.quit()

        return jsonify({
            "success": True,
            "message": "Email sent successfully"
        })

    except Exception as e:

        print("ERROR:", e)

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# =====================================================
# RUN APP
# =====================================================

if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )