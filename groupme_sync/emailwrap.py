import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(title: str, body: str,
    smtp_server: str, smtp_username: str, smtp_password: str,
    from_addr: str, to_addr: str):
    """
    Send an email to an SMTP server with starttls, and some other
    stuff. If you need to do anything different, just write your
    own implementation.
    """
    ctx = ssl.create_default_context()

    with smtplib.SMTP(smtp_server, port=587) as server:
        server.starttls(context=ctx)
        server.ehlo()
        server.login(smtp_username, smtp_password)

        message = MIMEMultipart("alternative")
        message["Subject"] = title
        message["From"] = from_addr
        message["To"] = to_addr
        part = MIMEText(body, "plain")
        message.attach(part)

        server.sendmail(
            from_addr, to_addr, message.as_string()
        )