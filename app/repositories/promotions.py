from datetime import datetime
from typing import Optional

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app import models


def get_promotions(db: Session):
    return db.query(models.Promotion).all()


def get_by_id(db: Session, promotion_id: int):
    return db.query(models.Promotion).get(promotion_id)


def add_new_promotion(db: Session, data: any):
    db_promotion = models.Promotion(
        **data
    )
    db.add(db_promotion)
    db.commit()
    db.refresh(db_promotion)
    return db_promotion


def update_promotion(db: Session, promotion_id: int, data: any):
    db_promotion = db.query(models.Promotion).filter(
        models.Promotion.id == promotion_id).first()

    if db_promotion is not None:
        for key, value in data.items():
            if value is not None:
                setattr(db_promotion, key, value)
        db_promotion.updated_at = datetime.now()
        db.commit()
        db.refresh(db_promotion)
    return db_promotion


def count_promotions(db: Session, promotion_type: Optional[str] = None):
    current_time = datetime.now()
    filters = (models.Promotion.is_active == True,
               models.Promotion.time_from <= current_time,
               models.Promotion.time_to >= current_time)
    if promotion_type:
        filters = (*filters, models.Promotion.promotion_type == promotion_type)

    db_promotion = db.query(models.Promotion).filter(*filters).count()

    return db_promotion


def user_get_promotion_list(db: Session, promotion_type: Optional[str] = None, limit: Optional[int] = 10,
                            offset: Optional[int] = 0):
    current_time = datetime.now()
    filters = (models.Promotion.is_active == True,
               models.Promotion.time_from <= current_time,
               models.Promotion.time_to >= current_time)
    if promotion_type:
        filters = (*filters, models.Promotion.promotion_type == promotion_type)

    db_promotion = db.query(models.Promotion).filter(*filters).order_by(desc(models.Promotion.updated_at)).offset(
        offset).limit(limit).all()

    return db_promotion
