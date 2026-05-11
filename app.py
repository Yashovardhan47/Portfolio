# # from flask import Flask, request, jsonify, render_template
# # from flask_cors import CORS
# # import smtplib
# # from email.mime.text import MIMEText
# # from email.mime.multipart import MIMEMultipart
# # import os

# # app = Flask(__name__, template_folder=".")
# # CORS(app)

# # # ─── CONFIG ───────────────────────────────────────────────────────────────────
# # # Set these as environment variables or replace with your credentials
# # SMTP_HOST     = os.getenv("SMTP_HOST", "smtp.gmail.com")
# # SMTP_PORT     = int(os.getenv("SMTP_PORT", 587))
# # SMTP_USER     = os.getenv("SMTP_USER", "kummarayashovardhan@gmail.com")       # sender email
# # SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "Yashu2106@kyv")      # Gmail App Password
# # RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL", "kummarayashovardhan@gmail.com")
# # # ──────────────────────────────────────────────────────────────────────────────


# # @app.route("/")
# # def index():
# #     return render_template("new.html")


# # @app.route("/send-email", methods=["POST"])
# # def send_email():
# #     data = request.get_json()

# #     name    = data.get("name", "").strip()
# #     email   = data.get("email", "").strip()
# #     message = data.get("message", "").strip()

# #     if not name or not email or not message:
# #         return jsonify({"success": False, "error": "All fields are required."}), 400

# #     try:
# #         msg = MIMEMultipart("alternative")
# #         msg["Subject"] = f"Portfolio Contact – {name}"
# #         msg["From"]    = SMTP_USER
# #         msg["To"]      = RECEIVER_EMAIL
# #         msg["Reply-To"] = email

# #         html_body = f"""
# #         <html><body style="font-family:Arial,sans-serif;padding:20px;background:#f4f4f4;">
# #           <div style="max-width:600px;margin:auto;background:#fff;border-radius:10px;
# #                       padding:30px;box-shadow:0 4px 12px rgba(0,0,0,.1);">
# #             <h2 style="color:#4a4af4;margin-bottom:4px;">New Portfolio Message</h2>
# #             <hr style="border:none;border-top:2px solid #4a4af4;margin-bottom:20px;">
# #             <p><strong>Name:</strong> {name}</p>
# #             <p><strong>Email:</strong> <a href="mailto:{email}">{email}</a></p>
# #             <p><strong>Message:</strong></p>
# #             <blockquote style="border-left:4px solid #4a4af4;padding-left:15px;color:#555;">
# #               {message.replace(chr(10), '<br>')}
# #             </blockquote>
# #           </div>
# #         </body></html>
# #         """

# #         msg.attach(MIMEText(html_body, "html"))

# #         with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
# #             server.ehlo()
# #             server.starttls()
# #             server.login(SMTP_USER, SMTP_PASSWORD)
# #             server.sendmail(SMTP_USER, RECEIVER_EMAIL, msg.as_string())

# #         return jsonify({"success": True, "message": "Email sent successfully!"})

# #     except Exception as e:
# #         print(f"[ERROR] {e}")
# #         return jsonify({"success": False, "error": "Failed to send email. Please try again later."}), 500


# # if __name__ == "__main__":
# #     app.run(debug=True, port=5000)











# # from flask import Flask, request, jsonify, render_template
# # from flask_cors import CORS
# # import smtplib
# # from email.mime.text import MIMEText
# # from email.mime.multipart import MIMEMultipart

# # app = Flask(__name__)
# # CORS(app)

# # # 🔐 CONFIG (IMPORTANT)
# # SMTP_HOST = "smtp.gmail.com"
# # SMTP_PORT = 587
# # SMTP_USER = "kummarayashovardhan@gmail.com"          # 👉 replace
# # SMTP_PASSWORD = "zuzyfsrdpirsivdo"         # 👉 Gmail App Password only
# # RECEIVER_EMAIL = "kummarayashovardhan@gmail.com"


# # # ✅ Home route
# # @app.route("/")
# # def index():
# #     return render_template("new.html")   # must be inside templates/


# # # ✅ Email API
# # @app.route("/send-email", methods=["POST"])
# # def send_email():
# #     data = request.get_json()

