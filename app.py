from flask import Flask, request, jsonify, render_template
from compliance import check_gdpr_compliance
from email_service import send_drip_email
from content import generate_content
from social import schedule_post
import os
from dotenv import load_dotenv
import logging
import sqlite3

load_dotenv()
app = Flask(__name__)
logging.basicConfig(level=logging.INFO, filename='app.log', format='%(asctime)s %(levelname)s:%(message)s')

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/check", methods=["POST"])
def check():
    try:
        data = request.get_json()
        url = data.get("url")
        email = data.get("email")
        if not url or not email:
            return jsonify({"error": "Missing url or email"}), 400
        report = check_gdpr_compliance(url)
        if "error" not in report:
            send_drip_email(email, "GDPR Compliance Report", f"Results: {report}")
        return jsonify(report)
    except Exception as e:
        logging.error(f"Check endpoint error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/subscribe", methods=["POST"])
def subscribe():
    try:
        data = request.get_json()
        email = data.get("email")
        conn = sqlite3.connect("content.db")
        conn.execute("INSERT INTO subscribers (email) VALUES (?)", (email,))
        conn.commit()
        conn.close()
        send_drip_email(email, "Welcome to GDPR Compliance!", "Thanks for subscribing! Pay via PayPal: paypal.me/youraccount")
        content = generate_content("GDPR compliance tips")
        schedule_post(content)
        return jsonify({"status": "success"})
    except Exception as e:
        logging.error(f"Subscribe error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
