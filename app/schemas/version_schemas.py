from datetime import datetime
from typing import List, Optional

from fastapi import File, Form, UploadFile
from pydantic import BaseModel, Json

# version

class VersionBase(BaseModel):
    ios: str
    android: str


class Version(VersionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True