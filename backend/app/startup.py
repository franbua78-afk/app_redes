from sqlalchemy import inspect
from .db.session import engine
from .db.models import Base
from loguru import logger


def init_db():
    inspector = inspect(engine)
    if not inspector.has_table("users"):
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)

