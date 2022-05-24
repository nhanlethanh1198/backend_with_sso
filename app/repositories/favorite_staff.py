from sqlalchemy.orm import Session
from app import models
from datetime import datetime
from typing import Optional, List


def get_favorite_staff_by_user_id(db: Session, user_id: int):
    return db.query(models.FavoriteStaffOfUser).filter(models.FavoriteStaffOfUser.user_id == user_id).all()


