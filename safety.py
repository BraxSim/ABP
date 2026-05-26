from __future__ import annotations

from config import AUTO_SEND_ONLY_KNOWN_USERS, EXTRA_SAFETY_KEYWORDS

DEFAULT_RISKY_KEYWORDS = [
    "bank",
    "payment failed",
    "invoice",
    "refund",
    "legal",
    "lawyer",
    "complaint",
    "angry",
    "urgent",
    "password",
    "verification code",
    "2fa",
    "security alert",
]

RISKY_KEYWORDS = DEFAULT_RISKY_KEYWORDS + EXTRA_SAFETY_KEYWORDS


def is_risky_email(
    subject: str,
    body: str,
    has_attachment: bool
) -> tuple[bool, str]:
    if has_attachment:
        return True, "Email has attachment."

    text = f"{subject}\n{body}".lower()

    for keyword in RISKY_KEYWORDS:
        if keyword in text:
            return True, f"Risky keyword detected: {keyword}"

    return False, ""


def should_auto_send(
    email_item: dict,
    user_info: dict | None
) -> tuple[bool, str]:
    if AUTO_SEND_ONLY_KNOWN_USERS and not user_info:
        return False, "Sender is not found in Google Sheet."

    risky, reason = is_risky_email(
        subject=email_item.get("subject", ""),
        body=email_item.get("body", ""),
        has_attachment=email_item.get("has_attachment", False),
    )

    if risky:
        return False, reason

    return True, "Allowed."