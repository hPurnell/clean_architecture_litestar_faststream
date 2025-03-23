from app.items.domain import Item
from app.utils.abstract_repository import AbstractRepository


class AbstractItemRepository(AbstractRepository[Item, int]):
    pass