# #     name = data.get("name", "").strip()
# #     email = data.get("email", "").strip()
# #     message = data.get("message", "").strip()

# #     print("\n📩 New Request Received")
# #     print("Name:", name)
# #     print("Email:", email)
# #     print("Message:", message)

# #     if not name or not email or not message:
# #         return jsonify({"success": False, "error": "All fields required"}), 400

# #     try:
# #         msg = MIMEMultipart("alternative")
# #         msg["Subject"] = f"Portfolio Contact – {name}"
# #         msg["From"] = SMTP_USER
# #         msg["To"] = RECEIVER_EMAIL
# #         msg["Reply-To"] = email

# #         html_body = f"""
# #         <html>
# #         <body style="font-family:Arial;padding:20px;background:#f4f4f4;">
# #             <div style="max-width:600px;margin:auto;background:#fff;padding:20px;border-radius:10px;">
# #                 <h2 style="color:#4a4af4;">New Message</h2>
# #                 <p><b>Name:</b> {name}</p>
# #                 <p><b>Email:</b> {email}</p>
# #                 <p><b>Message:</b></p>
# #                 <p>{message}</p>
# #             </div>
# #         </body>
# #         </html>
# #         """

# #         msg.attach(MIMEText(html_body, "html"))

# #         print("🔌 Connecting to SMTP...")
# #         with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
# #             server.starttls()
# #             print("🔑 Logging in...")
# #             server.login(SMTP_USER, SMTP_PASSWORD)

# #             print("📤 Sending email...")
# #             server.sendmail(SMTP_USER, RECEIVER_EMAIL, msg.as_string())

# #         print("✅ Email sent successfully!")

# #         return jsonify({"success": True})

# #     except Exception as e:
# #         print("❌ ERROR:", e)
# #         return jsonify({"success": False, "error": str(e)}), 500


# # # 🚀 Run server
# # if __name__ == "__main__":
# #     app.run(debug=True, port=5000)







# """
# Portfolio Contact – Flask backend
# ══════════════════════════════════
# Setup (one-time):
#   pip install flask flask-cors

# Run:
#   python app.py           ← dev mode (localhost:5000)
#   gunicorn -w 2 app:app   ← production
# """

# from flask import Flask, request, jsonify, render_template
# from flask_cors import CORS
# import smtplib, re, os, logging
# from email.mime.text      import MIMEText
# from email.mime.multipart import MIMEMultipart
# from datetime             import datetime

# app = Flask(__name__, template_folder=".")
# CORS(app, resources={r"/send-email": {"origins": "*"}})

# logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)s  %(message)s")
# log = logging.getLogger(__name__)

# SMTP_HOST      = os.getenv("SMTP_HOST",      "smtp.gmail.com")
# SMTP_PORT      = int(os.getenv("SMTP_PORT",  "587"))
# SMTP_USER      = os.getenv("SMTP_USER",      "kyashovardhank47@gmail.com")
# SMTP_PASSWORD  = os.getenv("SMTP_PASSWORD",  "mvfudrktjowphhgq")
# RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL", "kyashovardhank47@gmail.com")

# _EMAIL_RE = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')

# def valid_email(addr):
#     return bool(_EMAIL_RE.match(addr))

