import os
from typing import Optional

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="staffs/token")


class CurrentStaff(BaseModel):
    staff_id: int
    role: str
    phone: str
    email: Optional[str] = None
    fullname: Optional[str] = None
    address: Optional[str] = None


def decode_token(token):
    HASH_KEY = os.getenv('HASH_KEY')
    payload = jwt.decode(token, HASH_KEY, algorithms=["HS256"])
    return CurrentStaff(staff_id=payload['staff_id'], role=payload['role'], phone=payload['phone'],
                        email=payload['email'], fullname=payload['fullname'], address=payload['address'])


async def get_current_staff(token: str = Depends(oauth2_scheme)):
    user = decode_token(token)
    return user
