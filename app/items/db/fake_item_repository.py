from app.items.domain import AbstractItemRepository
from app.items.domain import Item
from typing import Optional


class FakeItemRepository(AbstractItemRepository):
    def __init__(self):
        self.items = {}  # In-memory storage for items
        self.next_id = 1  # To simulate auto-incrementing IDs

    def create(self, obj: Item) -> Item:
        obj.id = self.next_id
        self.items[self.next_id] = obj
        self.next_id += 1
        return obj

    def get(self, obj_id: int) -> Optional[Item]:
        return self.items.get(obj_id)

    def update(self, obj: Item) -> Optional[Item]:
        if obj.id in self.items:
            self.items[obj.id] = obj
            return obj
        return None

    def delete(self, obj_id: int) -> bool:
        if obj_id in self.items:
            del self.items[obj_id]
            return True
        return False

    def get_all(self) -> list[Item]:
        return list(self.items.values())
