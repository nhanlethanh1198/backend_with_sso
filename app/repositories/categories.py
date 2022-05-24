from datetime import datetime
from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app import models


def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Category).order_by(desc(models.Category.created_at)).offset(skip).limit(limit).all()


def get_products_code_by_category_in_store(db: Session, category_id: int, store_id: int):
    list_code = jsonable_encoder(db.query(models.Product.code).filter(models.Product.category_id == category_id,
                                                                      models.Product.belong_to_store == store_id).all())

    list_code_product = list(map(lambda x: x.get('code'), list_code))
    return list_code_product


def get_active_categories(db: Session, skip: Optional[int] = 0, limit: Optional[int] = 100):
    return db.query(models.Category).filter_by(is_active=True).order_by(desc(models.Category.created_at)).offset(
        skip).limit(limit).all()


def get_stores_with_category_id(db: Session, category_id: int):
    list_product_in_category = jsonable_encoder(
        db.query(models.Product.belong_to_store).filter_by(category_id=category_id).all())

    list_store_id = list(map(lambda x: x.get('belong_to_store'), list_product_in_category))
    # remove none value
    list_store_id = list(filter(lambda x: x is not None, list_store_id))
    # remove duplicate store ids
    list_store_id = list(set(list_store_id))

    return list_store_id


def add_category(db: Session, name: str, slug: str, image: str, parent_id: int, has_child: bool, is_active: bool):
    db_category = models.Category(
        name=name,
        slug=slug,
        image=image,
        parent_id=parent_id,
        has_child=has_child,
        is_active=is_active,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_category_by_id(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id).first()


def get_children_category_by_id(db: Session, category_id: int, is_active: bool):
    return db.query(models.Category).filter(models.Category.parent_id == category_id,
                                            models.Category.is_active == is_active).all()


def update_category(db: Session, category_id: int, name: Optional[str] = None, slug: Optional[str] = None,
                    image: Optional[str] = None, parent_id: Optional[int] = None, has_child: Optional[bool] = None,
                    is_active: Optional[bool] = None):
    current_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if current_category is not None:
        if name is not None:
            current_category.name = name

        if slug is not None:
            current_category.slug = slug

        if image is not None:
            current_category.image = image

        if parent_id is not None:
            current_category.parent_id = parent_id

        if has_child is not None:
            current_category.has_child = has_child

        if is_active is not None:
            current_category.is_active = is_active

        current_category.updated_at = datetime.now()
        db.commit()
        db.refresh(current_category)
    return current_category
