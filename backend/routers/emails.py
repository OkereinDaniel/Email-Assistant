from fastapi import APIRouter, HTTPException
from services.gmail_service import GmailService
from agents.email_analyzer import EmailAnalyzerAgent
from agents.priority_agent import PriorityAgent

router = APIRouter()
gmail_service = GmailService()
analyzer = EmailAnalyzerAgent()
priority_agent = PriorityAgent()


@router.get("/emails")
async def get_emails(max_results: int = 20):
    """Fetch emails from Gmail, analyze and prioritize them."""
    try:
        raw_emails = gmail_service.fetch_emails(max_results=max_results)
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Gmail error: {e}")

    enriched = []
    for email in raw_emails:
        analyzed = await analyzer.analyze(email)
        prioritized = await priority_agent.classify(analyzed)
        enriched.append(prioritized)

    return {"emails": enriched}
