from sqlalchemy.orm import Session
from app import models
from datetime import datetime
from typing import List, Optional

from sqlalchemy import any_

# Search Product By Name


def count_product_search(db: Session, name: str) -> int:
    return db.query(models.Product).filter(models.Product.name.ilike(f'%{name}%')).count()

