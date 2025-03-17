from datetime import datetime, timedelta
from dataclasses import dataclass, asdict

import jwt
from litestar.exceptions import NotAuthorizedException

from app.config import config

AUTH_DURATION = timedelta(hours=1)
ALGORITHM = "HS256"


@dataclass
class Token:
    exp: datetime
    iat: datetime
    sub: str


def decode_jwt_token(encoded_token: str) -> Token:
    try:
        payload = jwt.decode(jwt=encoded_token, key=config.JWT_SECRET, algorithms=[ALGORITHM])
        return Token(**payload)
    except jwt.exceptions.InvalidTokenError as e:
        raise NotAuthorizedException("Invalid token") from e


def encode_jwt_token(username: str) -> str:
    token = Token(
        exp=(datetime.now() + AUTH_DURATION).timestamp(),
        iat=datetime.now().timestamp(),
        sub=username,
    )
    return jwt.encode(asdict(token), config.JWT_SECRET, algorithm=ALGORITHM)