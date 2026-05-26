from __future__ import annotations

import imaplib
import email
from email.header import decode_header
from email.utils import parseaddr
from typing import Optional

from config import EMAIL_ADDRESS, EMAIL_PASSWORD, IMAP_SERVER, IMAP_PORT


def decode_mime_words(text: Optional[str]) -> str:
    if not text:
        return ""

    decoded_parts = decode_header(text)
    result = ""

    for part, encoding in decoded_parts:
        if isinstance(part, bytes):
            result += part.decode(encoding or "utf-8", errors="ignore")
        else:
            result += part

    return result


def extract_body(msg: email.message.Message) -> str:
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            disposition = str(part.get("Content-Disposition", ""))

            if content_type == "text/plain" and "attachment" not in disposition:
                payload = part.get_payload(decode=True)
                if payload:
                    return payload.decode(errors="ignore").strip()

        return ""

    payload = msg.get_payload(decode=True)

    if payload:
        return payload.decode(errors="ignore").strip()

    return ""


def has_attachment(msg: email.message.Message) -> bool:
    for part in msg.walk():
        disposition = str(part.get("Content-Disposition", "")).lower()

        if "attachment" in disposition:
            return True

    return False


def extract_sender_email(sender: str) -> str:
    _, addr = parseaddr(sender)
    return addr.lower().strip()


def fetch_unread_emails(limit: int = 5) -> list:
    emails = []

    with imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT) as mail:
        mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        mail.select("inbox")

        status, messages = mail.search(None, "UNSEEN")

        if status != "OK":
            return []

        email_ids = messages[0].split()
        selected_ids = email_ids[-limit:]

        for email_id in selected_ids:
            status, data = mail.fetch(email_id, "(RFC822)")

            if status != "OK" or not data or data[0] is None:
                continue

            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)

            sender = decode_mime_words(msg.get("From"))
            subject = decode_mime_words(msg.get("Subject"))
            body = extract_body(msg)
            sender_email = extract_sender_email(sender)

            emails.append({
                "imap_id": email_id.decode(),
                "message_id": msg.get("Message-ID", "").strip(),
                "from_raw": sender,
                "from_email": sender_email,
                "subject": subject,
                "body": body,
                "has_attachment": has_attachment(msg),
            })

    return emails


def mark_email_as_read(imap_id: str) -> None:
    with imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT) as mail:
        mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        mail.select("inbox")
        mail.store(imap_id, "+FLAGS", "\\Seen")