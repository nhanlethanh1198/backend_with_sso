from datetime import datetime
from typing import List, Optional

from fastapi import File, Form, UploadFile
from pydantic import BaseModel, Json


class UserBase(BaseModel):
    email: Optional[str] = None
    dob: Optional[datetime] = None
    fullname: Optional[str] = None
    phone: str
    address: Optional[str] = None
    medal_link: Optional[str] = None


class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class RegisterNewUser(BaseModel):
    phone: str
    password: str


class ForgotPassword(BaseModel):
    phone: str
    password: str


class CheckUserExist(BaseModel):
    phone: str


class LoginUser(BaseModel):
    phone: str
    id_token: str


class UserLoginWithPhoneNumberAndPassword(BaseModel):
    phone: str
    password: str


class UpdateUser(BaseModel):
    fullname: str
    address: str
    dob: Optional[datetime] = None
    email: Optional[str] = None


class UserAvatar(BaseModel):
    avatar: UploadFile

    @classmethod
    def as_form(cls,
                avatar: UploadFile = File(...)
                ) -> "UserAvatar":
        return cls(avatar=avatar)


class LoginUserResponse(BaseModel):
    detail: str
    access_token: str
    token_type: str
    is_update_user_info: bool


class UserAcceptStaff(BaseModel):
    task_id: str
    staff_id: int


class UserInfoResponse(BaseModel):
    detail: str
    data: User


class ListUserResponse(BaseModel):
    detail: str
    data: List[User]


class LockUser(BaseModel):
    is_active: bool


class UserCancelWithReason(BaseModel):
    reason: Optional[str] = None


class UserDeviceInfo(BaseModel):
    device_info: str
    FCM_token: str


class UserCheckDeviceExistResponse(BaseModel):
    detail: str
    has_device_token: bool
    FCM_token: Optional[str] = None


class UserFavorite(BaseModel):
    is_add: bool
    item_id: int
