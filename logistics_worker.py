from __future__ import annotations

from config import DRY_RUN
from email_sender import send_email
from google_sheet import load_orders_from_sheet, update_order_sent_status


def build_logistics_email(order: dict) -> tuple[str, str]:
    name = order.get("name") or "there"
    order_id = order.get("order_id") or ""
    logistics_link = order.get("logistics_link") or ""

    subject = "Your logistics tracking information"

    if order_id:
        subject = f"Your logistics tracking information - {order_id}"

    body = f"""Hi {name},

Your logistics tracking link is now available:

{logistics_link}

Please use this link to check the latest delivery status.

Best,
Zewen"""

    return subject, body


def should_send(order: dict) -> tuple[bool, str]:
    email = order.get("email", "").strip()
    logistics_link = order.get("logistics_link", "").strip()
    sent_status = order.get("sent_status", "").strip().upper()

    if not email:
        return False, "missing email"

    if not logistics_link:
        return False, "missing logistics_link"

    if sent_status == "SENT":
        return False, "already sent"

    return True, "ready"


def main() -> None:
    print("Starting logistics worker...")

    orders = load_orders_from_sheet()
    print(f"Loaded {len(orders)} order(s).")

    sent_count = 0

    for order in orders:
        row_number = order["row_number"]
        email = order.get("email", "")

        allowed, reason = should_send(order)

        print("=" * 70)
        print(f"Row: {row_number}")
        print(f"Email: {email}")
        print(f"Status: {reason}")

        if not allowed:
            continue

        subject, body = build_logistics_email(order)

        print(f"Subject: {subject}")
        print("-" * 70)
        print(body)
        print("-" * 70)

        if DRY_RUN:
            print("DRY_RUN=true, not sending email.")
        else:
            send_email(
                to_email=email,
                subject=subject,
                body=body,
            )
            update_order_sent_status(row_number)
            print("Email sent and sheet updated.")

        sent_count += 1

    print("=" * 70)
    print(f"Finished. Processed sendable orders: {sent_count}")


if __name__ == "__main__":
    main()