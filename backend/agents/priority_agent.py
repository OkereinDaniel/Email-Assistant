"""
Priority Agent
Classifies emails as urgent / important / normal / low based on
content, sender, intent, and deadline signals.
Uses Claude for classification.
"""

import anthropic
import json
from config import settings

client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)

SYSTEM_PROMPT = """You are an email priority classifier. Classify the given email into one of:
- urgent: requires immediate attention (today)
- important: should be handled within 24-48 hours
- normal: standard email, can be handled within a week
- low: newsletters, notifications, FYI emails

Return ONLY valid JSON:
{"priority": "<urgent|important|normal|low>", "reason": "<one sentence explaining why>"}"""


class PriorityAgent:
    async def classify(self, email: dict) -> dict:
        analysis = email.get("analysis", {})
        user_message = f"""
Subject: {email['subject']}
From: {email['sender']}
Intent: {analysis.get('intent', 'unknown')}
Has deadline: {analysis.get('has_deadline', False)}
Deadline: {analysis.get('deadline', 'none')}
Tone: {analysis.get('tone', 'neutral')}
Summary: {analysis.get('summary_one_line', '')}
"""
        message = await client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=128,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}],
        )

        try:
            result = json.loads(message.content[0].text)
        except json.JSONDecodeError:
            result = {"priority": "normal", "reason": "Could not classify."}

        return {
            **email,
            "priority": result["priority"],
            "priority_reason": result["reason"],
            "is_read": False,
            "preview": email.get("snippet", "")[:100],
            "received_at": email.get("date", ""),
        }
