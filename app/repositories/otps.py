from sqlalchemy.orm import Session
from app import models
from datetime import datetime


def update_or_create_otp(db: Session, user_id: int, otp_type: str, otp: str, otp_expires: datetime):
    current_otp = db.query(models.Otp).filter(models.Otp.user_id == user_id, models.Otp.otp_type == otp_type).first()
    if current_otp == None:
        db_otp = models.Otp(
            user_id = user_id, 
            otp_type = otp_type, 
            otp = otp, 
            otp_expires = otp_expires,
            created_at = datetime.now(), 
            updated_at = datetime.now()
        )
        db.add(db_otp)
        db.commit()
        db.refresh(db_otp)
        return db_otp
    else:
        current_otp.otp = otp
        current_otp.otp_expires = otp_expires
        current_otp.updated_at = datetime.now()
        db.commit()
        db.refresh(current_otp)
        return current_otp