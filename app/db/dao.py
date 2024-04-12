from typing import Generic

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.api.schemas import CreateBookmarkSchema, CreateSchema, ModelType
from app.db.models import Bookmark
from app.utils.url_loader import URLLoader


class BaseDAO(Generic[ModelType, CreateSchema]):
    model: ModelType

    def get_by_id(self, session: Session, pk: int) -> ModelType:
        return session.get(self.model, pk)

    def get(self, session: Session, offset=0, limit=20):
        return session.query(self.model).offset(offset).limit(limit).all()

    def create(self, session: Session, obj_in: CreateSchema) -> ModelType:
        obj = self.model(**jsonable_encoder(obj_in))
        session.add(obj)
        session.commit()
        return {"ok": True}

    def delete(self, session: Session, pk: int) -> ModelType:
        obj = session.get(self.model, pk)
        session.delete(obj)
        session.commit()

    def count(self, session: Session):
        return session.query(self.model).count()


class BookmarkDAO(BaseDAO[Bookmark, CreateBookmarkSchema]):
    model = Bookmark

    def create(self, session: Session, obj_in: CreateBookmarkSchema) -> Bookmark:
        if obj_in.title is None or obj_in.title.strip() == "":
            obj_in.title = URLLoader(obj_in.url).get_title()

        return super().create(session, obj_in)
