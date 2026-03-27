"""
Email Analyzer Agent
Parses incoming email content and extracts structured metadata:
sender intent, key entities, tone, and conversation context.
Uses Claude for classification tasks.
"""

import anthropic
from config import settings

client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)

SYSTEM_PROMPT = """You are an email analysis agent. Given a raw email, extract structured metadata.

Return ONLY valid JSON with these fields:
{
  "intent": "<string: one of reply_requested, fyi, action_required, meeting_request, follow_up, spam>",
  "tone": "<string: one of formal, casual, urgent, friendly, neutral>",
  "key_entities": ["<person or org names mentioned>"],
  "has_deadline": <boolean>,
  "deadline": "<ISO date string or null>",
  "summary_one_line": "<one sentence summary of the email>"
}"""


class EmailAnalyzerAgent:
    async def analyze(self, email: dict) -> dict:
        """Analyze a raw email dict and return enriched metadata."""
        user_message = f"""
Subject: {email['subject']}
From: {email['sender']}
Date: {email['date']}

Body:
{email['body'][:3000]}
"""
        message = await client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=512,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}],
        )

        import json
        try:
            analysis = json.loads(message.content[0].text)
        except json.JSONDecodeError:
            analysis = {"intent": "fyi", "tone": "neutral", "key_entities": [], "has_deadline": False, "deadline": None, "summary_one_line": ""}

        return {**email, "analysis": analysis}
