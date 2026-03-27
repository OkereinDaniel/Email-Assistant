"""
Meeting Detection Agent
Detects meeting requests in emails and suggests available time slots
from Google Calendar.
Uses Claude for detection + structured extraction.
"""

import anthropic
import json
from config import settings

client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)

DETECTION_PROMPT = """You are a meeting detection agent. Determine if the email contains a meeting request or scheduling ask.

Return ONLY valid JSON:
{
  "is_meeting_request": <boolean>,
  "proposed_times": ["<ISO datetime or natural language time mention>"],
  "duration_minutes": <number or null>,
  "meeting_type": "<call|video|in_person|unknown or null>",
  "notes": "<any relevant scheduling context>"
}"""


class MeetingAgent:
    async def detect_and_suggest(self, email: dict) -> dict:
        user_message = f"""
Subject: {email['subject']}
From: {email['sender']}
Date: {email.get('date', '')}

Body:
{email['body'][:3000]}
"""
        message = await client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=256,
            system=DETECTION_PROMPT,
            messages=[{"role": "user", "content": user_message}],
        )

        try:
            detection = json.loads(message.content[0].text)
        except json.JSONDecodeError:
            detection = {"is_meeting_request": False}

        if not detection.get("is_meeting_request"):
            return {"is_meeting_request": False, "suggested_slots": []}

        # TODO: Call Google Calendar API to fetch real availability
        # For now return placeholder slots
        suggested_slots = [
            "Tomorrow at 10:00 AM",
            "Tomorrow at 2:00 PM",
            "Day after tomorrow at 11:00 AM",
        ]

        return {
            "is_meeting_request": True,
            "proposed_times": detection.get("proposed_times", []),
            "duration_minutes": detection.get("duration_minutes"),
            "meeting_type": detection.get("meeting_type"),
            "notes": detection.get("notes", ""),
            "suggested_slots": suggested_slots,
        }
