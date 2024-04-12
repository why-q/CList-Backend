import pytest
from alembic import command, config
from fastapi.testclient import TestClient
from loguru import logger
from sqlalchemy.exc import SQLAlchemyError

from app.api import server
from app.config import settings
from app.db.db import SessionFactory
from app.db.models import Bookmark
from app.log import init_loguru


@pytest.fixture()
def init():
    init_loguru()


@pytest.fixture()
def migrate(init):
    alembic_cfg = config.Config(f"{settings.ALEMBIC.DIR}/alembic.ini")
    alembic_cfg.set_main_option("script_location", settings.ALEMBIC.DIR)

    logger.debug("\n----- RUN ALEMBIC MIGRATION -----\n")

    command.downgrade(alembic_cfg, "base")
    command.upgrade(alembic_cfg, "head")
    try:
        yield
    finally:
        command.downgrade(alembic_cfg, "base")


@pytest.fixture()
def session(migrate):
    _s = SessionFactory()
    yield _s
    _s.close()


@pytest.fixture()
def init_bookmark(session):
    b_1 = Bookmark(url="https://111.com", title="111")
    b_2 = Bookmark(url="https://222.com", title="222")
    b_3 = Bookmark(url="https://333.com", title="333")
    session.add_all([b_1, b_2, b_3])
    try:
        session.commit()
    except SQLAlchemyError:
        session.rollback()


@pytest.fixture()
def client():
    _s = server.Server()
    _s.init_app()
    _c = TestClient(app=_s.app)
    yield _c


def pytest_sessionfinish():
    pass
