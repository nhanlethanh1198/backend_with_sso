from fastapi import APIRouter, Depends, File, UploadFile, Form
from sqlalchemy.orm import Session

from app.database import get_db
from app.get_current_staff import get_current_staff, CurrentStaff
from app.repositories import banners
from app.upload_file_to_s3 import S3

router = APIRouter(
    prefix="/banners",
    tags=["banners"],
    responses={404: {"description": "Not found"}},
)


@router.get("/get-list-banner")
async def get_list_banner(db: Session = Depends(get_db), current_staff: CurrentStaff = Depends(get_current_staff)):
    results = banners.get_list_banner(db=db)
    return {
        "detail": "success",
        "data": results
    }


@router.post("/add-new-banner")
async def add_new_banner(title: str = Form(...), category_id: int = Form(...), image: UploadFile = File(...), db: Session = Depends(get_db), current_staff: CurrentStaff = Depends(get_current_staff)):

    # upload file to s3 cloud
    s3 = S3()
    url_img = None
    if image:
        path_file = 'banners/{}'.format(image.filename)
        url_img = s3.upload_file_to_s3(image, path_file)

    results = banners.add_new_banner(
        db=db, title=title, category_id=category_id, image=url_img)
    return {
        "detail": "success",
        "data": results
    }


@router.get('/get-banner-by-id/{banner_id}')
async def get_banner_by_id(banner_id: int, db: Session = Depends(get_db), current_staff: CurrentStaff = Depends(get_current_staff)):
    results = banners.get_banner_by_id(db=db, banner_id=banner_id)
    return {
        "detail": "success",
        "data": results
    }


@router.delete("/remove-banner/{banner_id}")
async def remove_banner(banner_id: int, db: Session = Depends(get_db), current_staff: CurrentStaff = Depends(get_current_staff)):
    result = banners.remove_banner(db=db, banner_id=banner_id)
    return {
        "detail": "success",
        "data": result
    }


@router.put("/update-banner/{banner_id}")
async def update_banner(banner_id: int, title: str = Form(None), category_id: int = Form(None), is_active: bool = Form(None), image: UploadFile = File(None), db: Session = Depends(get_db), current_staff: CurrentStaff = Depends(get_current_staff)):

    # upload file to s3 cloud
    s3 = S3()
    url_img = None
    if image:
        path_file = 'banners/{}'.format(image.filename)
        url_img = s3.upload_file_to_s3(image, path_file)

    data = {
        "title": title,
        "category_id": category_id,
        "is_active": is_active,
        "image": url_img
    }

    result = banners.update_banner(db=db, banner_id=banner_id, data=data)
    return {
        "detail": "success",
        "data": result
    }


@router.get("/user-get-banner")
async def user_get_banner(db: Session = Depends(get_db)):
    results = banners.user_get_banner(db=db)
    return {
        "detail": "success",
        "data": results
    }
