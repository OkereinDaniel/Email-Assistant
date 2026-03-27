"""
Task Extraction Agent
Detects actionable tasks, deadlines, and owners from email content.
Uses Claude for structured data extraction.
"""

import anthropic
import json
from config import settings

client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)

SYSTEM_PROMPT = """You are a task extraction agent. Extract all actionable tasks from the email.

Return ONLY valid JSON:
{
  "tasks": [
    {
      "title": "<short task title>",
      "description": "<what needs to be done>",
      "owner": "<person responsible, or 'me' if the recipient>",
      "due_date": "<ISO date string or null>",
      "priority": "<high|medium|low>"
    }
  ]
}

If there are no tasks, return {"tasks": []}."""


class TaskAgent:
    async def extract(self, email: dict) -> list[dict]:
        user_message = f"""
Subject: {email['subject']}
From: {email['sender']}
Date: {email.get('date', '')}

Body:
{email['body'][:4000]}
"""
        message = await client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=512,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}],
        )

        try:
            result = json.loads(message.content[0].text)
            return result.get("tasks", [])
        except json.JSONDecodeError:
            return []
