"""Secret dependency.
"""
import os
import uuid
import warnings

from fastapi import Security
from fastapi.security import APIKeyHeader
from starlette.exceptions import HTTPException
from starlette.status import HTTP_403_FORBIDDEN


class GhostLoadedSecret:
    """Ghost-loaded secret handler"""

    def __init__(self) -> None:
        self._secret = None

    @property
    def value(self):
        if self._secret:
            return self._secret

        else:
            self._secret = self.get_secret_value()
            return self.value

    def get_secret_value(self):
        """
        The get_secret_value function is a helper function that returns the secret value for the session.
        If no secret value has been set, it will generate a single-use secret key for this session.
        
        Args:
            self: Access the class attributes and methods
        
        Returns:
            A string
        """
        try:
            secret_value = os.environ["FASTAPI_AUTH_SECRET"]

        except KeyError:
            secret_value = str(uuid.uuid4())

            warnings.warn(
                f"ENVIRONMENT VARIABLE 'FASTAPI_AUTH_SECRET' NOT FOUND\n"
                f"\tGenerated a single-use secret key for this session:\n"
                f"\t{secret_value=}"
            )

        return secret_value


secret = GhostLoadedSecret()

SECRET_KEY_NAME = "secret-key"

secret_header = APIKeyHeader(
    name=SECRET_KEY_NAME, scheme_name="Secret header", auto_error=False
)


async def secret_based_security(header_param: str = Security(secret_header)):
    """
    Args:
        header_param: parsed header field secret_header

    Returns:
        True if the authentication was successful

    Raises:
        HTTPException if the authentication failed
    """

    # We simply return True if the given secret-key has the right value
    if header_param == secret.value:
        return True

    # Error text without header param
    if not header_param:
        error = "secret_key must be passed as a header field"

    # Error text with wrong header param
    else:
        error = (
            "Wrong secret key. If not set through environment variable \
                'FASTAPI_AUTH_SECRET', it was "
            "generated automatically at startup and appears in the server logs."
        )

    raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail=error)
