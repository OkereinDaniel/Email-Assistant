from __future__ import annotations

from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import base64
import json
import os

from config import settings

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.modify",
]

# In production, store credentials in Supabase per user
_token_store: dict = {}


class GmailService:
    def get_auth_url(self) -> str:
        flow = self._build_flow()
        auth_url, _ = flow.authorization_url(prompt="consent", access_type="offline")
        return auth_url

    def exchange_code(self, code: str) -> None:
        flow = self._build_flow()
        flow.fetch_token(code=code)
        creds = flow.credentials
        # Store serialized credentials (in production: per-user in Supabase)
        _token_store["default"] = json.loads(creds.to_json())

    def _get_credentials(self) -> Credentials:
        token_data = _token_store.get("default")
        if not token_data:
            raise ValueError("Gmail not connected. Authorize first via /connect-gmail.")
        return Credentials.from_authorized_user_info(token_data, SCOPES)

    def _build_service(self):
        creds = self._get_credentials()
        return build("gmail", "v1", credentials=creds)

    def fetch_emails(self, max_results: int = 20) -> list[dict]:
        service = self._build_service()
        results = (
            service.users()
            .messages()
            .list(userId="me", maxResults=max_results, labelIds=["INBOX"])
            .execute()
        )
        messages = results.get("messages", [])
        emails = []
        for msg in messages:
            full = service.users().messages().get(userId="me", id=msg["id"], format="full").execute()
            emails.append(self._parse_message(full))
        return emails

    def get_email(self, email_id: str) -> dict | None:
        try:
            service = self._build_service()
            full = service.users().messages().get(userId="me", id=email_id, format="full").execute()
            return self._parse_message(full)
        except Exception:
            return None

    def _parse_message(self, msg: dict) -> dict:
        headers = {h["name"]: h["value"] for h in msg["payload"].get("headers", [])}
        body = self._extract_body(msg["payload"])
        return {
            "id": msg["id"],
            "subject": headers.get("Subject", "(no subject)"),
            "sender": headers.get("From", ""),
            "to": headers.get("To", ""),
            "date": headers.get("Date", ""),
            "body": body,
            "snippet": msg.get("snippet", ""),
            "label_ids": msg.get("labelIds", []),
        }

    def _extract_body(self, payload: dict) -> str:
        if "body" in payload and payload["body"].get("data"):
            return base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8", errors="replace")
        for part in payload.get("parts", []):
            if part.get("mimeType") == "text/plain":
                data = part.get("body", {}).get("data", "")
                if data:
                    return base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")
        return ""

    def _build_flow(self) -> Flow:
        client_config = {
            "web": {
                "client_id": settings.google_client_id,
                "client_secret": settings.google_client_secret,
                "redirect_uris": [settings.google_redirect_uri],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        }
        return Flow.from_client_config(client_config, scopes=SCOPES, redirect_uri=settings.google_redirect_uri)
