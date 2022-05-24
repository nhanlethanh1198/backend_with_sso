from datetime import datetime
from typing import List, Optional

from fastapi import File, Form, UploadFile
from pydantic import BaseModel, Json


# 4.Service


class ServiceBase(BaseModel):
    title: str
    extra_title: Optional[str]
    image: str
    tag: Optional[str]


class Service(ServiceBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class ServiceResponse(BaseModel):
    detail: str
    data: List[Service] = []
