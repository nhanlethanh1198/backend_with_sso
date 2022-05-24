from typing import Optional
from pydantic import BaseModel
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
import jwt
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")


class CurrentUser(BaseModel):
    user_id: int
    phone: str
    email: Optional[str] = None
    fullname: Optional[str] = None
    address: Optional[str] = None


def decode_token(token):
    HASH_KEY = os.getenv('HASH_KEY')
    payload = jwt.decode(token, HASH_KEY, algorithms=["HS256"])
    return CurrentUser(user_id=payload['user_id'], phone=payload['phone'], email=payload['email'],
                       fullname=payload['fullname'], address=payload['address'])


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = decode_token(token)
    return user
