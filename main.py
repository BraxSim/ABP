from __future__ import annotations

import re

from config import (
    DRY_RUN,
    MAX_EMAILS_PER_RUN,
    MARK_AS_READ_AFTER_PROCESS,
    EMPLOYEE_APPROVAL_EMAIL,
    APPROVAL_KEYWORD,
    REJECTION_KEYWORD,
)

from email_reader import fetch_unread_emails, mark_email_as_read
from google_sheet import find_user_by_email
from renderer import render_template
from email_sender import send_email
from safety import should_auto_send
from logger import already_replied, daily_limit_reached, record_sent
from approval_store import (
    create_approval_request,
    find_pending_by_id,
    mark_status,
)


def get_profile_link(user_info: dict | None) -> str:
    if not user_info:
        return ""

    return (
        user_info.get("profile_link")
        or user_info.get("profile_url")
        or user_info.get("link")
        or ""
    ).strip()


def extract_approval_command(email_item: dict) -> tuple[str, str] | None:
    text = f"{email_item.get('subject', '')}\n{email_item.get('body', '')}"
    approve = re.search(rf"\b{re.escape(APPROVAL_KEYWORD)}\s+([A-Fa-f0-9]{{8}})\b", text)
    reject = re.search(rf"\b{re.escape(REJECTION_KEYWORD)}\s+([A-Fa-f0-9]{{8}})\b", text)

    if approve:
        return "approved", approve.group(1).upper()

    if reject:
        return "rejected", reject.group(1).upper()

    return None


def process_employee_approval_reply(email_item: dict) -> bool:
    from_email = email_item.get("from_email", "").lower().strip()

    if not EMPLOYEE_APPROVAL_EMAIL or from_email != EMPLOYEE_APPROVAL_EMAIL:
        return False

    command = extract_approval_command(email_item)

    if not command:
        print("Employee email found, but no approval command detected.")
        return True

    status, approval_id = command
    pending = find_pending_by_id(approval_id)

    if not pending:
        print(f"No pending approval found for {approval_id}.")
        return True

    if status == "rejected":
        mark_status(approval_id, "rejected")
        print(f"Approval {approval_id} rejected. Customer email not sent.")
        return True

    if daily_limit_reached():
        print("Skipped approved send: daily send limit reached.")
        return True

    customer_email = pending["customer_email"]
    reply_subject = pending["reply_subject"]
    reply_body = pending["reply_body"]

    print(f"Approval {approval_id} approved.")
    print(f"Customer: {customer_email}")
    print(f"Subject: {reply_subject}")
    print("-" * 70)
    print(reply_body)
    print("-" * 70)

    if DRY_RUN:
        print("DRY_RUN=true, approved customer email not actually sent.")
    else:
        send_email(
            to_email=customer_email,
            subject=reply_subject,
            body=reply_body,
        )
        print("Approved customer email sent.")

    mark_status(approval_id, "approved")

    record_sent(
        message_id=pending.get("source_message_id", ""),
        from_email=customer_email,
        subject=pending.get("original_subject", ""),
        template_id=pending.get("template_id", "customer_profile_link"),
        dry_run=DRY_RUN,
    )

    return True


def send_approval_request_to_employee(
    approval_id: str,
    customer_email: str,
    user_info: dict,
    reply_subject: str,
    reply_body: str,
) -> None:
    profile_link = get_profile_link(user_info)

    approval_subject = f"Approval required: send profile link to {customer_email}"
    approval_body = f"""Please review this automated email before it is sent.

Approval ID: {approval_id}
Customer email: {customer_email}
Customer name: {user_info.get("name", "")}
Profile link: {profile_link}

Draft email:
----------------------------------------------------------------------
Subject: {reply_subject}

{reply_body}
----------------------------------------------------------------------

To approve, reply exactly:
{APPROVAL_KEYWORD} {approval_id}

To reject, reply exactly:
{REJECTION_KEYWORD} {approval_id}
"""

    print(f"Approval request subject: {approval_subject}")
    print("-" * 70)
    print(approval_body)
    print("-" * 70)

    if DRY_RUN:
        print("DRY_RUN=true, approval request not actually sent.")
        return

    if not EMPLOYEE_APPROVAL_EMAIL:
        raise ValueError("EMPLOYEE_APPROVAL_EMAIL is missing in .env")

    send_email(
        to_email=EMPLOYEE_APPROVAL_EMAIL,
        subject=approval_subject,
        body=approval_body,
    )
    print("Approval request sent to employee.")


def process_customer_email(email_item: dict) -> None:
    from_email = email_item.get("from_email", "")
    subject = email_item.get("subject", "")
    message_id = email_item.get("message_id", "")
    imap_id = email_item.get("imap_id", "")

    print("=" * 70)
    print(f"From: {from_email}")
    print(f"Subject: {subject}")

    if already_replied(message_id, from_email, subject):
        print("Skipped: already replied before.")
        return

    user_info = find_user_by_email(from_email)

    if not user_info:
        print("No matching user found in Google Sheet.")
        return

    profile_link = get_profile_link(user_info)

    if not profile_link:
        print("Skipped: user found, but no profile_link/profile_url/link column value.")
        return

    allowed, reason = should_auto_send(email_item, user_info)

    if not allowed:
        print(f"Skipped: {reason}")
        return

    template_id = "customer_profile_link"
    reply_subject, reply_body = render_template(
        template_id=template_id,
        user_info=user_info,
        original_subject=subject,
    )

    approval_id = create_approval_request(
        customer_email=from_email,
        original_subject=subject,
        source_message_id=message_id,
        template_id=template_id,
        reply_subject=reply_subject,
        reply_body=reply_body,
        user_info=user_info,
    )

    send_approval_request_to_employee(
        approval_id=approval_id,
        customer_email=from_email,
        user_info=user_info,
        reply_subject=reply_subject,
        reply_body=reply_body,
    )

    if MARK_AS_READ_AFTER_PROCESS and imap_id:
        mark_email_as_read(imap_id)
        print("Marked as read.")


def process_one_email(email_item: dict) -> None:
    if process_employee_approval_reply(email_item):
        return

    process_customer_email(email_item)


def main() -> None:
    print("Starting approval-based profile-link email bot...")
    print(f"DRY_RUN: {DRY_RUN}")
    print(f"MAX_EMAILS_PER_RUN: {MAX_EMAILS_PER_RUN}")

    emails = fetch_unread_emails(limit=MAX_EMAILS_PER_RUN)

    if not emails:
        print("No unread emails found.")
        return

    print(f"Found {len(emails)} unread email(s).")

    for email_item in emails:
        try:
            process_one_email(email_item)
        except Exception as e:
            print("=" * 70)
            print("Error while processing email:")
            print(e)


if __name__ == "__main__":
    main()
