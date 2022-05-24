import json
from typing import List, Optional

from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.sqltypes import ARRAY

from app.repositories import search

from app.database import get_db

from app import response_models, redis_search_driver

from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException

import urllib.parse

from app.get_current_staff import get_current_staff, CurrentStaff

from app.get_current_user import get_current_user, CurrentUser

import math

router = APIRouter(
    prefix="/search",
    tags=["searching"],
    responses={404: {"description": "Not found"}},
)


# Search product by name


@router.get("/hotkey-product-by-name", response_model=response_models.SearchModel)
async def search_product_by_name(db: Session = Depends(get_db)):
    # Handle get recommend keyword in redis
    appSearchHotKey = redis_search_driver.getAppSearchKey()
    # Check if no query, return keyword list
    return {
        "data": 'success',
        'app_search_hotkey': appSearchHotKey[:5]
    }
