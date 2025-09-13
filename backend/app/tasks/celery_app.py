from celery import Celery
from ..settings import settings


celery_app = Celery(
    "ai_shorts_studio",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

celery_app.conf.task_routes = {
    "app.tasks.generate.*": {"queue": "generate"},
    "app.tasks.upload.*": {"queue": "upload"},
    "app.tasks.cleanup.*": {"queue": "cleanup"},
}

# Beat schedule for periodic tasks
celery_app.conf.beat_schedule = {
    "dispatch-due-every-minute": {
        "task": "app.tasks.scheduler.dispatch_due",
        "schedule": 60.0,
    },
    "clean-tmp-every-30-min": {
        "task": "app.tasks.cleanup.clean_tmp",
        "schedule": 1800.0,
    },
}

