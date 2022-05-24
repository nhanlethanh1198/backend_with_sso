from datetime import datetime
from typing import Optional, List

from fastapi.encoders import jsonable_encoder
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app import models


def get_list_order(db: Session):
    return db.query(models.Order).order_by(models.Order.created_at).all()


def get_order_by_id(db: Session, order_id: str):
    return db.query(models.Order).filter_by(order_id=order_id).first()


def user_get_order_by_id(db: Session, order_id: str, user_id: int):
    return db.query(models.Order).filter_by(order_id=order_id, user_id=user_id).first()


def create_order(db: Session, data: dict):
    current_time = datetime.now()
    time_stamp = current_time.timestamp()

    db_order = models.Order(**data)
    db.add(db_order)
    db.commit()
    db_order.order_id = "OD{:06d}".format(db_order.id)
    db.commit()
    db.refresh(db_order)
    return db_order


def update_order(db: Session, order_id, fullname, phone, address_delivery, ship_fee, product_money, total_money,
                 total_money_sale, count_product):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order is not None:
        db_order.fullname = fullname if fullname is not None else db_order.fullname
        db_order.phone = phone if phone is not None else db_order.phone
        db_order.address_delivery = address_delivery if address_delivery is not None else db_order.address_delivery
        db_order.ship_fee = ship_fee
        db_order.product_money = product_money
        db_order.total_money = total_money
        db_order.total_money_sale = total_money_sale
        db_order.count_product = count_product
        db.commit()
        db.refresh(db_order)
    return db_order


def add_order_detail(db: Session, array_item: list):
    try:
        for item in array_item:
            order_detail = models.OrderDetail(**item)
            db.add(order_detail)
        db.commit()
        return True
    except Exception as e:
        return False


def cancel_order(db: Session, order_id: str):
    db_order = db.query(models.Order).filter_by(order_id=order_id).first()
    if db_order is not None:
        db_order.status = 4  # status = 4 is cancel order
        db_order.updated_at = datetime.now()
        db.commit()
        db.refresh(db_order)
    return db_order


def get_detail_order(db: Session, order_id: int):
    return db.query(models.OrderDetail).filter(models.OrderDetail.order_id == order_id).all()


def delete_order_detail(db: Session, order_id: str):
    return db.query(models.OrderDetail).filter(models.OrderDetail.order_id == order_id).delete()


def count_order_by_user_id(db: Session, user_id: int, status: Optional[List[int]] = None):
    if status is None:
        filters = (models.Order.user_id == user_id)
    else:
        filters = (models.Order.user_id == user_id, models.Order.status.in_(status))
    return db.query(models.Order).filter(*filters).count()


def get_order_by_user_id(db: Session, user_id: int, limit: int = 10, skip: int = 0, status: Optional[List[int]] = None):
    if status is None:
        filters = (models.Order.user_id == user_id)
    else:
        filters = (models.Order.user_id == user_id, models.Order.status.in_(status))
    db_orders = jsonable_encoder(
        db.query(models.Order).filter(*filters).order_by(models.Order.created_at).offset(skip).limit(limit).all())

    for order in db_orders:
        order['order_details'] = get_detail_order(db, order.get('id'))

    return db_orders


def count_order_history_by_user_id(db: Session, user_id: int, status: Optional[int] = None):
    if status is None:
        return db.query(models.Order).filter(models.Order.user_id == user_id,
                                             models.Order.status.in_([5, 6, 7])).count()
    else:
        return db.query(models.Order).filter(models.Order.user_id == user_id, models.Order.status == status).count()


def get_order_history_by_user_id(db: Session, user_id: int, limit: int = 10, skip: int = 0,
                                 status: Optional[int] = None):
    if status is None:
        db_orders = jsonable_encoder(db.query(models.Order).filter(models.Order.user_id == user_id,
                                                                   models.Order.status.in_([5, 6, 7])).order_by(
            desc(models.Order.created_at)).offset(skip).limit(limit).all())
    else:
        db_orders = jsonable_encoder(db.query(models.Order).filter(models.Order.user_id == user_id,
                                                                   models.Order.status == status).order_by(
            desc(models.Order.created_at)).offset(skip).limit(limit).all())

    for order in db_orders:
        order['order_details'] = get_detail_order(db, order.get('id'))

    return db_orders
