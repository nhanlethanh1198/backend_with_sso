from sqlalchemy.orm import Session
from app import models
from datetime import datetime
from typing import List, Optional


def create_task_schedule(db: Session, data: dict):
    task_schedule = models.TaskSchedule(**data)
    db.add(task_schedule)
    db.commit()
    db.refresh(task_schedule)
    return task_schedule


def get_list_task_schedule(db: Session, task_id: str, user_id: int):
    return db.query(models.TaskSchedule).filter(models.TaskSchedule.task_id == task_id,
                                                models.TaskSchedule.f_user_id == user_id).all()


def get_lis_task_schedule_by_task(db: Session, task_id: str):
    return db.query(models.TaskSchedule).filter(models.TaskSchedule.task_id == task_id).all()


def update_task_schedule(db: Session, task_id: str, schedule_id: int, status: int, cancel_reason: Optional[str] = None):
    current_schedule = db.query(models.TaskSchedule).filter(models.TaskSchedule.task_id == task_id,
                                                            models.TaskSchedule.id == schedule_id).first()
    if current_schedule is not None:
        current_schedule.updated_at = datetime.now()
        current_schedule.schedule_status = status
        if cancel_reason is not None:
            current_schedule.cancel_reason = cancel_reason
        db.commit()
        db.refresh(current_schedule)
        return current_schedule
    else:
        return False


def get_list_schedule(db: Session, time_from: datetime, time_to: datetime):
    return db.query(models.TaskSchedule).filter(models.TaskSchedule.time_from >= time_from,
                                                models.TaskSchedule.time_to <= time_to).all()
