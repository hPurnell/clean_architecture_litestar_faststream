import datetime

from litestar import Controller, post, Response
from litestar.exceptions import HTTPException
from dishka.integrations.litestar import inject, FromDishka

from app.auth.controllers import AuthRequest, AuthResponse
from app.auth.domain import AbstractUserRepository, User, encode_jwt_token


class AuthController(Controller):
    tags = ["Auth"]
    exclude_from_auth = True

    @post(path="/auth/login", exclude_from_auth=True)
    @inject
    async def login(
        self, data: AuthRequest, user_repository: FromDishka[AbstractUserRepository]
    ) -> Response:
        username = data.username
        password = data.password

        # Verify user credentials
        user: User | None = user_repository.get_user(username.lower())
        if not user:
            raise HTTPException(status_code=401, detail="Invalid username or password")

        # TODO: Verify hashed password.
        if not user.password == password:
            raise HTTPException(status_code=401, detail="Invalid username or password")

        token = encode_jwt_token(username)

        return Response(
            content=AuthResponse(access_token=token).model_dump(),
            media_type="application/json",
        )
