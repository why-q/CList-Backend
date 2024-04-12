import pytest
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.api.schemas import ModelType
from app.db.models import Bookmark


def test_docs(client):
    response = client.get("/docs")
    assert response.status_code == 200


class BaseTest:
    version = "v1"
    base_url: str
    model: ModelType

    @pytest.fixture()
    def init_data(self):
        pass

    def url(self, pk: int = None) -> str:
        url_split = ["api", self.version, self.base_url]
        if pk:
            url_split.append(str(pk))
        return "/".join(url_split)

    def assert_response_ok(self, response: Response):
        assert response.status_code == 200

    def test_get(self, client: TestClient, session: Session, init_data):
        cnt = session.query(self.model).count()
        response = client.get(self.url())
        self.assert_response_ok(response)
        assert cnt == len(response.json())

    def test_get_by_id(self, client: TestClient, session: Session, init_data):
        obj = session.query(self.model).first()
        response = client.get(self.url(obj.id))
        self.assert_response_ok(response)
        assert jsonable_encoder(obj) == response.json()

    def test_delete(self, client: TestClient, session: Session, init_data):
        origin_cnt = session.query(self.model).count()
        session.close()
        response = client.delete(self.url(1))
        self.assert_response_ok(response)
        cnt = session.query(self.model).count()
        assert cnt == 2
        assert origin_cnt - 1 == cnt


class TestBookmark(BaseTest):
    model = Bookmark
    base_url = "bookmarks"

    @pytest.fixture()
    def init_data(self, init_bookmark):
        pass

    def test_create(self, client: TestClient, session: Session, init_data):
        response = client.post(
            self.url(), json={"url": "https://example.com", "title": ""}
        )
        self.assert_response_ok(response)
        assert response.json().get("ok")
