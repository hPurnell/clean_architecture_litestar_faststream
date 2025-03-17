from sqlalchemy import create_engine

from app.config import config
from app.items.db import item_repository

engine = create_engine(config.DATABASE_URL)

item_repository.Base.metadata.drop_all(engine)


item_repository.Base.metadata.create_all(engine)