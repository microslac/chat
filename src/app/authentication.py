import jwt
from typing import Optional
from pydantic import BaseModel, Field
from fastapi import status, Header, HTTPException
from app.settings import settings


class Token(BaseModel):
    auth_id: str
    team_id: Optional[str] = Field(default="")
    user_id: Optional[str] = Field(default="")


def raise_unauthorized(exc=None):
    detail = dict(ok=False, error="unauthenticated")
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail=detail
    ) from exc


def authorization_token(authorization: str = Header("")) -> Token:
    try:
        scheme, jwt_token = authorization.split()
        if scheme.lower() != settings.jwt.scheme.lower():
            raise_unauthorized()

        payload = jwt.decode(jwt_token, options={"verify_signature": False})
        token = Token(
            auth_id=payload.pop("aid"),
            team_id=payload.pop("tid", ""),
            user_id=payload.pop("uid", ""),
        )
    except Exception as exc:
        raise_unauthorized(exc)
    else:
        return token


def internal_header(internal_key: str = Header("", alias="X-Internal")) -> bool:
    if not internal_key or internal_key != settings.ms.internal_key:
        raise_unauthorized()
    return True
