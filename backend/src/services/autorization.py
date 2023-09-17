import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import DecodeError, ExpiredSignatureError, InvalidSignatureError

from backend.src.auth.abc_key import AbstractKey
from backend.src.auth.rsa_key import get_pk
from backend.src.local.services import autorization as errors
from backend.src.models.jwt import JWTPayload

security = HTTPBearer(auto_error=False)


async def get_token_payload(
    authorization: HTTPAuthorizationCredentials | None = Depends(security),
    pk: AbstractKey = Depends(get_pk),
) -> None | JWTPayload:
    if authorization is not None:
        token = authorization.credentials
        try:
            payload = jwt.decode(token, pk.key, algorithms=pk.algorithms)
            return JWTPayload(
                is_superuser=payload[pk.pl_is_superuser],
                permissions=payload[pk.pl_permissions],
                user_id=payload[pk.pl_sub],
            )
        except ExpiredSignatureError:
            raise HTTPException(status_code=403, detail=errors.TOKEN_EXPIRED)
        except InvalidSignatureError:
            raise HTTPException(status_code=403, detail=errors.TOKEN_VER_FAILED)
        except DecodeError:
            raise HTTPException(status_code=403, detail=errors.TOKEN_BAD_DECODE)
        except KeyError:
            raise HTTPException(status_code=403, detail=errors.TOKEN_BAD_PAYLOAD)
    return None
