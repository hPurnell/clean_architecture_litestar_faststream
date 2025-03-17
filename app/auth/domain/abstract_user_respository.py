from abc import ABC, abstractmethod

from app.auth.domain.user import User


class AbstractUserRepository(ABC):
    @abstractmethod
    def get_user(self, username: str) -> User | None: ...
