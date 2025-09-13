from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from ..deps import get_current_user
from ..db.session import get_db
from ..db.models import Schedule
from ..tasks.upload import publish_scheduled


router = APIRouter(prefix="", tags=["upload"])


class UploadRequest(BaseModel):
    video_id: int
    platforms: list[str]


@router.post("/upload-video")
def upload_now(payload: UploadRequest, user=Depends(get_current_user), db: Session = Depends(get_db)):
    items = []
    for p in payload.platforms:
        s = Schedule(
            user_id=user.id,
            video_id=payload.video_id,
            platform=p,
            publish_at=datetime.now(timezone.utc),
            status="scheduled",
        )
        db.add(s)
        db.flush()
        items.append(s)
    db.commit()
    for s in items:
        publish_scheduled.delay(s.id)
    return {"ok": True, "count": len(items)}

