from __future__ import annotations

from datetime import datetime

ALLOWED_TEMPLATE_IDS = {
    "reference_learning",
    "paid_user_support",
    "not_paid_or_expired",
    "customer_profile_link",
}


ACADEMIC_KEYWORDS = [
    "assignment",
    "homework",
    "code",
    "reference",
    "copy",
    "reuse",
    "solution",
    "answers",
    "coursework",
]


def assert_template_allowed(template_id: str) -> None:
    if template_id not in ALLOWED_TEMPLATE_IDS:
        raise ValueError(f"Blocked: template_id '{template_id}' is not allowed.")


def is_paid_active(user_info: dict | None) -> bool:
    if not user_info:
        return False

    paid_status = str(user_info.get("paid_status", "")).lower().strip()
    expiry_date = str(user_info.get("expiry_date", "")).strip()

    if paid_status not in {"true", "yes", "paid", "active"}:
        return False

    if not expiry_date:
        return True

    try:
        expiry = datetime.strptime(expiry_date, "%Y-%m-%d").date()
        return expiry >= datetime.today().date()
    except ValueError:
        return False


def choose_template_id(subject: str, body: str, user_info: dict | None) -> str:
    text = f"{subject}\n{body}".lower()

    if any(keyword in text for keyword in ACADEMIC_KEYWORDS):
        return "reference_learning"

    if is_paid_active(user_info):
        return "paid_user_support"

    return "not_paid_or_expired"