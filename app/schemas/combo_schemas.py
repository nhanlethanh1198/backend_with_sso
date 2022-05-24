from datetime import datetime
from typing import List, Optional

from fastapi import File, Form, UploadFile
from pydantic import BaseModel, Json


# 10.Combo
class ProductCombo(BaseModel):
    code: str
    name: str
    image: str
    original_price: float
    sale_price: float
    weight: str
    unit: str
    count_product: int


class ProductComboResponse(ProductCombo):
    id: int


class ProductComboInForm(BaseModel):
    id: int
    count: int


class ComboCreate(BaseModel):
    name: str
    image: UploadFile
    detail: str
    total_money: float
    total_money_sale: float
    recommend_price: float
    products: str
    is_active: Optional[bool]
    description: Optional[str]
    note: Optional[str]
    tag: Optional[str]
    brand: Optional[str]
    guide: Optional[str]
    preserve: Optional[str]
    made_in: Optional[str]
    made_by: Optional[str]
    day_to_shipping: Optional[str]

    @classmethod
    def as_form(
            cls,
            name: str = Form(...),
            image: UploadFile = File(...),
            detail: str = Form(...),
            total_money: float = Form(...),
            total_money_sale: float = Form(...),
            recommend_price: float = Form(...),
            products: str = Form(...),
            is_active: Optional[bool] = Form(None),
            description: Optional[str] = Form(None),
            note: Optional[str] = Form(None),
            tag: Optional[str] = Form(None),
            brand: Optional[str] = Form(None),
            guide: Optional[str] = Form(None),
            preserve: Optional[str] = Form(None),
            made_in: Optional[str] = Form(None),
            made_by: Optional[str] = Form(None),
            day_to_shipping: Optional[str] = Form(None),

    ) -> "ComboCreate":
        return cls(
            name=name,
            image=image,
            detail=detail,
            total_money=total_money,
            total_money_sale=total_money_sale,
            recommend_price=recommend_price,
            is_active=is_active,
            products=products,
            description=description,
            note=note,
            tag=tag,
            brand=brand,
            guide=guide,
            preserve=preserve,
            made_in=made_in,
            made_by=made_by,
            day_to_shipping=day_to_shipping,
        )


class ComboCreateResponse(ComboCreate):
    id: int
    created_at: datetime
    updated_at: datetime


class ComboUpdate(BaseModel):
    name: Optional[str] = None
    image: Optional[UploadFile] = None
    detail: Optional[str] = None
    total_money: Optional[float] = None
    total_money_sale: Optional[float] = None
    is_active: Optional[bool] = None
    recommend_price: Optional[float] = None
    products: Optional[str] = None
    description: Optional[str]
    note: Optional[str]
    tag: Optional[str]
    brand: Optional[str]
    guide: Optional[str]
    preserve: Optional[str]
    made_in: Optional[str]
    made_by: Optional[str]
    day_to_shipping: Optional[str]

    @classmethod
    def as_form(
            cls,
            name: str = Form(None),
            image: UploadFile = File(None),
            detail: str = Form(None),
            total_money: float = Form(None),
            total_money_sale: float = Form(None),
            recommend_price: float = Form(None),
            products: str = Form(None),
            is_active: Optional[bool] = Form(None),
            description: Optional[str] = Form(None),
            note: Optional[str] = Form(None),
            tag: Optional[str] = Form(None),
            brand: Optional[str] = Form(None),
            guide: Optional[str] = Form(None),
            preserve: Optional[str] = Form(None),
            made_in: Optional[str] = Form(None),
            made_by: Optional[str] = Form(None),
            day_to_shipping: Optional[str] = Form(None),
    ) -> 'ComboUpdate':
        return cls(
            name=name,
            image=image,
            detail=detail,
            total_money=total_money,
            total_money_sale=total_money_sale,
            recommend_price=recommend_price,
            is_active=is_active,
            products=products,
            description=description,
            note=note,
            tag=tag,
            brand=brand,
            guide=guide,
            preserve=preserve,
            made_in=made_in,
            made_by=made_by,
            day_to_shipping=day_to_shipping,
        )


class ComboUpdateResponse(ComboUpdate):
    id: int
    products: Optional[List[ProductComboResponse]] = None


class ComboResponse(BaseModel):
    detail: str
    data: ComboUpdate


# 10.1 Vote
class AddVoteCombo(BaseModel):
    comment: Optional[str]
    tags: Optional[List[str]]
    vote_score: int
