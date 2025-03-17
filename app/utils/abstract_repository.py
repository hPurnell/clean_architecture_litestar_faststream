from typing import Optional, TypeVar, Generic, List
from abc import ABC, abstractmethod

T = TypeVar('T')
ID = TypeVar('ID', bound=int)

class AbstractRepository(ABC, Generic[T, ID]):
    @abstractmethod
    def create(self, obj: T) -> T: ...

    @abstractmethod
    def get(self, obj_id: ID) -> Optional[T]: ...

    @abstractmethod
    def update(self, obj: T) -> Optional[T]: ...

    @abstractmethod
    def delete(self, obj_id: ID) -> bool: ...

    @abstractmethod
    def get_all(self) -> List[T]: ...