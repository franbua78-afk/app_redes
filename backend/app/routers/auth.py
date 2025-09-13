from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..db.session import get_db
from ..db.models import User
from ..security import create_access_token, hash_password, verify_password
from ..settings import settings
from ..deps import get_current_user
from ..oauth.google import get_consent_url, exchange_code_store


router = APIRouter(prefix="/auth", tags=["auth"])


class RegisterRequest(BaseModel):
    email: str
    password: str
    full_name: str | None = None


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/register")
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(email=payload.email, hashed_password=hash_password(payload.password), full_name=payload.full_name)
    db.add(user)
    db.commit()
    return {"ok": True}


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(user.email)
    return {"access_token": token, "token_type": "bearer"}


# Placeholders for platform OAuth routes
@router.get("/google")
def google_oauth_begin():
    return {"auth_url": get_consent_url()}


@router.get("/google/callback")
def google_oauth_callback(code: str, user=Depends(get_current_user), db: Session = Depends(get_db)):
    exchange_code_store(db, user.id, code)
    return {"ok": True}


@router.get("/tiktok")
def tiktok_oauth_begin():
    return {"message": "redirect to tiktok oauth", "client_id": settings.TIKTOK_CLIENT_ID}


@router.get("/tiktok/callback")
def tiktok_oauth_callback():
    return {"ok": True}


@router.get("/instagram")
def instagram_oauth_begin():
    return {"message": "redirect to instagram oauth", "client_id": settings.META_APP_ID}


@router.get("/instagram/callback")
def instagram_oauth_callback():
    return {"ok": True}

