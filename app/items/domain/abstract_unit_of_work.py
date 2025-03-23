from abc import ABC, abstractmethod
from app.items.domain import AbstractItemRepository


class AbstractUnitOfWork(ABC):
    @abstractmethod
    def __enter__(self): ...

    @abstractmethod
    def __exit__(self, *args) -> None: ...

    @abstractmethod
    def commit(self) -> None: ...

    @abstractmethod
    def rollback(self) -> None: ...

    @property
    @abstractmethod
    def items(self) -> AbstractItemRepository: ...
