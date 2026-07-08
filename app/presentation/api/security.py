from hmac import compare_digest
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.presentation.api.dependencies import Config

bearer_scheme = HTTPBearer()


def check_authentication(
    config: Config,
    token: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
) -> None:
    if compare_digest(config.api_key, token.credentials):
        return

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
