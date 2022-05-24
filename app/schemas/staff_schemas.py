from datetime import datetime
from typing import List, Optional

from fastapi import File, Form, UploadFile
from pydantic import BaseModel, Json


# 6.staff
class CreateStaff(BaseModel):
    fullname: str
    dob: datetime
    gender: str
    phone: str
    email: str
    id_card: str
    province_code: int
    district_code: int
    address: str
    role: str
    password: str
    avatar_img: UploadFile
    id_card_img_1: UploadFile
    id_card_img_2: UploadFile

    @classmethod
    def as_form(cls,
                fullname: str = Form(...),
                dob: datetime = Form(...),
                gender: str = Form(...),
                phone: str = Form(...),
                email: str = Form(...),
                id_card: str = Form(...),
                province_code: int = Form(...),
                district_code: int = Form(...),
                address: str = Form(...),
                role: str = Form(...),
                password: str = Form(...),
                avatar_img: UploadFile = File(...),
                id_card_img_1: UploadFile = File(...),
                id_card_img_2: UploadFile = File(...)) -> 'CreateStaff':
        return cls(
            fullname=fullname,
            dob=dob,
            gender=gender,
            phone=phone,
            email=email,
            id_card=id_card,
            province_code=province_code,
            district_code=district_code,
            address=address,
            role=role,
            password=password,
            avatar_img=avatar_img,
            id_card_img_1=id_card_img_1,
            id_card_img_2=id_card_img_2
        )


class UpdateStaff(BaseModel):
    fullname: Optional[str]
    dob: Optional[datetime]
    gender: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    id_card: Optional[str]
    province_code: Optional[int]
    district_code: Optional[int]
    address: Optional[str]
    role: Optional[str]
    password: Optional[str]
    avatar_img: Optional[UploadFile]
    id_card_img_1: Optional[UploadFile]
    id_card_img_2: Optional[UploadFile]

    @classmethod
    def as_form(cls,
                fullname: Optional[str] = Form(None),
                dob: datetime = Form(None),
                gender: str = Form(None),
                phone: Optional[str] = Form(None),
                email: Optional[str] = Form(None),
                id_card: Optional[str] = Form(None),
                province_code: Optional[int] = Form(None),
                district_code: Optional[int] = Form(None),
                address: Optional[str] = Form(None),
                role: Optional[str] = Form(None),
                password: Optional[str] = Form(None),
                avatar_img: UploadFile = File(None),
                id_card_img_1: UploadFile = File(None),
                id_card_img_2: UploadFile = File(None)) -> 'UpdateStaff':
        return cls(
            fullname=fullname,
            dob=dob,
            gender=gender,
            phone=phone,
            email=email,
            id_card=id_card,
            province_code=province_code,
            district_code=district_code,
            address=address,
            role=role,
            password=password,
            avatar_img=avatar_img,
            id_card_img_1=id_card_img_1,
            id_card_img_2=id_card_img_2
        )


class StaffBase(BaseModel):
    id: int
    fullname: str
    phone: str
    avatar_img: str
    id_card_img_1: str
    id_card_img_2: str
    join_from_date: datetime
    working_count: int
    vote_count: int
    vote_average_score: float


class StoreItem(BaseModel):
    id: int
    name: str


class Staff(StaffBase):
    id: int
    dob: datetime
    gender: str
    age: int
    role: str
    id_card: str
    status: str
    join_from_date: datetime
    is_active: bool
    province_code: Optional[int]
    district_code: Optional[int]
    address: str
    email: Optional[str] = None
    phone: str

    # item_store: Optional[StoreItem] = None

    class Config:
        orm_mode = True


class LoginStaff(BaseModel):
    phone: str
    password: str

    class Config:
        orm_mode = True


class StaffLoginResponse(BaseModel):
    detail: str
    access_token: str
    token_type: str


class StaffResponse(BaseModel):
    detail: str
    data: Staff


class ListStaffResponse(BaseModel):
    detail: str
    data: List[Staff]


class UserGetStaffResponse(BaseModel):
    detail: str
    data: StaffBase


class AddStaff(BaseModel):
    fullname: str
    dob: datetime
    id_card: str
    phone: str
    address: str
    role: str


class LockStaff(BaseModel):
    is_active: bool


# 6.1 Vote Staff
class VoteStaff(BaseModel):
    vote_score: int
    comment: Optional[str] = None
    tags: Optional[List[str]] = None

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "vote_score": 5,
                "comment": "Tôi thật sự hài lòng với tác phong chuyên nghiệp và thái độ lịch sự, thân thiện của người nhân viên này.",
                "tags": ["good_job", "good_skill", "working_clean", "friendly", "working_on_time", "working_carefully",
                         "good_attitude"]
            }
        }


class UpdateVoteStaff(BaseModel):
    vote_score: int
    comment: Optional[str] = None

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "vote_score": 5,
                "comment": "Tôi thật sự hài lòng với tác phong chuyên nghiệp và thái độ lịch sự, thân thiện của người nhân viên này.",
            }
        }


class FavoriteStaff(BaseModel):
    staff_id: int
    is_favorite: bool


class BannedStaffByUser(BaseModel):
    staff_id: int
    is_banned: bool


class ListStaffId(BaseModel):
    list_staff_id: List[int]
