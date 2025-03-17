from app.items.domain import Item
from app.utils.abstract_repository import AbstractAsyncRepository


class AbstractItemRepository(AbstractAsyncRepository[Item, int]):
    pass