import pytest
from sqlalchemy.orm import Session

from app.api.schemas import CreateBookmarkSchema
from app.db.dao import BookmarkDAO


class TestBookmark:

    @pytest.fixture()
    def dao(self, init_bookmark):
        yield BookmarkDAO()

    def test_count(self, dao: BookmarkDAO, session: Session):
        cnt = dao.count(session)
        assert cnt == 3

    def test_get(self, dao: BookmarkDAO, session: Session):
        bookmarks = dao.get(session)
        assert len(bookmarks) == 3
        bookmarks = dao.get(session, limit=2)
        assert len(bookmarks) == 2
        bookmarks = dao.get(session, offset=4)
        assert not bookmarks

    def test_get_by_id(self, dao: BookmarkDAO, session: Session):
        bookmarks = dao.get_by_id(session, 1)
        assert bookmarks.id == 1

    def test_create(self, dao: BookmarkDAO, session: Session):
        origin_cnt = session.query(dao.model).count()
        obj_in = CreateBookmarkSchema(url='https://mp.weixin.qq.com/s/vfB_rB9K79P6mxUB0U8xhg')
        dao.create(session, obj_in)
        cnt = session.query(dao.model).count()
        assert origin_cnt + 1 == cnt

    def test_delete(self, dao: BookmarkDAO, session: Session):
        origin_cnt = session.query(dao.model).count()
        dao.delete(session, 1)
        cnt = session.query(dao.model).count()
        assert origin_cnt - 1 == cnt

    