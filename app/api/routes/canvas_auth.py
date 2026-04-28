import os
import time

from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse

from app.repositories.canvas_token_repository import CanvasTokenRepository
from app.services.canvas_oauth_service import CanvasOAuthService

router = APIRouter(prefix="/canvas/oauth", tags=["canvas-oauth"])


@router.get("/start")
def start_canvas_oauth():
    service = CanvasOAuthService()

    canvas_base_url = os.getenv("CANVAS_BASE_URL")
    client_id = os.getenv("CANVAS_CLIENT_ID")
    redirect_uri = os.getenv(
        "CANVAS_REDIRECT_URI",
        "http://127.0.0.1:8000/canvas/oauth/callback",
    )

    if not canvas_base_url or not client_id:
        raise HTTPException(
            status_code=400,
            detail="CANVAS_BASE_URL and CANVAS_CLIENT_ID must be set.",
        )

    url = service.build_authorization_url(
        base_url=canvas_base_url,
        client_id=client_id,
        redirect_uri=redirect_uri,
        state="demo-state",
    )

    return RedirectResponse(url)


@router.get("/callback")
def canvas_oauth_callback(code: str | None = None):
    if code is None:
        raise HTTPException(status_code=400, detail="Missing OAuth code")

    canvas_base_url = os.getenv("CANVAS_BASE_URL")
    client_id = os.getenv("CANVAS_CLIENT_ID")
    client_secret = os.getenv("CANVAS_CLIENT_SECRET")
    redirect_uri = os.getenv(
        "CANVAS_REDIRECT_URI",
        "http://127.0.0.1:8000/canvas/oauth/callback",
    )

    if not canvas_base_url or not client_id or not client_secret:
        raise HTTPException(
            status_code=400,
            detail="CANVAS_BASE_URL, CANVAS_CLIENT_ID, and CANVAS_CLIENT_SECRET must be set.",
        )

    service = CanvasOAuthService()

    token_data = service.exchange_code_for_token(
        base_url=canvas_base_url,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        code=code,
    )

    access_token = token_data.get("access_token")
    refresh_token = token_data.get("refresh_token")
    expires_in = token_data.get("expires_in")

    if not access_token:
        raise HTTPException(
            status_code=502,
            detail="Canvas did not return an access token.",
        )

    expires_at = int(time.time()) + int(expires_in) if expires_in else None

    repo = CanvasTokenRepository()
    repo.save_token(
        profile_key="default",
        canvas_base_url=canvas_base_url,
        access_token=access_token,
        refresh_token=refresh_token,
        expires_at=expires_at,
    )

    return {
        "status": "canvas_connected",
        "profile_key": "default",
        "expires_at": expires_at,
    }