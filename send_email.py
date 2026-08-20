import smtplib
import os
from dotenv import load_dotenv, dotenv_values
from email.mime.text import MIMEText

def send_email(subject, body, to_email):
    load_dotenv()

    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")

    connection = smtplib.SMTP("smtp.gmail.com", 587)
    connection.starttls()
    connection.login(sender_email, sender_password)

    message = MIMEText(body, "html")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = to_email

    connection.sendmail(
        sender_email,
        to_email,
        message.as_string()
    )

    connection.close()