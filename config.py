from __future__ import annotations

import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


def get_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)

    if value is None:
        return default

    return value.strip().lower() in {"true", "1", "yes", "y"}


def get_list(name: str, default: Optional[list[str]] = None) -> list[str]:
    value = os.getenv(name)

    if not value:
        return default or []

    return [
        item.strip().lower()
        for item in value.split(",")
        if item.strip()
    ]


EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")

IMAP_SERVER = os.getenv("IMAP_SERVER", "imap.gmail.com")
IMAP_PORT = int(os.getenv("IMAP_PORT", "993"))

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))

GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID", "")
GOOGLE_SHEET_RANGE = os.getenv("GOOGLE_SHEET_RANGE", "Sheet1!A:F")
GOOGLE_CREDENTIALS_JSON = os.getenv("GOOGLE_CREDENTIALS_JSON", "credentials.json")

EMPLOYEE_APPROVAL_EMAIL = os.getenv("EMPLOYEE_APPROVAL_EMAIL", "")

DRY_RUN = get_bool("DRY_RUN", True)
AUTO_SEND_ONLY_KNOWN_USERS = get_bool("AUTO_SEND_ONLY_KNOWN_USERS", True)

MAX_EMAILS_PER_RUN = int(os.getenv("MAX_EMAILS_PER_RUN", "5"))
DAILY_SEND_LIMIT = int(os.getenv("DAILY_SEND_LIMIT", "20"))

MARK_AS_READ_AFTER_PROCESS = get_bool("MARK_AS_READ_AFTER_PROCESS", False)

EXTRA_SAFETY_KEYWORDS = get_list("SAFETY_KEYWORDS", [])

SENT_LOG_PATH = "sent_log.json"

PENDING_APPROVALS_PATH = os.getenv("PENDING_APPROVALS_PATH", "pending_approvals.json")
APPROVAL_KEYWORD = os.getenv("APPROVAL_KEYWORD", "APPROVE")
REJECTION_KEYWORD = os.getenv("REJECTION_KEYWORD", "REJECT")