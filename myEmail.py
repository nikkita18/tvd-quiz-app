import os
from flask_mail import Mail, Message
from dotenv import load_dotenv

load_dotenv()

class Email:
    def __init__(self, app):
        # Mail configuration from environment variables
        app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
        app.config["MAIL_PORT"] = int(os.environ.get("MAIL_PORT", 587))
        app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME", "")
        app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD", "")
        app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS", "true").lower() in ("true", "1", "yes")
        app.config["MAIL_USE_SSL"] = os.environ.get("MAIL_USE_SSL", "false").lower() in ("true", "1", "yes")
        self.sender = os.environ.get("MAIL_USERNAME", "no-reply@tvdquiz.com")
        self.mail = Mail(app)

    def compose_mail(self, subject, email, message):
        sender = self.sender or 'no-reply@tvdquiz.com'
        msg = Message(subject, sender=sender, recipients=[email])
        msg.body = message
        self.mail.send(msg)