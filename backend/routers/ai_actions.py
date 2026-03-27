from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from agents.reply_agent import ReplyAgent
from agents.summarizer_agent import SummarizerAgent
from agents.task_agent import TaskAgent
from agents.meeting_agent import MeetingAgent
from services.gmail_service import GmailService

router = APIRouter()
gmail_service = GmailService()
reply_agent = ReplyAgent()
summarizer = SummarizerAgent()
task_agent = TaskAgent()
meeting_agent = MeetingAgent()


class EmailActionRequest(BaseModel):
    email_id: str
    context: str = ""


@router.post("/generate-reply")
async def generate_reply(req: EmailActionRequest):
    email = gmail_service.get_email(req.email_id)
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    reply = await reply_agent.generate(email, context=req.context)
    return {"reply": reply}


@router.post("/summarize-email")
async def summarize_email(req: EmailActionRequest):
    email = gmail_service.get_email(req.email_id)
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    summary = await summarizer.summarize(email)
    return {"summary": summary}


@router.post("/extract-task")
async def extract_task(req: EmailActionRequest):
    email = gmail_service.get_email(req.email_id)
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    tasks = await task_agent.extract(email)
    return {"tasks": tasks}


@router.post("/schedule-meeting")
async def schedule_meeting(req: EmailActionRequest):
    email = gmail_service.get_email(req.email_id)
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    result = await meeting_agent.detect_and_suggest(email)
    return result
