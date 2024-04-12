from fastapi import Request
from sqlalchemy.orm import Session


def get_db(request: Request) -> Session:
    return request.state.db


class CommonQueryParams:
    def __init__(self, offset: int = 1, limit: int = 20):
        self.offset = offset - 1 if offset - 1 >= 0 else 0
        self.limit = limit if limit > 0 else 20
