from datetime import datetime
from typing import Optional

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app import models


def get_all_stores(db: Session):
    return db.query(models.Store).order_by(desc(models.Store.updated_at)).all()


def count_store(db: Session, status: Optional[bool] = None):
    if status is not None:
        return db.query(models.Store).filter_by(is_active=status).count()
    else:
        return db.query(models.Store).count()


def get_list_store(db: Session, limit: int = 20, skip: int = 0, is_active: Optional[bool] = None):
    if is_active is not None:
        return db.query(models.Store).filter_by(is_active=is_active).order_by(models.Store.created_at).offset(
            skip).limit(limit).all()
    else:
        return db.query(models.Store).order_by(models.Store.created_at).offset(skip).limit(limit).all()


def get_list_store_active(db: Session, limit: int = 20, skip: int = 0):
    return db.query(models.Store).filter_by(is_active=True).order_by(models.Store.created_at).offset(skip).limit(
        limit).all()


def get_store_by_id(db: Session, store_id: int):
    return db.query(models.Store).filter(models.Store.id == store_id).first()


def add_new_store(db: Session, data: dict):

    # get full address
    district = db.query(models.LocationDistrict.fullname).filter(models.LocationDistrict.code == data['district_code']).first()
    province = db.query(models.LocationProvince.fullname).filter(models.LocationProvince.code == data['province_code']).first()
    full_address = '{}, {}, {}'.format(data['address'], district[0], province[0])

    db_store = models.Store(
        **data,
        full_address=full_address,
        is_active=True,
    )
    db.add(db_store)
    db.commit()
    db.refresh(db_store)
    return db_store


def update_store(db: Session, store_id: int, data: dict):
    db_store = db.query(models.Store).filter(models.Store.id == store_id).first()
    if db_store is not None:
        for key, value in data.items():
            if key not in ['province_code', 'district_code', 'address'] and value is not None:
                setattr(db_store, key, value)

        # get full address
        # check prev_address different current_address
        if data['address'] != db_store.address or data['district_code'] != db_store.district_code or data['province_code'] != db_store.province_code:
            district = db.query(models.LocationDistrict.fullname).filter(models.LocationDistrict.code == data['district_code']).first() if data['district_code'] else db_store.address
            province = db.query(models.LocationProvince.fullname).filter(models.LocationProvince.code == data['province_code']).first() if data['province_code'] else db_store.address
            full_address = '{}, {}, {}'.format(data['address'] if data['address'] else db_store.address, district[0], province[0])
            db_store.full_address = full_address

        db.commit()
        db.refresh(db_store)
    return db_store


def lock_store(db: Session, store_id: int, is_active: bool):
    db_store = db.query(models.Store).filter(models.Store.id == store_id).first()
    if db_store is not None:
        db_store.is_active = is_active
        db_store.updated_at = datetime.now()
        db.commit()
        db.refresh(db_store)
    return db_store


def user_get_list_hot_selling_store(db: Session, limit: int = 20):
    list_store = db.query(models.Store).order_by(desc(models.Store.product_sale_count)).limit(limit).all()
    return list_store


def user_count_list_store_by_category(db: Session, category_id: int):
    count = db.query(models.Store).outerjoin(models.Product).filter(models.Product.category_id == category_id).group_by(
        models.Store.id).count()
    return count


def user_get_list_store_by_category(db: Session, category_id: int, limit: int = 20, skip: int = 0):
    list_store = db.query(models.Store).outerjoin(models.Product).filter(
        models.Product.category_id == category_id).group_by(models.Store.id).offset(skip).limit(limit).all()
    return list_store


def user_get_list_store_have_promotions(db: Session, limit: int = 3, skip: int = 0):
    return db.query(models.Store).order_by(models.Store.updated_at.asc()).limit(limit).offset(skip).all()


def get_list_id_categories_from_store(db: Session, store_id: int):
    # find all categories from store
    categories_list_id = db.query(models.Product.category_id).filter(
        models.Product.belong_to_store == store_id).distinct().all()

    # convert to list
    categories_list_id = list(map(lambda x: x[0], categories_list_id))

    # remove duplicate
    categories_list_id = list(set(categories_list_id))

    return categories_list_id
