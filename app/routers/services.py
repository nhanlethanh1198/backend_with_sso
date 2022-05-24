from typing import List

from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.repositories import services

from app.database import get_db

from app import schemas

from docs import services as services_docs


router = APIRouter(
    prefix="/services",
    tags=["services"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=schemas.ServiceResponse, description=services_docs.serviceListDescription)
async def get_services(db: Session = Depends(get_db)):
    results = services.get_services(db)
    return {
        "detail": "success",
        "data": results
    }
