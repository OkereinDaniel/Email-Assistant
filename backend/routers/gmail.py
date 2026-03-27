from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from services.gmail_service import GmailService

router = APIRouter()
gmail_service = GmailService()


@router.post("/connect-gmail")
def connect_gmail():
    """Returns the OAuth URL to begin Gmail authorization."""
    auth_url = gmail_service.get_auth_url()
    return {"auth_url": auth_url}


@router.get("/auth/callback/google")
def google_callback(code: str, state: str = ""):
    """Handles the OAuth callback from Google and stores the token."""
    try:
        gmail_service.exchange_code(code)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return RedirectResponse(url="http://localhost:3000/dashboard")
