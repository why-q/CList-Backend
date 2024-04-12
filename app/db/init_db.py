import os

from app.config import settings
from app.db.db import engine
from app.db.models import BaseModel


def init_db():
    db_path = settings.DATABASE.PATH
    if not os.path.exists(db_path):
        BaseModel.metadata.create_all(bind=engine)


def remove_db():
    db_path = settings.DATABASE.PATH
    if os.path.exists(db_path):
        os.remove(db_path)
