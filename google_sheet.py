from __future__ import annotations

import json
import os
from datetime import datetime

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from config import GOOGLE_SHEET_ID, GOOGLE_SHEET_RANGE, GOOGLE_CREDENTIALS_JSON

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def load_token_info():
    raw = os.getenv("GOOGLE_TOKEN_JSON", "").strip()
    if raw:
        return json.loads(raw)

    if os.path.exists("token.json"):
        with open("token.json", "r", encoding="utf-8") as f:
            return json.load(f)

    return None


def load_client_config():
    raw = os.getenv("GOOGLE_CREDENTIALS_JSON_CONTENT", "").strip()
    if raw:
        return json.loads(raw)

    with open(GOOGLE_CREDENTIALS_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def get_google_credentials():
    token_info = load_token_info()

    if token_info:
        creds = Credentials.from_authorized_user_info(token_info, SCOPES)

        if creds.expired and creds.refresh_token:
            creds.refresh(Request())

        return creds

    client_config = load_client_config()
    flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
    creds = flow.run_local_server(port=0)

    with open("token.json", "w", encoding="utf-8") as token:
        token.write(creds.to_json())

    return creds


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


def update_order_sent_status(row_number: int) -> None:
    service = get_sheet_service()

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    body = {
        "values": [["SENT", now]]
    }

    service.spreadsheets().values().update(
        spreadsheetId=GOOGLE_SHEET_ID,
        range=f"Sheet1!E{row_number}:F{row_number}",
        valueInputOption="USER_ENTERED",
        body=body,
    ).execute()