# def build_html(name, email, message):
#     safe = (message.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace("\n","<br>"))
#     ts = datetime.now().strftime("%d %b %Y, %I:%M %p")
#     return f"""<html><body style="margin:0;padding:0;background:#f4f4f4;font-family:Arial,sans-serif;">
#   <div style="max-width:600px;margin:30px auto;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 6px 24px rgba(0,0,0,.1);">
#     <div style="background:linear-gradient(135deg,#5c3bfe,#7c3aed);padding:30px 36px;">
#       <h1 style="margin:0;color:#fff;font-size:21px;font-weight:700;">📬 New Portfolio Message</h1>
#       <p style="margin:6px 0 0;color:rgba(255,255,255,.65);font-size:13px;">{ts}</p>
#     </div>
#     <div style="padding:32px 36px;">
#       <table style="width:100%;border-collapse:collapse;margin-bottom:28px;background:#f8f7ff;border-radius:10px;overflow:hidden;">
#         <tr><td style="padding:12px 16px;font-size:12px;color:#6b7280;font-weight:700;text-transform:uppercase;width:80px;">Name</td>
#             <td style="padding:12px 16px;font-size:15px;color:#0d0d1a;font-weight:600;">{name}</td></tr>
#         <tr style="border-top:1px solid #ede9fe;">
#             <td style="padding:12px 16px;font-size:12px;color:#6b7280;font-weight:700;text-transform:uppercase;">From</td>
#             <td style="padding:12px 16px;"><a href="mailto:{email}" style="color:#5c3bfe;font-size:15px;">{email}</a></td></tr>
#       </table>
#       <p style="font-size:12px;color:#6b7280;font-weight:700;text-transform:uppercase;margin-bottom:10px;">Message</p>
#       <div style="background:#f8f7ff;border-left:4px solid #5c3bfe;border-radius:0 10px 10px 0;padding:18px 22px;font-size:15px;color:#374151;line-height:1.8;">{safe}</div>
#       <div style="margin-top:28px;padding:16px;background:rgba(0,217,163,.07);border-radius:10px;font-size:13px;color:#059669;font-weight:600;">💡 Reply directly to respond to {name}.</div>
#     </div>
#     <div style="background:#f4f4f4;padding:14px 36px;text-align:center;font-size:12px;color:#9ca3af;border-top:1px solid #ede9fe;">K. Yashovardhan · Portfolio Contact Form</div>
#   </div>
# </body></html>"""

# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route("/send-email", methods=["POST"])
# def send_email():
#     data = request.get_json(silent=True)
#     if not data:
#         return jsonify({"success": False, "error": "Invalid request body."}), 400

#     name    = (data.get("name",    "") or "").strip()
#     email   = (data.get("email",   "") or "").strip()
#     message = (data.get("message", "") or "").strip()

#     errors = []
#     if not name:               errors.append("Name is required.")
#     elif len(name) > 120:      errors.append("Name is too long.")
#     if not email:              errors.append("Email is required.")
#     elif not valid_email(email): errors.append("Invalid email address.")
#     if not message:            errors.append("Message is required.")
#     elif len(message) > 5000:  errors.append("Message too long.")
#     if errors:
#         return jsonify({"success": False, "error": " ".join(errors)}), 400

#     try:
#         msg = MIMEMultipart("alternative")
#         msg["Subject"]  = f"Portfolio Contact - {name}"
#         msg["From"]     = f"Portfolio <{SMTP_USER}>"
#         msg["To"]       = RECEIVER_EMAIL
#         msg["Reply-To"] = email
#         msg.attach(MIMEText(build_html(name, email, message), "html", "utf-8"))

#         log.info("Connecting to %s:%d ...", SMTP_HOST, SMTP_PORT)
#         with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as server:
#             server.ehlo()
#             server.starttls()
#             server.ehlo()
#             server.login(SMTP_USER, SMTP_PASSWORD)
#             server.sendmail(SMTP_USER, RECEIVER_EMAIL, msg.as_string())

#         log.info("Email sent from %s", email)
#         return jsonify({"success": True, "message": "Email sent successfully!"})

#     except smtplib.SMTPAuthenticationError:
#         log.error("SMTP auth failed")
#         return jsonify({"success": False, "error": "Server authentication error."}), 500
#     except smtplib.SMTPException as exc:
#         log.error("SMTP error: %s", exc)
#         return jsonify({"success": False, "error": "Delivery failed. Please try again."}), 500
#     except Exception as exc:
#         log.exception("Unexpected error: %s", exc)
#         return jsonify({"success": False, "error": "Unexpected error. Please try again."}), 500

# @app.route("/health")
# def health():
#     return jsonify({"status": "ok", "receiver": RECEIVER_EMAIL})

# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0", port=5000)













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

# YOUR GMAIL
SMTP_USER = "kyashovardhank47@gmail.com"

# IMPORTANT:
# Use GOOGLE APP PASSWORD (16 digits)
# NOT your normal Gmail password
SMTP_PASSWORD = "wxaukxihltmqxdfr"

# Receiver mail
RECEIVER_EMAIL = "kyashovardhank47@gmail.com"

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

        server.starttls()

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