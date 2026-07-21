from hmac import compare_digest
from pathlib import Path
from secrets import token_urlsafe
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

API_TOKEN_PATH = Path("/data/api-token")
OWNER_READ_WRITE_FILE_MODE = 0o600

bearer_scheme = HTTPBearer()


def get_or_create_api_token() -> str:
    if not API_TOKEN_PATH.exists():
        API_TOKEN_PATH.parent.mkdir(parents=True, exist_ok=True)
        API_TOKEN_PATH.write_text(token_urlsafe(32))
        API_TOKEN_PATH.chmod(OWNER_READ_WRITE_FILE_MODE)

    return API_TOKEN_PATH.read_text()


def check_authentication(
    request: Request,
    token: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
) -> None:
    if compare_digest(request.app.state.api_token, token.credentials):
        return

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
