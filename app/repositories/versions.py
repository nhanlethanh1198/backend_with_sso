from sqlalchemy.orm import Session
from app import models
from datetime import datetime


def get_version(db: Session):
    return db.query(models.Version).first()


def update_version(db: Session, version_id: int, android: str, ios: str):
    current_version = db.query(models.Version).filter(
        models.Version.id == version_id).first()
    print(current_version.android)
    if current_version is not None:
        current_version.android = android
        current_version.ios = ios
        current_version.updated_at = datetime.now()
        db.commit()
        db.refresh(current_version)
    return current_version
