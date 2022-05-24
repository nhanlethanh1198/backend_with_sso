from sqlalchemy import desc
from sqlalchemy.orm import Session

from app import models

from datetime import datetime

from app.fmodels.notification import Notification as NotificationModel


def user_get_list_notification(db: Session, user_id: int, limit: int = 20, skip: int = 0):
    return db.query(NotificationModel).filter(NotificationModel.user_id == user_id).order_by(
        desc(NotificationModel.created_at)).offset(skip).limit(limit).all()


def user_count_notification(db: Session, user_id: int):
    return db.query(NotificationModel).filter(NotificationModel.user_id == user_id).count()


def create_notification(db: Session, data: dict):
    new_notification = NotificationModel(**data)
    db.add(new_notification)
    db.commit()
    db.refresh(new_notification)
    return new_notification


def user_update_notification(db: Session, noti_id: int, user_id: int, is_read: bool):
    current_noti = db.query(NotificationModel).filter(NotificationModel.id == noti_id, NotificationModel.user_id == user_id).first()
    if current_noti is not None:
        current_noti.is_read = is_read
        current_noti.updated_at = datetime.now()
        db.commit()
        db.refresh(current_noti)
        return current_noti
    else:
        return None


def count_system_notification(db: Session):
    return db.query(models.SystemNotification).count()


def get_list_system_notification(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.SystemNotification).order_by(desc(models.SystemNotification.created_at)).offset(skip).limit(
        limit).all()


def create_system_notification(db: Session, notification: dict):
    new_notification = models.SystemNotification(**notification)
    db.add(new_notification)
    db.commit()
    db.refresh(new_notification)
    return new_notification


def get_system_notification_by_id(db: Session, notification_id: int):
    return db.query(models.SystemNotification).get({"id": notification_id})


def get_fcm_token_by_user_id(db: Session, user_id: int):
    return db.query(models.SystemNotification).filter(models.SystemNotification.user_id == user_id).first()
