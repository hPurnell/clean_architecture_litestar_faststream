from app import FastStreamBroker
from app.items.domain import AbstractItemCommandPublisher


class ItemCommandPublisher(AbstractItemCommandPublisher):
    def __init__(self, broker: FastStreamBroker):
        self.broker = broker

    async def create_item(self, item):
        await self.broker.publisher("item_service_create_command").publish(item)

    async def update_item(self, item):
        await self.broker.publisher("item_service_update_command").publish(item)

    async def delete_item(self, item_id):
        await self.broker.publisher("item_service_delete_command").publish(item_id)
