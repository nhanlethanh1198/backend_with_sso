from sqlalchemy.orm import Session
from app import models
from datetime import datetime

def get_services(db: Session):
    return db.query(models.Service).all()


