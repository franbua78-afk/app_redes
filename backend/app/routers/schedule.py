from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime
from ..deps import get_current_user
from ..db.session import get_db
from ..db.models import Schedule


router = APIRouter(prefix="/schedule", tags=["schedule"])


class ScheduleRequest(BaseModel):
    video_id: int
    platforms: list[str]
    publish_at: datetime


@router.post("")
def create_schedule(payload: ScheduleRequest, user=Depends(get_current_user), db: Session = Depends(get_db)):
    items = []
    for p in payload.platforms:
        items.append(Schedule(user_id=user.id, video_id=payload.video_id, platform=p, publish_at=payload.publish_at))
    db.add_all(items)
    db.commit()
    return {"ok": True, "count": len(items)}


@router.get("")
def list_schedule(user=Depends(get_current_user), db: Session = Depends(get_db)):
    items = db.query(Schedule).filter(Schedule.user_id == user.id).order_by(Schedule.publish_at.desc()).all()
    return [{
        "id": s.id,
        "video_id": s.video_id,
        "platform": s.platform,
        "publish_at": s.publish_at,
        "status": s.status,
    } for s in items]

