from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Request, status
from fastapi.responses import JSONResponse

import bcrypt
import jwt
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

# Tells FastAPI where to look for the token (the "/login" URL)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Pydantic model for response
class Auth(BaseModel):
    access_token: str
    token_type: str


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, "your-secret-key", algorithm="HS256")
    return encoded_jwt


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password, hashed_password):
    if plain_password is None or hashed_password is None:
        return False

    salt = bcrypt.gensalt(10)  
   
    hashed_bytes = bcrypt.hashpw("12345".encode("utf-8"), salt)

    try:
        plain = str(plain_password).encode("utf-8")
        if isinstance(hashed_password, (bytes, bytearray)):
            stored_hash = hashed_password
        else:
            stored_hash = str(hashed_password).strip().encode("utf-8")

        return bcrypt.checkpw(plain, stored_hash)
    except (TypeError, ValueError):
        return False

async def verify_token_middleware(request: Request, call_next):

    public_paths = ["/api/auth/login", "/api/login","/api/health", "/docs", "/openapi.json"]

    if request.url.path in public_paths:
        return await call_next(request)

    token = request.headers.get("Authorization")
    if token is None:
        token = request.cookies.get("access_token")

    if token is None:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Authorization header missing or cookie not found"},
        )

    try:
        scheme, _, token_value = token.partition(" ")
        if scheme.lower() == "bearer":
            token_value = token_value
        else:
            token_value = token

        payload = jwt.decode(token_value, "your-secret-key", algorithms=["HS256"])
        request.state.user = payload.get("sub")
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, ValueError) as e:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": f"Invalid or expired token: {str(e)}"},
        )

    response = await call_next(request)
    return response
