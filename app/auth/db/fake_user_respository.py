from app.auth.domain import User
from app.auth.domain import AbstractUserRepository


class FakeUserRepository(AbstractUserRepository):
    def __init__(self):
        self.collection = {
            "john.doe@example.com": User(id="1", name="John Doe", username="john.doe@example.com", password="password")
        }
        return
    
    def get_user(self, username: str) -> User | None:
        return self.collection.get(username) 