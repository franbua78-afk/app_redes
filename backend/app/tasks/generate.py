from .celery_app import celery_app
from sqlalchemy.orm import Session
from ..db.session import SessionLocal
from ..db.models import Video
from ..video.pipeline import VideoPipeline
from loguru import logger


def enqueue_generate_video(video_id: int):
    generate_video.delay(video_id)


@celery_app.task(name="app.tasks.generate.generate_video", bind=True, max_retries=3)
def generate_video(self, video_id: int):
    logger.info(f"Generating video {video_id}")
    db: Session = SessionLocal()
    try:
        video = db.query(Video).filter(Video.id == video_id).first()
        if not video:
            logger.error("Video not found")
            return
        video.status = "generating"
        db.commit()

        pipeline = VideoPipeline(db)
        pipeline.generate(video)

        video.status = "ready"
        db.commit()
    except Exception as e:
        logger.exception(e)
        try:
            video = db.query(Video).filter(Video.id == video_id).first()
            if video:
                video.status = "failed"
                video.error = str(e)
                db.commit()
        except Exception:
            pass
        raise self.retry(exc=e, countdown=10)
    finally:
        db.close()

