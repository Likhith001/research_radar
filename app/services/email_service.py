import smtplib
from email.mime.text import MIMEText
import os

def send_email(content):

    sender = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")

    if not sender or not password:
        print("Email credentials missing")
        return

    msg = MIMEText(content)
    msg["Subject"] = "ResearchRadar Daily Digest"
    msg["From"] = sender
    msg["To"] = sender

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)

        server.sendmail(sender, sender, msg.as_string())
        server.quit()

        print("Email sent successfully!")

    except Exception as e:
        print("Email error:", e)