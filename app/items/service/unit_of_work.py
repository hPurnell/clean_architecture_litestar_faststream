from sqlalchemy.ext.asyncio import AsyncSession

from app.items.domain import Item, AbstractItemRepository, AbstractUnitOfWork
from app.items.db.item_repository import ItemRepository
from app.config import DEFAULT_SESSION_FACTORY


class UnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY, test: bool = False):
        self.session_factory = session_factory
        self.test = test

    def __enter__(self):
        self.session: AsyncSession = self.session_factory()
        self._items_repository: AbstractItemRepository = ItemRepository(self.session)
        return self

    def __exit__(self, *args):
        self.rollback()
        self.session.close()

    def commit(self):
        if not self.test:
            self.session.commit()

    def rollback(self):
        self.session.rollback()

    @property
    def items(self) -> AbstractItemRepository:
        return self._items_repository
