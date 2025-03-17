from abc import ABC, abstractmethod


class AbstractItemCommandPublisher(ABC):
    @abstractmethod
    async def create_item(self, item): ...

    @abstractmethod
    async def update_item(self, item): ...

    @abstractmethod
    async def delete_item(self, item_id): ...