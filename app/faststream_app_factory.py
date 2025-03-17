from contextlib import asynccontextmanager

from litestar import Litestar
from faststream import FastStream
from app import FastStreamBroker

from app.config import config
from app.items.service import item_command_subscriber

MESSAGE_BROKER_URL = config.MESSAGE_BROKER_URL


def create_faststream_app() -> FastStream:
    broker = FastStreamBroker(
        MESSAGE_BROKER_URL,
    )
    broker.include_router(item_command_subscriber.router)
    faststream_app = FastStream(broker)
    return faststream_app


@asynccontextmanager
async def lifespan_broker(app: Litestar):
    broker = app.state.broker
    await broker.start()
    try:
        yield
    finally:
        await broker.close()
