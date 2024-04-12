from typing import Optional, TypeVar

from pydantic import BaseModel

from app.db.models import BaseModel as DBModel

ModelType = TypeVar("ModelType", bound=DBModel)
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)


class InDBMixin(BaseModel):
    id: int

    class Config:
        from_attribute = True


class BaseBookmark(BaseModel):
    url: str
    title: Optional[str] = None


class BookmarkSchema(BaseBookmark, InDBMixin):
    pass


class CreateBookmarkSchema(BaseBookmark):
    pass
