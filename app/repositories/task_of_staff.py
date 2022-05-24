from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi.encoders import jsonable_encoder
from app import models
from datetime import datetime, timedelta
from typing import List, Optional


def create_task_of_staff(db: Session, data: dict):
    task_db = models.TaskOfStaff(**data)
    db.add(task_db)
    db.commit()
    db.refresh(task_db)
    return task_db

