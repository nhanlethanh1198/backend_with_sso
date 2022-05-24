from datetime import datetime
from typing import List, Optional

from fastapi import File, Form, UploadFile
from pydantic import BaseModel, Json


# 3.Product

class CreateProductForm(BaseModel):
    name: str
    category_id: int
    weight: int
    unit: str
    stock: int
    price: float
    price_sale: Optional[float] = None
    belong_to_store: Optional[int] = None
    location: str
    is_show_on_homepage: Optional[bool] = None
    is_show_on_store: Optional[bool] = None
    is_show_on_combo: Optional[bool] = None
    avatar_img: UploadFile
    image_1: Optional[UploadFile] = None
    image_2: Optional[UploadFile] = None
    image_3: Optional[UploadFile] = None
    image_4: Optional[UploadFile] = None
    description: Optional[str] = None
    guide: Optional[str] = None
    preserve: Optional[str] = None
    made_by: Optional[str] = None
    made_in: Optional[str] = None
    brand: Optional[str] = None
    day_to_shipping: Optional[str] = None
    note: Optional[str] = None
    tag: Optional[str] = None

    @classmethod
    def as_form(cls,
                name: str = Form(...),
                category_id: int = Form(...),
                weight: int = Form(...),
                unit: str = Form(...),
                stock: int = Form(...),
                price: float = Form(...),
                price_sale: float = Form(None),
                belong_to_store: int = Form(None),
                location: str = Form(...),
                is_show_on_homepage: bool = Form(None),
                is_show_on_store: bool = Form(None),
                is_show_on_combo: bool = Form(None),
                avatar_img: UploadFile = File(...),
                image_1: UploadFile = File(None),
                image_2: UploadFile = File(None),
                image_3: UploadFile = File(None),
                image_4: UploadFile = File(None),
                description: str = Form(None),
                guide: str = Form(None),
                preserve: str = Form(None),
                made_by: str = Form(None),
                made_in: str = Form(None),
                brand: str = Form(None),
                day_to_shipping: str = Form(None),
                note: str = Form(None),
                tag: str = Form(None)
                ) -> "CreateProductForm":
        return cls(name=name,
                   category_id=category_id,
                   weight=weight,
                   unit=unit,
                   stock=stock,
                   price=price,
                   price_sale=price_sale,
                   belong_to_store=belong_to_store,
                   location=location,
                   is_show_on_homepage=is_show_on_homepage,
                   is_show_on_store=is_show_on_store,
                   is_show_on_combo=is_show_on_combo,
                   avatar_img=avatar_img,
                   image_1=image_1,
                   image_2=image_2,
                   image_3=image_3,
                   image_4=image_4,
                   description=description,
                   guide=guide,
                   preserve=preserve,
                   made_by=made_by,
                   made_in=made_in,
                   brand=brand,
                   day_to_shipping=day_to_shipping,
                   note=note,
                   tag=tag)


class UpdateProductForm(BaseModel):
    name: Optional[str] = None
    category_id: Optional[int] = None
    weight: Optional[int] = None
    unit: Optional[str] = None
    stock: Optional[int] = None
    price: Optional[float] = None
    price_sale: Optional[float] = None
    belong_to_store: Optional[int] = None
    location: Optional[str] = None
    is_show_on_homepage: Optional[bool] = None
    is_show_on_store: Optional[bool] = None
    is_show_on_combo: Optional[bool] = None
    avatar_img: Optional[UploadFile] = None
    image_1: Optional[UploadFile] = None
    image_2: Optional[UploadFile] = None
    image_3: Optional[UploadFile] = None
    image_4: Optional[UploadFile] = None
    description: Optional[str] = None
    guide: Optional[str] = None
    preserve: Optional[str] = None
    made_by: Optional[str] = None
    made_in: Optional[str] = None
    brand: Optional[str] = None
    day_to_shipping: Optional[str] = None
    note: Optional[str] = None
    tag: Optional[str] = None

    @classmethod
    def as_form(cls,
                name: str = Form(None),
                category_id: int = Form(None),
                weight: int = Form(None),
                unit: str = Form(None),
                stock: int = Form(None),
                price: float = Form(None),
                price_sale: float = Form(None),
                belong_to_store: int = Form(None),
                location: str = Form(None),
                is_show_on_homepage: bool = Form(None),
                is_show_on_store: bool = Form(None),
                is_show_on_combo: bool = Form(None),
                avatar_img: UploadFile = File(None),
                image_1: UploadFile = File(None),
                image_2: UploadFile = File(None),
                image_3: UploadFile = File(None),
                image_4: UploadFile = File(None),
                description: str = Form(None),
                guide: str = Form(None),
                preserve: str = Form(None),
                made_by: str = Form(None),
                made_in: str = Form(None),
                brand: str = Form(None),
                day_to_shipping: str = Form(None),
                note: str = Form(None),
                tag: str = Form(None)
                ) -> "UpdateProductForm":
        return cls(name=name,
                   category_id=category_id,
                   weight=weight,
                   unit=unit,
                   stock=stock,
                   price=price,
                   price_sale=price_sale,
                   belong_to_store=belong_to_store,
                   location=location,
                   is_show_on_homepage=is_show_on_homepage,
                   is_show_on_store=is_show_on_store,
                   is_show_on_combo=is_show_on_combo,
                   avatar_img=avatar_img,
                   image_1=image_1,
                   image_2=image_2,
                   image_3=image_3,
                   image_4=image_4,
                   description=description,
                   guide=guide,
                   preserve=preserve,
                   made_by=made_by,
                   made_in=made_in,
                   brand=brand,
                   day_to_shipping=day_to_shipping,
                   note=note,
                   tag=tag)


class ProductBase(BaseModel):
    tag: Optional[str]
    image_list: Optional[Json] = None
    day_to_shipping: Optional[str] = None
    description: Optional[str] = None
    note: Optional[str] = None
    tag: Optional[str] = None
    type_product: Optional[str] = None
    brand: Optional[str] = None
    made_in: Optional[str] = None
    made_by: Optional[str] = None
    guide: Optional[str] = None
    preserve: Optional[str] = None
    location: Optional[int] = None
    total_rate: Optional[int] = 0
    comment: Optional[Json] = None
    belong_to_store: Optional[int] = None
    extra: Optional[Json] = None


class Product(ProductBase):
    id: int
    code: str
    name: str
    slug: str
    avatar_img: str
    category_id: Json
    price: Json
    is_active: bool
    status: int
    created_at: datetime
    updated_at: datetime
    sale_count: int

    class Config:
        orm_mode = True


class AddProduct(BaseModel):
    name: str
    category_id: List
    price: List


class ProductResponse(BaseModel):
    detail: str
    data: List[Product] = []


class ProductDetailResponse(BaseModel):
    detail: str
    data: Product


class StatusProduct(BaseModel):
    status: int


class PositionProductSale(BaseModel):
    code: str
    score: int


class UpdatePositionProductSale(BaseModel):
    list_product: List[PositionProductSale]


# 3.1 Product Votting
class ProductVote(ProductBase):
    vote_count_updated_at: datetime
    vote_count: int
    vote_average_score: float
    vote_one_star_count: int
    vote_two_star_count: int
    vote_three_star_count: int
    vote_four_star_count: int
    vote_five_star_count: int

    class Config:
        orm_mode = True


class ProductUserVote(BaseModel):
    vote_score: int
    comment: Optional[str] = None
    tags: Optional[List[str]] = None


class ProductUserVoteBase(ProductUserVote):
    id: int
    user_id: int
    product_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class CheckUserIsBoughtProduct(BaseModel):
    order_id: int
    code_list: List[str]
