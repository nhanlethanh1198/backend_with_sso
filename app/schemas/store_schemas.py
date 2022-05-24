from datetime import datetime
from typing import List, Optional

from fastapi import File, Form, UploadFile
from pydantic import BaseModel, Json


class StoreItem(BaseModel):
    id: int
    name: str


class StoreBase(BaseModel):
    name: str
    phone: str
    email: Optional[str] = None
    avatar: Optional[UploadFile] = None
    description: Optional[str] = None
    address: str
    district_code: str
    province_code: str

    @classmethod
    def as_form(
            cls,
            name: str = Form(...),
            phone: str = Form(...),
            email: Optional[str] = Form(None),
            avatar: Optional[UploadFile] = File(None),
            description: Optional[str] = Form(None),
            address: str = Form(...),
            district_code: str = Form(...),
            province_code: str = Form(...)
    ) -> "StoreBase":
        return cls(
            name=name,
            phone=phone,
            email=email,
            avatar=avatar,
            déscription=description,
            address=address,
            district_code=district_code,
            province_code=province_code
        )


class Store(StoreBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class LockStore(BaseModel):
    is_active: bool


class UpdateStore(BaseModel):
    name: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    avatar: Optional[UploadFile]
    description: Optional[str]
    address: Optional[str]
    district_code: Optional[str]
    province_code: Optional[str]

    @classmethod
    def as_form(
            cls,
            name: str = Form(None),
            phone: str = Form(None),
            email: str = Form(None),
            avatar: Optional[UploadFile] = File(None),
            description: Optional[str] = Form(None),
            address: str = Form(None),
            district_code: str = Form(None),
            province_code: str = Form(None)
    ) -> "UpdateStore":
        return cls(
            name=name,
            address=address,
            phone=phone,
            email=email,
            avatar=avatar,
            description=description,
            district_code=district_code,
            province_code=province_code
        )
