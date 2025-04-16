import smtplib
from email.mime.text import MIMEText
import logging
import os
from dotenv import load_dotenv

load_dotenv()
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
logging.basicConfig(level=logging.INFO, filename='app.log')

def send_drip_email(to_email, subject, content):
    try:
        msg = MIMEText(content)
        msg["Subject"] = subject
        msg["From"] = f"compliance@{SMTP_HOST}"
        msg["To"] = to_email
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(msg["From"], [to_email], msg.as_string())
        logging.info(f"Email sent to {to_email}")
        return True
    except Exception as e:
        logging.error(f"Email failed for {to_email}: {str(e)}")
        return False
