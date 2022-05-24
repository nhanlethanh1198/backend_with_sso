from datetime import datetime
from typing import List, Optional

from fastapi import File, Form, UploadFile
from pydantic import BaseModel, Json


class CreateSystemNotification(BaseModel):
    title: str
    message: str
    image: Optional[UploadFile] = None
    exp_at: Optional[datetime] = None
    notification_type: str
    priority: str

    @classmethod
    def as_form(cls,
                title: str = Form(...),
                message: str = Form(...),
                image: Optional[UploadFile] = File(None),
                exp_at: Optional[datetime] = Form(None),
                notification_type: str = Form(...),
                priority: str = Form(...)
                ) -> "CreateSystemNotification":
        return cls(
            title=title,
            message=message,
            image=image,
            exp_at=exp_at,
            notification_type=notification_type,
            priority=priority
        )


class UpdateSystemNotification(BaseModel):
    title: Optional[str]
    message: Optional[str]
    image: Optional[UploadFile] = None
    exp_at: Optional[datetime] = None
    notification_type: Optional[str] = None
    priority: Optional[str] = None

    @classmethod
    def as_form(cls,
                title: str = Form(None),
                message: str = Form(None),
                image: Optional[UploadFile] = File(None),
                exp_at: Optional[datetime] = Form(None),
                notification_type: str = Form(None),
                priority: str = Form(None)
                ) -> "UpdateSystemNotification":
        return cls(
            title=title,
            message=message,
            image=image,
            exp_at=exp_at,
            notification_type=notification_type,
            priority=priority
        )


class FCMtest1(BaseModel):
    title: str
    body: str
    tokens: List[str]


class FCMtest2(BaseModel):
    title: str
    body: str
    token: str