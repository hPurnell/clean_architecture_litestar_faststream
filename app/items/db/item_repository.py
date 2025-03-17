import datetime

from sqlalchemy.orm import Session
from sqlalchemy import Integer, String, Float, DateTime, Column
from sqlalchemy.orm import declarative_base

from app.utils.base_repository import BaseRepository
from app.items.domain import AbstractItemRepository
from app.items.domain import Item


Base = declarative_base()


class ItemEntity(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    value_str = Column(String(255), nullable=True)
    value_int = Column(Integer, nullable=True)
    value_float = Column(Float, nullable=True)
    created_date = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    modified_date = Column(DateTime, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


class ItemRepository(BaseRepository[ItemEntity, Item], AbstractItemRepository):
    def __init__(self, session: Session):
        super().__init__(session, ItemEntity, Item)