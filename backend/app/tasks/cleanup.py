import os
import shutil
from .celery_app import celery_app


@celery_app.task(name="app.tasks.cleanup.clean_tmp")
def clean_tmp():
    tmp = "/app/tmp"
    if os.path.isdir(tmp):
        for name in os.listdir(tmp):
            path = os.path.join(tmp, name)
            try:
                if os.path.isdir(path):
                    shutil.rmtree(path, ignore_errors=True)
                else:
                    os.remove(path)
            except Exception:
                pass

