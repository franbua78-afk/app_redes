from fastapi import APIRouter, Depends, BackgroundTasks
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..deps import get_current_user
from ..db.session import get_db
from ..db.models import Video
from ..tasks.generate import enqueue_generate_video
from ..storage.s3 import S3Storage


router = APIRouter(prefix="", tags=["videos"])


class GenerateRequest(BaseModel):
    topic: str
    duration: int
    style: str
    voice: str
    music: str
    captions: bool = True
    platforms: dict
    publish: str = "now"  # now | schedule


@router.post("/generate-video")
def generate_video(payload: GenerateRequest, user=Depends(get_current_user), db: Session = Depends(get_db)):
    video = Video(user_id=user.id, topic=payload.topic, params=payload.model_dump(), status="pending")
    db.add(video)
    db.commit()
    db.refresh(video)
    enqueue_generate_video(video.id)
    return {"video_id": video.id, "status": video.status}


@router.get("/videos/{video_id}")
def get_video(video_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    video = db.query(Video).filter(Video.id == video_id, Video.user_id == user.id).first()
    if not video:
        return {"error": "not found"}
    storage = S3Storage()
    return {
        "id": video.id,
        "status": video.status,
        "script_text": video.script_text,
        "video_url": storage.get_url(video.video_s3_key) if video.video_s3_key else None,
        "thumbnail_url": storage.get_url(video.thumbnail_s3_key) if video.thumbnail_s3_key else None,
        "error": video.error,
    }


@router.get("/videos")
def list_videos(user=Depends(get_current_user), db: Session = Depends(get_db)):
    videos = db.query(Video).filter(Video.user_id == user.id).order_by(Video.created_at.desc()).limit(50).all()
    storage = S3Storage()
    return [{
        "id": v.id,
        "topic": v.topic,
        "status": v.status,
        "thumbnail_url": storage.get_url(v.thumbnail_s3_key) if v.thumbnail_s3_key else None,
        "created_at": v.created_at.isoformat(),
    } for v in videos]

