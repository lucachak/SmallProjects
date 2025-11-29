
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

class EmailHandler:
    def __init__(self,
                 SMTP_SERVER="smtp.gmail.com",
                 SMTP_PORT=587,
                 EMAIL_SENDER="your_email@gmail.com",
                 EMAIL_PASSWORD="your_app_password",
                 EMAIL_SUBJECT="⚠️ License Expiration Reminder"):

        self.SMTP_SERVER = SMTP_SERVER
        self.SMTP_PORT = SMTP_PORT
        self.EMAIL_SENDER = EMAIL_SENDER
        self.EMAIL_PASSWORD = EMAIL_PASSWORD
        self.EMAIL_SUBJECT = EMAIL_SUBJECT

    def send_email(self, to_email, name, exp_date):
        msg = MIMEMultipart()
        msg["From"] = self.EMAIL_SENDER
        msg["To"] = to_email
        msg["Subject"] = self.EMAIL_SUBJECT

        body = f"""
Hello {name or "User"},

This is an automated message: your license will expire on {exp_date.strftime('%d/%m/%Y')}.
Please renew your contract.

Regards,
Lil Bot
"""
        msg.attach(MIMEText(body, "plain"))
        try:
            with smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT) as server:
                server.starttls()
                server.login(self.EMAIL_SENDER, self.EMAIL_PASSWORD)
                server.send_message(msg)
            print(f"✅ Email sent to {to_email}")
        except Exception as e:
            print(f"❌ Failed to send email to {to_email}: {e}")
            print(f"Error happened to {to_email} error {e}")
