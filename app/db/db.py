from sqlalchemy.engine import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from app.config import settings

url = settings.DATABASE.URL
engine = create_engine(url, connect_args={"check_same_thread": False})
SessionFactory = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)
ScopedSession = scoped_session(SessionFactory)
