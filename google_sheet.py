from __future__ import annotations

import json
import os
from datetime import datetime

from google.oauth2 import service_account
from googleapiclient.discovery import build

from config import GOOGLE_SHEET_ID, GOOGLE_SHEET_RANGE, GOOGLE_CREDENTIALS_JSON


SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def get_google_credentials():
    """
    Load Google credentials using Service Account.

    Local:
        credentials.json

    GitHub Actions:
        GOOGLE_CREDENTIALS_JSON_CONTENT
    """

    raw = os.getenv("GOOGLE_CREDENTIALS_JSON_CONTENT", "").strip()

    if raw:
        info = json.loads(raw)
        return service_account.Credentials.from_service_account_info(
            info,
            scopes=SCOPES,
        )

    if os.path.exists(GOOGLE_CREDENTIALS_JSON):
        return service_account.Credentials.from_service_account_file(
            GOOGLE_CREDENTIALS_JSON,
            scopes=SCOPES,
        )

    if os.path.exists("credentials.json"):
        return service_account.Credentials.from_service_account_file(
            "credentials.json",
            scopes=SCOPES,
        )

    raise FileNotFoundError(
        "No Google service account credentials found. "
        "Please provide credentials.json or GOOGLE_CREDENTIALS_JSON_CONTENT."
    )


def get_sheet_service():
    creds = get_google_credentials()
    return build("sheets", "v4", credentials=creds)


def load_orders_from_sheet() -> list[dict]:
    service = get_sheet_service()

    result = service.spreadsheets().values().get(
        spreadsheetId=GOOGLE_SHEET_ID,
        range=GOOGLE_SHEET_RANGE,
    ).execute()

    rows = result.get("values", [])

    if not rows:
        return []

    headers = [h.strip() for h in rows[0]]
    orders = []

    for index, row in enumerate(rows[1:], start=2):
        record = {"row_number": index}

        for i, header in enumerate(headers):
            record[header] = row[i].strip() if i < len(row) else ""

        orders.append(record)

    return orders


def update_photo_sent_status(row_number: int) -> None:
    service = get_sheet_service()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    body = {
        "values": [["SENT", now]]
    }

    service.spreadsheets().values().update(
        spreadsheetId=GOOGLE_SHEET_ID,
        range=f"Sheet1!R{row_number}:S{row_number}",
        valueInputOption="USER_ENTERED",
        body=body,
    ).execute()


def update_track_sent_status(row_number: int) -> None:
    service = get_sheet_service()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    body = {
        "values": [["SENT", now]]
    }

    service.spreadsheets().values().update(
        spreadsheetId=GOOGLE_SHEET_ID,
        range=f"Sheet1!U{row_number}:V{row_number}",
        valueInputOption="USER_ENTERED",
        body=body,
    ).execute()
