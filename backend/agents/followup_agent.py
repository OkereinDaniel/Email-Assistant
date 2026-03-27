"""
Follow-up Monitoring Agent
Scans sent emails that have not received a reply within a configurable
window and generates follow-up reminders.
Uses Claude to draft the reminder message.
"""

import anthropic
from config import settings

client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)

SYSTEM_PROMPT = """You are a follow-up reminder agent.
Given a sent email that has not received a reply, write a short, polite follow-up message.
Keep it under 80 words. Do not be pushy. Include a natural opening referencing the original email."""


class FollowUpAgent:
    async def generate_reminder(self, original_email: dict) -> str:
        user_message = f"""
Original email I sent:
To: {original_email.get('to', '')}
Subject: {original_email['subject']}
Sent: {original_email.get('date', '')}

Body:
{original_email['body'][:2000]}
"""
        message = await client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=200,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}],
        )
        return message.content[0].text.strip()

    async def scan_for_followups(self, sent_emails: list[dict], days_threshold: int = 3) -> list[dict]:
        """
        Given a list of sent emails, return those that need a follow-up.
        In production, this checks reply status via Gmail thread API.
        """
        # TODO: filter by thread reply status and date threshold via Gmail API
        flagged = []
        for email in sent_emails:
            # Placeholder: flag all sent emails for now
            reminder = await self.generate_reminder(email)
            flagged.append({**email, "follow_up_reminder": reminder})
        return flagged
