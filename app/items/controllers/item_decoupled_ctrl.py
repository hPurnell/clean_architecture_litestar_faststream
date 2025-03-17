import logging

from litestar.controller import Controller
from litestar.handlers.http_handlers.decorators import delete, patch, post
from litestar.exceptions import HTTPException
from dishka.integrations.litestar import inject, FromDishka

from app.items.domain import Item, AbstractItemCommandPublisher
from app.items.controllers import NewItemDTO, UpdateItemDTO

logger = logging.getLogger(__name__)


class ItemsCommandsDecoupled(Controller):
    path = "/items_decoupled"
    tags = ["Items Commands Decoupled"]


    @post(path="", dto=NewItemDTO)
    @inject
    async def post_item(
        self, data: Item, item_command_publisher: FromDishka[AbstractItemCommandPublisher]
    ) -> None:
        await item_command_publisher.create_item(data)
        return

    @patch(path="", dto=UpdateItemDTO)
    @inject
    async def patch_item(
        self, data: Item, item_command_publisher: FromDishka[AbstractItemCommandPublisher]
    ) -> None:
        await item_command_publisher.update_item(data)
        return

    @delete(path="/{item_id:int}")
    @inject
    async def delete_item(
        self, item_id: int, item_command_publisher: FromDishka[AbstractItemCommandPublisher]
    ) -> None:
        await item_command_publisher.delete_item(item_id)
        return