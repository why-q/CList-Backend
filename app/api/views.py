from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import CommonQueryParams, get_db
from app.api.schemas import CreateBookmarkSchema
from app.db.services import BookmarkService

router = APIRouter()
_service = BookmarkService()


@router.get("/bookmarks")
def get(
    session: Session = Depends(get_db),
    commons: CommonQueryParams = Depends(),
):
    return _service.get(session, offset=commons.offset, limit=commons.limit)


@router.get("/bookmarks/{pk}")
def get_by_id(pk: int, session: Session = Depends(get_db)):
    return _service.get_by_id(session, pk=pk)


@router.post("/bookmarks")
def create(obj_in: CreateBookmarkSchema, session: Session = Depends(get_db)):
    return _service.create(session, obj_in=obj_in)


@router.delete("/bookmarks/{pk}")
def delete(pk: int, session: Session = Depends(get_db)):
    return _service.delete(session, pk=pk)
