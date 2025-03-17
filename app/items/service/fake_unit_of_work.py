from app.items.domain import Item, AbstractItemRepository, AbstractUnitOfWork
from app.items.db.fake_item_repository import FakeItemRepository


class FakeUnitOfWork(AbstractUnitOfWork):
    _item_repository: AbstractItemRepository = FakeItemRepository()

    def __init__(self, session_factory=None): ...

    def __enter__(self):
        return self

    def __exit__(self, *args): ...

    def commit(self): ...

    def rollback(self): ...

    @property
    def items(self) -> AbstractItemRepository:
        return self._item_repository
