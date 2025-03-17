from litestar.connection import ASGIConnection
from litestar.exceptions import NotAuthorizedException
from litestar.middleware import (
    AbstractAuthenticationMiddleware,
    AuthenticationResult,
)

from app.auth.domain import decode_jwt_token, Token

API_KEY_HEADER = "Authorization"


class JWTAuthenticationMiddleware(AbstractAuthenticationMiddleware):
    async def authenticate_request(self, connection: ASGIConnection) -> AuthenticationResult:

        auth_header = connection.headers.get(API_KEY_HEADER)
        if not auth_header:
            raise NotAuthorizedException()
        
        auth_header_split = auth_header.split(" ")
        if len(auth_header_split) != 2:
            raise NotAuthorizedException()

        if auth_header_split[0] != "Bearer":
            raise NotAuthorizedException()

        bearer_token = auth_header_split[1]

        token: Token = decode_jwt_token(encoded_token=bearer_token)

        return AuthenticationResult(user=token, auth=token)