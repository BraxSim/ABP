import smtplib
from email.message import EmailMessage
from typing import Optional

from config import EMAIL_ADDRESS, EMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT


def send_email(
    to_email: str,
    subject: str,
    body: str,
    html_body: Optional[str] = None
) -> None:
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        raise ValueError("EMAIL_ADDRESS or EMAIL_PASSWORD is missing")

    msg = EmailMessage()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.set_content(body)

    if html_body:
        msg.add_alternative(html_body, subtype="html")

    with smtplib.SMTP_SSL(SMTP_SERVER, int(SMTP_PORT), timeout=30) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)