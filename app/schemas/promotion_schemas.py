from datetime import datetime
from typing import List, Optional

from fastapi import File, Form, UploadFile
from pydantic import BaseModel, Json


# 5.Promotion
class CreatePromotionForm(BaseModel):
    title: str
    code: str
    time_from: str
    time_to: str
    promotion_type: str
    image: UploadFile
    detail: Optional[str]
    rule: Optional[str]

    @classmethod
    def as_form(cls,
                title: str = Form(...),
                code: str = Form(...),
                time_from: str = Form(...),
                time_to: str = Form(...),
                promotion_type: str = Form(...),
                image: UploadFile = File(...),
                detail: Optional[str] = Form(None),
                rule: Optional[str] = Form(None)) -> "CreatePromotionForm":
        return cls(title=title,
                   code=code,
                   time_from=time_from,
                   time_to=time_to,
                   promotion_type=promotion_type,
                   image=image,
                   detail=detail,
                   rule=rule)


class UpdatePromotionForm(BaseModel):
    title: Optional[str]
    code: Optional[str]
    time_from: Optional[str]
    time_to: Optional[str]
    promotion_type: Optional[str]
    image: Optional[UploadFile]
    detail: Optional[str]
    rule: Optional[str]

    @classmethod
    def as_form(cls,
                title: Optional[str] = Form(None),
                code: Optional[str] = Form(None),
                time_from: Optional[str] = Form(None),
                time_to: Optional[str] = Form(None),
                promotion_type: Optional[str] = Form(None),
                image: Optional[UploadFile] = File(None),
                detail: Optional[str] = Form(None),
                rule: Optional[str] = Form(None)) -> "UpdatePromotionForm":
        return cls(title=title,
                   code=code,
                   time_from=time_from,
                   time_to=time_to,
                   promotion_type=promotion_type,
                   image=image,
                   detail=detail,
                   rule=rule)


class PromotionBase(BaseModel):
    code: str
    image: str
    title: str
    time_to: datetime
    time_from: datetime
    promotion_type: str = 'system'
    detail: Optional[str] = None
    rule: Optional[str] = None


class Promotion(PromotionBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class PromotionResponse(BaseModel):
    detail: str
    prev_page: Optional[int]
    next_page: Optional[int]
    total_page: Optional[int]
    current_page: Optional[int]
    limit: Optional[int]
    total_promotions: Optional[int]
    data: List[Promotion]
