from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import gmail, emails, ai_actions

app = FastAPI(
    title="AI Email Assistant API",
    description="Backend API for AI-powered inbox management",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(gmail.router, tags=["Gmail"])
app.include_router(emails.router, tags=["Emails"])
app.include_router(ai_actions.router, tags=["AI Actions"])


@app.get("/health")
def health():
    return {"status": "ok"}
