from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException

from typing import List

from sqlalchemy.orm import Session
from sqlalchemy.sql import schema

from app.repositories import versions

from app.database import get_db

from app.get_current_staff import get_current_staff, CurrentStaff

from app.get_current_user import get_current_user, CurrentUser

from app.upload_file_to_s3 import S3

router = APIRouter(
    prefix="/versions",
    tags=["versions"],
    responses={404: {"description": "Not found"}},
)


@router.get("/get-version")
async def get_version(db: Session = Depends(get_db)):
    result = versions.get_version(db=db)
    return {
        "detail": "success",
        "data": result
    }


@router.put("/update-version/{version_id}")
async def update_version(version_id: int, android: str = Form(...), ios: str = Form(...),  db: Session = Depends(get_db), current_staff: CurrentStaff = Depends(get_current_staff)):
    result = versions.update_version(
        db=db, version_id=version_id, android=android, ios=ios)
    if result is not None:
        return {
            "detail": "success",
            "data": result
        }
    else:
        raise HTTPException(status_code=400, detail="Version is not updated")
