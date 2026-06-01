from __future__ import annotations

from config import DRY_RUN
from email_sender import send_email
from email_templates import (
    render_photo_confirmation_email,
    render_tracking_number_email,
)
from google_sheet import (
    load_orders_from_sheet,
    update_photo_sent_status,
    update_track_sent_status,
)


def clean(value: str | None) -> str:
    return (value or "").strip()


def is_sent(value: str | None) -> bool:
    return clean(value).upper() == "SENT"


def should_send_photo(order: dict) -> tuple[bool, str]:
    email = clean(order.get("Cust_Email"))
    photo_link = clean(order.get("Photo_link"))
    photo_status = clean(order.get("Photo_status") or order.get("Photo_statu"))

    if not email:
        return False, "missing Cust_Email"

    if not photo_link:
        return False, "missing Photo_link"

    if is_sent(photo_status):
        return False, "photo already sent"

    return True, "photo ready"


def should_send_tracking(order: dict) -> tuple[bool, str]:
    email = clean(order.get("Cust_Email"))
    track_link = clean(order.get("Track_link"))
    track_status = clean(order.get("Track_status") or order.get("Track_statu"))

    if not email:
        return False, "missing Cust_Email"

    if not track_link:
        return False, "missing Track_link"

    if is_sent(track_status):
        return False, "tracking already sent"

    return True, "tracking ready"


def send_photo_email(order: dict) -> bool:
    row_number = order["row_number"]
    email = clean(order.get("Cust_Email"))

    allowed, reason = should_send_photo(order)

    print("-" * 70)
    print(f"Photo email status: {reason}")

    if not allowed:
        return False

    subject, body, html_body = render_photo_confirmation_email(order)

    print(f"Sending photo email to: {email}")
    print(f"Subject: {subject}")

    if DRY_RUN:
        print("DRY_RUN=true, photo email not actually sent.")
    else:
        send_email(
            to_email=email,
            subject=subject,
            body=body,
            html_body=html_body,
        )
        update_photo_sent_status(row_number)
        print("Photo email sent and sheet updated.")

    return True


def send_tracking_email(order: dict) -> bool:
    row_number = order["row_number"]
    email = clean(order.get("Cust_Email"))

    allowed, reason = should_send_tracking(order)

    print("-" * 70)
    print(f"Tracking email status: {reason}")

    if not allowed:
        return False

    subject, body, html_body = render_tracking_number_email(order)

    print(f"Sending tracking email to: {email}")
    print(f"Subject: {subject}")

    if DRY_RUN:
        print("DRY_RUN=true, tracking email not actually sent.")
    else:
        send_email(
            to_email=email,
            subject=subject,
            body=body,
            html_body=html_body,
        )
        update_track_sent_status(row_number)
        print("Tracking email sent and sheet updated.")

    return True


def main() -> None:
    print("Starting Prism order email worker...")

    orders = load_orders_from_sheet()
    print(f"Loaded {len(orders)} order(s).")

    photo_count = 0
    tracking_count = 0

    for order in orders:
        row_number = order["row_number"]
        order_id = clean(order.get("Order_id"))
        email = clean(order.get("Cust_Email"))

        print("=" * 70)
        print(f"Row: {row_number}")
        print(f"Order ID: {order_id}")
        print(f"Email: {email}")

        if send_photo_email(order):
            photo_count += 1

        if send_tracking_email(order):
            tracking_count += 1

    print("=" * 70)
    print(f"Finished.")
    print(f"Photo emails processed: {photo_count}")
    print(f"Tracking emails processed: {tracking_count}")

if __name__ == "__main__":
    main()