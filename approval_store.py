from __future__ import annotations

import json
import os
import secrets
from datetime import datetime

from config import PENDING_APPROVALS_PATH


def load_pending() -> list[dict]:
    if not os.path.exists(PENDING_APPROVALS_PATH):
        return []

    with open(PENDING_APPROVALS_PATH, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_pending(items: list[dict]) -> None:
    with open(PENDING_APPROVALS_PATH, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)


def create_approval_request(
    customer_email: str,
    original_subject: str,
    source_message_id: str,
    template_id: str,
    reply_subject: str,
    reply_body: str,
    user_info: dict | None,
) -> str:
    items = load_pending()

    # Do not create duplicate approval requests for the same inbound message.
    for item in items:
        if (
            item.get("source_message_id") == source_message_id
            and item.get("status") == "pending"
        ):
            return item["approval_id"]

    approval_id = secrets.token_hex(4).upper()

    items.append({
        "approval_id": approval_id,
        "status": "pending",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "approved_at": "",
        "rejected_at": "",
        "customer_email": customer_email,
        "original_subject": original_subject,
        "source_message_id": source_message_id,
        "template_id": template_id,
        "reply_subject": reply_subject,
        "reply_body": reply_body,
        "user_info": user_info or {},
    })

    save_pending(items)
    return approval_id


def find_pending_by_id(approval_id: str) -> dict | None:
    approval_id = approval_id.upper().strip()

    for item in load_pending():
        if item.get("approval_id") == approval_id and item.get("status") == "pending":
            return item

    return None


def mark_status(approval_id: str, status: str) -> dict | None:
    items = load_pending()
    selected = None

    for item in items:
        if item.get("approval_id") == approval_id and item.get("status") == "pending":
            item["status"] = status
            if status == "approved":
                item["approved_at"] = datetime.now().isoformat(timespec="seconds")
            elif status == "rejected":
                item["rejected_at"] = datetime.now().isoformat(timespec="seconds")
            selected = item
            break

    save_pending(items)
    return selected
