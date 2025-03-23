from datetime import datetime, timedelta

import pytest
import jwt
from litestar.exceptions import NotAuthorizedException

from app.config import config
from app.auth.domain.token import decode_jwt_token, encode_jwt_token

# Constants
ALGORITHM = "HS256"
AUTH_DURATION = timedelta(hours=1)

# Mock the secret key used in encoding and decoding
config.JWT_SECRET = "supersecretkey"


class TestJWT:
    def test_encode_jwt_token(self):
        """Test the JWT token encoding functionality."""
        username = "testuser"

        # Encode the token
        token = encode_jwt_token(username)

        # Decode the token to validate the encoding
        decoded_token = decode_jwt_token(token)

        # Ensure the decoded token contains the correct username
        assert decoded_token.sub == username

        # Ensure the token contains the necessary fields
        assert isinstance(decoded_token.exp, float)
        assert isinstance(decoded_token.iat, float)
        assert isinstance(decoded_token.sub, str)

    def test_decode_valid_jwt_token(self):
        """Test decoding a valid JWT token."""
        username = "testuser"

        # Encode a valid token
        token = encode_jwt_token(username)

        # Decode the token
        decoded_token = decode_jwt_token(token)

        # Ensure the decoded token contains the correct username
        assert decoded_token.sub == username
        assert isinstance(decoded_token.exp, float)
        assert isinstance(decoded_token.iat, float)

    def test_decode_invalid_jwt_token(self):
        """Test decoding an invalid JWT token."""
        invalid_token = "invalid.token.here"

        # Try decoding an invalid token and ensure it raises a NotAuthorizedException
        with pytest.raises(NotAuthorizedException, match="Invalid token"):
            decode_jwt_token(invalid_token)

    def test_decode_expired_jwt_token(self):
        """Test decoding an expired JWT token."""
        username = "testuser"

        # Create a token with a past expiration date
        expired_token = jwt.encode(
            {
                "exp": (datetime.now() - timedelta(days=1)).timestamp(),
                "iat": datetime.now().timestamp(),
                "sub": username,
            },
            config.JWT_SECRET,
            algorithm=ALGORITHM,
        )

        # Try decoding the expired token and ensure it raises a NotAuthorizedException
        with pytest.raises(NotAuthorizedException, match="Invalid token"):
            decode_jwt_token(expired_token)
