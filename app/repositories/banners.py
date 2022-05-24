from datetime import datetime

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app import models


def add_new_banner(db: Session, title, category_id, image):
    db_banner = models.Banner(
        title=title,
        category_id=category_id,
        image=image,
        is_active=True,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(db_banner)
    db.commit()
    db.refresh(db_banner)
    return db_banner


def get_list_banner(db: Session):
    return db.query(models.Banner).order_by(desc(models.Banner.updated_at)).all()


def get_banner_by_id(db: Session, banner_id: int):
    return db.query(models.Banner).filter(models.Banner.id == banner_id).first()


def remove_banner(db: Session, banner_id: int):
    db_banner = db.query(models.Banner).filter(
        models.Banner.id == banner_id).delete()
    db.commit()
    return db_banner


def update_banner(db: Session, banner_id, data):
    db_banner = db.query(models.Banner).filter(
        models.Banner.id == banner_id).first()
    if db_banner:
        for key, value in data.items():
            if value != None:
                setattr(db_banner, key, value)
        db_banner.updated_at = datetime.now()
        db.commit()
        db.refresh(db_banner)
        return db_banner
    else:
        return None


def user_get_banner(db: Session):
    db_banner = db.query(models.Banner).filter(
        models.Banner.is_active == True).order_by(desc(models.Banner.updated_at)).all()
    return db_banner
