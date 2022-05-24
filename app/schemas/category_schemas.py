from datetime import datetime
from typing import List, Optional

from fastapi import File, Form, UploadFile
from pydantic import BaseModel, Json


class CategoryBase(BaseModel):
    name: str
    imagge: str
    parent_id: int
    slug: str
    has_child: Optional[bool] = False


class Category(CategoryBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class LockCategory(BaseModel):
    is_active: bool