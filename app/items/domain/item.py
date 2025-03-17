from datetime import datetime
from enum import Enum
from dataclasses import dataclass


@dataclass(kw_only=True)
class Item:
    id: int | None = None
    value_str: str | None = None
    value_int: int | None = None
    value_float: float | None = None
    created_date: datetime | None = None
    modified_date: datetime | None = None
