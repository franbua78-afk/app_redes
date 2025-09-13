from fastapi import APIRouter
import psutil


router = APIRouter(prefix="/system", tags=["system"])


@router.get("/metrics")
def metrics():
    return {
        "cpu_percent": psutil.cpu_percent(interval=0.1),
        "memory": psutil.virtual_memory()._asdict(),
        "disk": psutil.disk_usage("/")._asdict(),
    }

