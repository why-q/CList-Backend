from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import declarative_base


class CustomBase:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True, index=True)


BaseModel = declarative_base(cls=CustomBase)


class Bookmark(BaseModel):
    url = Column(String, unique=True, index=True)
    title = Column(String)
