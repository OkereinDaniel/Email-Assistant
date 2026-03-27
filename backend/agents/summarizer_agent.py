"""
Summarizer Agent
Produces a concise summary of an email.
Uses Claude for summarization tasks.
"""

import anthropic
from config import settings

client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)

SYSTEM_PROMPT = """You are an email summarization assistant.
Summarize the email in 2-4 bullet points. Be concise and factual.
Do not add information that is not present in the email.
Format as a plain list without markdown headers."""


class SummarizerAgent:
    async def summarize(self, email: dict) -> str:
        user_message = f"""
Subject: {email['subject']}
From: {email['sender']}

Body:
{email['body'][:4000]}
"""
        message = await client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=256,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}],
        )
        return message.content[0].text.strip()
