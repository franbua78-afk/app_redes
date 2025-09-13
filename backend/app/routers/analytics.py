from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..deps import get_current_user
from ..db.session import get_db
from ..db.models import Analytics


router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("")
def get_analytics(user=Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.query(Analytics).filter(Analytics.user_id == user.id).all()
    return [{
        "video_id": r.video_id,
        "platform": r.platform,
        "views": r.views,
        "likes": r.likes,
        "comments": r.comments,
    } for r in rows]

