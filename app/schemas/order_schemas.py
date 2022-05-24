from datetime import datetime
from typing import List, Optional

from fastapi import File, Form, UploadFile
from pydantic import BaseModel, Json


# 9.order
class UserGetListOrder(BaseModel):
    status: Optional[List[int]]
    limit: Optional[int] = 20
    page: Optional[int] = 1


class OrderBase(BaseModel):
    fullname: str
    phone: str
    address_delivery: str
    count_product: int
    order_type: Optional[str] = None
    shipper: Optional[str] = None
    start_delivery: Optional[datetime] = None
    end_delivery: Optional[datetime] = None
    voucher: Optional[str] = None
    total_money: float
    total_money_sale: float
    product_money: float
    ship_fee: float
    user_id: int
    note: Optional[str] = None
    method_payment: str


class Order(OrderBase):
    id: int
    status: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ProductOrder(BaseModel):
    code: str
    product_name: str
    product_image: str
    original_price: float
    sale_price: float
    weight: str
    unit: str
    count_product: int


class OrderItems(BaseModel):
    is_combo: bool
    code: str
    quantity: int

    class Config:
        orm_mode = True


class CreateOrder(BaseModel):
    location_id: int
    start_delivery: Optional[datetime] = None
    end_delivery: Optional[datetime] = None
    voucher: Optional[str] = None
    items: List[OrderItems]
    note: Optional[str] = None
    method_payment: str
    use_point: Optional[bool] = False


class UpdateOrder(BaseModel):
    fullname: Optional[str] = None
    phone: Optional[str] = None
    address_delivery: Optional[str] = None
    products: List
