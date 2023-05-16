import json
import smtplib
import os
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from deepdiff import DeepDiff

SMTP_USERNAME = os.environ["SMTP_USERNAME"]
SMTP_PASSWORD = os.environ["SMTP_PASSWORD"]
SENDER_EMAIL = os.environ["SENDER_EMAIL"]
RECIPIENT_EMAIL = os.environ["RECIPIENT_EMAIL"]

#Replace with your SMTP Server Credentials
SMTP_SERVER = "SMTPServer"
SMTP_PORT = 25
USE_TLS = False

def send_email(subject, body):
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECIPIENT_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
        if USE_TLS:
            smtp.starttls()
        smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
        smtp.sendmail(SMTP_USERNAME, RECIPIENT_EMAIL, msg.as_string())

def main():
    with open("previous_data.json", "r") as file:
        previous_data = json.load(file)

    response = requests.get(
        "https://www.gstatic.com/ipranges/goog.json"
    )
    current_data = response.json()

    diff = DeepDiff(previous_data, current_data, exclude_paths=["root['syncToken']", "root['creationTime']"])

    if diff:
        differences = json.dumps({"old": previous_data, "new": current_data}, indent=2)
        send_email("Google IP Changes Detected", differences)

        with open("previous_data.json", "w") as file:
            json.dump(current_data, file, indent=2)

if __name__ == "__main__":
    main()
