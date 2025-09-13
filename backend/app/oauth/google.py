from datetime import datetime, timedelta, timezone
from typing import Tuple
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from sqlalchemy.orm import Session
from ..settings import settings
from ..db.models import SocialToken


YOUTUBE_SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
]


def build_flow() -> Flow:
    client_config = {
        "web": {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [settings.GOOGLE_REDIRECT_URI],
        }
    }
    flow = Flow.from_client_config(client_config, scopes=YOUTUBE_SCOPES, redirect_uri=settings.GOOGLE_REDIRECT_URI)
    return flow


def get_consent_url(state: str | None = None) -> str:
    flow = build_flow()
    auth_url, _ = flow.authorization_url(include_granted_scopes="true", access_type="offline", prompt="consent", state=state)
    return auth_url


def exchange_code_store(db: Session, user_id: int, code: str) -> None:
    flow = build_flow()
    flow.fetch_token(code=code)
    creds = flow.credentials
    expires_at = datetime.now(timezone.utc) + timedelta(seconds=creds.expiry.timestamp() - datetime.now(timezone.utc).timestamp()) if creds.expiry else None
    token = (
        db.query(SocialToken)
        .filter(SocialToken.user_id == user_id, SocialToken.platform == "youtube")
        .first()
    )
    if not token:
        token = SocialToken(user_id=user_id, platform="youtube")
        db.add(token)
    token.access_token = creds.token
    token.refresh_token = creds.refresh_token or token.refresh_token
    token.expires_at = creds.expiry
    token.scope = " ".join(YOUTUBE_SCOPES)
    token.extra = {"token_uri": "https://oauth2.googleapis.com/token"}
    db.commit()


def ensure_fresh_credentials(db: Session, token: SocialToken) -> Credentials:
    creds = Credentials(
        token=token.access_token,
        refresh_token=token.refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=settings.GOOGLE_CLIENT_ID,
        client_secret=settings.GOOGLE_CLIENT_SECRET,
        scopes=YOUTUBE_SCOPES,
    )
    if not creds.valid and creds.refresh_token:
        creds.refresh(request=_GoogleRequest())
        token.access_token = creds.token
        token.expires_at = datetime.fromtimestamp(creds.expiry.timestamp(), tz=timezone.utc) if creds.expiry else None
        db.commit()
    return creds


class _GoogleRequest:
    # Minimal adapter for google.auth.transport.requests.Request
    def __call__(self, *args, **kwargs):
        import requests
        session = requests.Session()
        return session

