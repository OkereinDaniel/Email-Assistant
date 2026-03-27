"""
Reply Generation Agent
Generates a professional reply suggestion that matches the sender's tone.
Uses GPT for conversational/generative tasks.
"""

from openai import AsyncOpenAI
from config import settings

client = AsyncOpenAI(api_key=settings.openai_api_key)

SYSTEM_PROMPT = """You are an email reply assistant. Write a concise, professional reply to the email below.
Rules:
- Match the sender's tone (formal if they are formal, casual if casual)
- Keep the reply under 150 words unless the email requires a detailed response
- Do NOT hallucinate facts — only respond to what is in the email
- Do NOT include a subject line, just the body of the reply
- End with an appropriate sign-off"""


class ReplyAgent:
    async def generate(self, email: dict, context: str = "") -> str:
        analysis = email.get("analysis", {})
        user_message = f"""
Email to reply to:
From: {email['sender']}
Subject: {email['subject']}
Tone: {analysis.get('tone', 'neutral')}

Body:
{email['body'][:3000]}

{"Additional context: " + context if context else ""}
"""
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            max_tokens=400,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
        )
        return response.choices[0].message.content.strip()
