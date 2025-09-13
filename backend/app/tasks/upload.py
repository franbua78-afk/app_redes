from .celery_app import celery_app
from sqlalchemy.orm import Session
from ..db.session import SessionLocal
from ..db.models import Video, Schedule
from ..uploader.youtube import YouTubeUploader
from loguru import logger


@celery_app.task(name="app.tasks.upload.publish_scheduled", bind=True, max_retries=3)
def publish_scheduled(self, schedule_id: int):
    db: Session = SessionLocal()
    try:
        sched = db.query(Schedule).filter(Schedule.id == schedule_id).first()
        if not sched:
            return
        video = db.query(Video).filter(Video.id == sched.video_id).first()
        if not video or not video.video_s3_key:
            raise ValueError("Video not ready")
        if sched.platform == "youtube":
            uploader = YouTubeUploader(db)
            uploader.upload(video, sched)
        # TODO: add TikTok and Instagram uploaders
        sched.status = "published"
        db.commit()
    except Exception as e:
        logger.exception(e)
        try:
            sched = db.query(Schedule).filter(Schedule.id == schedule_id).first()
            if sched:
                sched.status = "failed"
                sched.last_error = str(e)
                sched.attempts += 1
                db.commit()
        except Exception:
            pass
        raise self.retry(exc=e, countdown=30)
    finally:
        db.close()

