from __future__ import annotations

import json
import os
from datetime import datetime

from config import SENT_LOG_PATH, DAILY_SEND_LIMIT


def load_log() -> list[dict]:
    if not os.path.exists(SENT_LOG_PATH):
        return []

    with open(SENT_LOG_PATH, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_log(log: list[dict]) -> None:
    with open(SENT_LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2, ensure_ascii=False)


def already_replied(message_id: str, from_email: str, subject: str) -> bool:
    log = load_log()

    for item in log:
        if message_id and item.get("message_id") == message_id:
            return True

        if (
            item.get("from_email") == from_email
            and item.get("subject") == subject
        ):
            return True

    return False


def count_today_sent() -> int:
    today = datetime.now().strftime("%Y-%m-%d")
    log = load_log()

    return sum(
        1
        for item in log
        if item.get("sent_at", "").startswith(today)
    )


def daily_limit_reached() -> bool:
    return count_today_sent() >= DAILY_SEND_LIMIT


def record_sent(
    message_id: str,
    from_email: str,
    subject: str,
    template_id: str,
    dry_run: bool,
) -> None:
    log = load_log()

    log.append({
        "sent_at": datetime.now().isoformat(timespec="seconds"),
        "message_id": message_id,
        "from_email": from_email,
        "subject": subject,
        "template_id": template_id,
        "dry_run": dry_run,
    })

    save_log(log)