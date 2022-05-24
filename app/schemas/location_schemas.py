from datetime import datetime
from typing import List, Optional

from fastapi import File, Form, UploadFile
from pydantic import BaseModel, Json


# 8.location
class AddLocation(BaseModel):
    fullname: str
    phone: str
    title_location: str
    type_location: str
    address: str
    district: str
    city: str
    country: str
    is_active: bool

    class Config:
        orm_mode = True


class Location(AddLocation):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True