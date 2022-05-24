import enum
import math
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import response_models
from app.database import get_db
from app.get_current_staff import get_current_staff, CurrentStaff
from app.repositories import promotions
from app.upload_file_to_s3 import S3
from docs import promotions as docs_promotions

from app.schemas import promotion_schemas

router = APIRouter(
    prefix="/promotions",
    tags=["promotions"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=promotion_schemas.PromotionResponse, description=docs_promotions.getListPromotion)
async def get_promotions_list(db: Session = Depends(get_db)):
    results = promotions.get_promotions(db)
    return {
        "detail": "success",
        "data": results
    }


@router.get("/get-by-id/{promotion_id}", response_model=response_models.Promotion,
            description=docs_promotions.getPromotionById)
async def get_promotions(promotion_id: int, db: Session = Depends(get_db)):
    result = promotions.get_by_id(db, promotion_id=promotion_id)
    return {
        "detail": "success",
        "data": result
    }


@router.post("/create-promotion", description=docs_promotions.createPromotion)
async def create_promotion(request_data: promotion_schemas.CreatePromotionForm = Depends(promotion_schemas.CreatePromotionForm.as_form),
                           db: Session = Depends(get_db), current_staff: CurrentStaff = Depends(get_current_staff)):
    # image s3
    s3 = S3()
    url_img = None
    if request_data.image is not None:
        path_file = 'promotion/{}/{}'.format(request_data.code, request_data.image.filename)
        url_img = s3.upload_file_to_s3(request_data.image, path_file)

    data = {
        **request_data.dict(),
        'image': url_img,
    }

    new_promotion = promotions.add_new_promotion(db=db, data=data)

    if not new_promotion:
        raise HTTPException(status_code=400, detail="Cannot create new promotion")

    return {
        "detail": "success",
        "data": new_promotion
    }


@router.put("/update-promotion/{promotion_id}", description=docs_promotions.updatePromotionById)
async def update_promotion(promotion_id: int,
                           request_data: promotion_schemas.UpdatePromotionForm = Depends(promotion_schemas.UpdatePromotionForm.as_form),
                           db: Session = Depends(get_db),
                           current_staff: CurrentStaff = Depends(get_current_staff)):
    # image s3
    s3 = S3()
    url_img = None
    if request_data.image is not None:
        path_file = 'promotion/{}/{}'.format(request_data.code, request_data.image.filename)
        url_img = s3.upload_file_to_s3(request_data.image, path_file)

    data = {}

    if url_img:
        data['image'] = url_img

    for key, value in request_data.dict().items():
        if key != 'image' and value is not None:
            data[key] = value

    updated_promotion = promotions.update_promotion(db, promotion_id=promotion_id, data=data)

    if not updated_promotion:
        raise HTTPException(status_code=400, detail="Cannot update promotion")

    return {
        "detail": "success",
        "data": updated_promotion
    }


# user

class ChoosePromotionType(str, enum.Enum):
    system = "system"
    user = "user"
    task = "task"
    odd_shift = 'odd-shift'
    fixed_shift = 'fixed-shift'


@router.get("/user-get-promotion", response_model=promotion_schemas.PromotionResponse,
            description=docs_promotions.userGetPromotion)
async def user_get_promotion_list(promotion_type: Optional[ChoosePromotionType] = None, limit: Optional[int] = 10,
                                  page: Optional[int] = 1, db: Session = Depends(get_db)):
    count_promotions = promotions.count_promotions(db, promotion_type=promotion_type)
    total_page = math.ceil(count_promotions / limit)
    offset = (page - 1) * limit
    results = promotions.user_get_promotion_list(db, promotion_type=promotion_type, limit=limit, offset=offset)

    prev_page = None if page <= 1 else page - 1
    next_page = None if page >= total_page else page + 1

    return {
        "detail": "success",
        "prev_page": prev_page,
        "next_page": next_page,
        "total_page": total_page,
        "current_page": page,
        "limit": limit,
        "total_promotions": count_promotions,
        "data": results,
    }


@router.get('/user-get-promotion/{promotion_id}', response_model=response_models.Promotion,
            description=docs_promotions.userGetPromotionById)
async def user_get_promotion_info(promotion_id: int, db: Session = Depends(get_db)):
    result = promotions.get_by_id(
        db=db, promotion_id=promotion_id)
    return {
        "detail": "success",
        "data": result
    }
