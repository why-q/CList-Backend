from typing import Generic, List

from sqlalchemy.orm import Session

from app.api.schemas import CreateSchema, ModelType
from app.db.dao import BaseDAO, BookmarkDAO
from app.db.models import Bookmark


class BaseService(Generic[ModelType, CreateSchema]):
    dao: BaseDAO

    def get(self, session: Session, offset=0, limit=20) -> List[ModelType]:
        return self.dao.get(session, offset, limit)

    def get_by_id(self, session: Session, pk: int) -> ModelType:
        return self.dao.get_by_id(session, pk)

    def create(self, session: Session, obj_in: CreateSchema) -> ModelType:
        return self.dao.create(session, obj_in)

    def delete(self, session: Session, pk: int):
        return self.dao.delete(session, pk)

    def total(self, session: Session) -> int:
        return self.dao.count(session)


class BookmarkService(BaseService[Bookmark, CreateSchema]):
    dao = BookmarkDAO()
