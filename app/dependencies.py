from fastapi import Header, HTTPException, status
from .security import decode_token

def get_current_user(authorization: str | None = Header(default=None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    return decode_token(authorization.split(" ", 1)[1])
