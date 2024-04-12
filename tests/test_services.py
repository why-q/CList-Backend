import pytest
from sqlalchemy.orm import Session

from app.api.schemas import CreateBookmarkSchema
from app.db.services import BookmarkService


class TestBookmarkService:
    @pytest.fixture()
    def service(self, init_bookmark):
        yield BookmarkService()

    def test_get(self, service: BookmarkService, session: Session):
        objs = service.get(session)
        assert len(objs) == 3
        objs = service.get(session, limit=2)
        assert len(objs) == 2
        objs = service.get(session, offset=4)
        assert not objs

    def test_total(self, service: BookmarkService, session: Session):
        total = service.total(session)
        assert total == 3

    def test_get_by_id(self, service: BookmarkService, session: Session):
        __obj = session.query(service.dao.model).first()
        obj = service.get_by_id(session, __obj.id)
        assert obj.id == __obj.id

    def test_create(self, service: BookmarkService, session: Session):
        origin_cnt = service.total(session)
        obj_in = CreateBookmarkSchema(url="https://444.com", title="444")
        service.create(session, obj_in)
        cnt = service.total(session)
        assert origin_cnt + 1 == cnt

    def test_delete(self, service: BookmarkService, session: Session):
        origin_cnt = service.total(session)
        obj = session.query(service.dao.model).first()
        service.delete(session, obj.id)
        cnt = service.total(session)
        assert origin_cnt - 1 == cnt
