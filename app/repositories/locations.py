from datetime import datetime

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import models


def add_location(db: Session, data: dict):
    db_location = models.Location(**data)
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location


def update_location(db: Session, user_id, is_active):
    return db.query(models.Location).filter(models.Location.user_id == user_id).update({
        "is_active": is_active
    })


def get_current_location(db: Session, user_id):
    return db.query(models.Location).filter(models.Location.user_id == user_id,
                                            models.Location.is_active == True).first()


def get_list_location(db: Session, user_id):
    return db.query(models.Location).filter(models.Location.user_id == user_id).all()


def get_location_by_id(db: Session, user_id: int, location_id: int):
    return db.query(models.Location).filter_by(id=location_id, user_id=user_id).first()


def upd_location(db: Session, user_id, location_id, data):
    db_location = db.query(models.Location).filter(models.Location.user_id == user_id,
                                                   models.Location.id == location_id).first()
    if data:
        for key, value in data.items():
            if value != '':
                setattr(db_location, key, value)
        db_location.updated_at = datetime.now()
        db.commit()
        db.refresh(db_location)
        return db_location

    return None


def get_provinces(db: Session):
    return db.query(models.LocationProvince).all()


def get_districts_in_province(db: Session, province_code: int):
    province = jsonable_encoder(
        db.query(models.LocationProvince).filter(models.LocationProvince.code == province_code).first())
    if province is None:
        return 'Cannot find province'
    district = jsonable_encoder(db.query(models.LocationDistrict).outerjoin(models.LocationProvince).filter(
        models.LocationDistrict.province_code == province_code).order_by(models.LocationDistrict.fullname.asc()).all())
    return {
        **province,
        'districts': district
    }
