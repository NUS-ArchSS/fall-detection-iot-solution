import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access environment variables
sender_email = os.getenv("SENDER_EMAIL")
sender_password = os.getenv("SENDER_PASSWORD")
receiver_email = os.getenv("RECEIVER_EMAIL")
sender_email = os.getenv("SENDER_EMAIL")
smtp_server = os.getenv("SMTP_SERVER")
smtp_port = os.getenv("SMTP_PORT")


def send_email(sender_email, sender_password, receiver_email, subject, message):
    smtp_username = sender_email

    # Create a multipart message object
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    # Attach the message to the email
    msg.attach(MIMEText(message, "plain"))

    try:
        # Create a secure connection to the SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            # Log in to the SMTP server
            server.login(smtp_username, sender_password)
            # Send the email
            server.send_message(msg)
        print("Email sent successfully!")
    except smtplib.SMTPException as e:
        print("Error sending email:", str(e))


subject = "Hello from Python!"
message = "This is a test email sent from a Python app."

send_email(sender_email, sender_password, receiver_email, subject, message)
