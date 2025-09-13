from datetime import datetime, timezone
from sqlalchemy.orm import Session
from loguru import logger
from .celery_app import celery_app
from ..db.session import SessionLocal
from ..db.models import Schedule
from .upload import publish_scheduled


@celery_app.task(name="app.tasks.scheduler.dispatch_due")
def dispatch_due():
    db: Session = SessionLocal()
    try:
        now = datetime.now(timezone.utc)
        due = (
            db.query(Schedule)
            .filter(Schedule.publish_at <= now, Schedule.status == "scheduled")
            .all()
        )
        for s in due:
            logger.info(f"Dispatching schedule {s.id} for platform {s.platform}")
            publish_scheduled.delay(s.id)
    finally:
        db.close()

