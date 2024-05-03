from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .jwt_handler import decode_token


def verify_jwt(jwtoken: str):
    payload = decode_token(jwtoken)
    return payload


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        print("Credentials :", credentials)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication token"
                )

            payload = verify_jwt(credentials.credentials)
            if not payload:
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token"
                )
            return payload
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization token")