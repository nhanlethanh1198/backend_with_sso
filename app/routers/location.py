from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import response_models
from app.database import get_db
from app.repositories import locations
from typing import Optional

router = APIRouter(
    prefix="/location",
    tags=["location"],
    responses={404: {"description": "Not found"}}
)

province_description = """
Get Province by code

default code is 79: Ho Chi Minh City

List of province code:
79: Ho Chi Minh City
48: Da Nang
74: Binh Duong 
"""


# @router.get('/province')
# async def get_provinces(db: Session = Depends(get_db)):
#     return locations.get_provinces(db)


@router.get('/province', summary="Get province by code", description=province_description)
async def get_districts_in_province(province_code: Optional[int] = None, db: Session = Depends(get_db)):
    if province_code is None:
        return locations.get_provinces(db)
    else:
        return locations.get_districts_in_province(db, province_code)
