import math
from typing import Optional

from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException
from fastapi.encoders import jsonable_encoder
from slugify import slugify
from sqlalchemy.orm import Session

from app.schemas import category_schemas


from app import redis_drivers
from app import response_models
from app.database import get_db
from app.get_current_staff import get_current_staff, CurrentStaff
from app.repositories import categories
from app.upload_file_to_s3 import S3
from docs import categories as docs_categories

router = APIRouter(
    prefix="/categories",
    tags=["categories"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", description=docs_categories.readCategoriesDescription)
async def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    results = categories.get_categories(db, skip, limit)
    return {
        "detail": "success",
        "data": category_tree(results)
    }


def category_tree(data):
    croot = []
    for each_category in data:
        if each_category.parent_id == 0 and each_category.has_child == True and each_category.is_active == True:
            arr_child = []
            for item in data:
                if item.parent_id == each_category.id:
                    arr_child.append(item)
            each_category.child = arr_child
            croot.append(each_category)

        elif each_category.parent_id == 0 and each_category.has_child == False and each_category.is_active == True:
            each_category.child = None
            croot.append(each_category)

    return croot


@router.get('/{category_id}/with-store', summary='Get Stores of Category', description="Get List Stores has Category",
            response_model=response_models.ListStoreResponse)
async def get_stores_with_category(category_id: int, limit: Optional[int] = 20, page: Optional[int] = 1,
                                   db: Session = Depends(get_db)):
    list_store_id = categories.get_stores_with_category_id(db=db, category_id=category_id)

    total_page = math.ceil(len(list_store_id) / limit)
    skip = (page - 1) * limit

    list_store = []

    prev_page = page - 1
    if prev_page <= 0:
        prev_page = None

    next_page = page + 1
    if next_page > total_page:
        next_page = None

    # Syntax: for item in list[star:stop:step]
    for store_id in list_store_id[skip: skip + limit:1]:
        store_info = await redis_drivers.get_store_info(store_id)
        if store_info:
            list_store.append(store_info)

    return {
        "detail": "success",
        "prev_page": prev_page,
        "next_page": next_page,
        "total_page": total_page,
        "current_page": page,
        "limit": limit,
        "total_stores": len(list_store_id),
        "data": list_store,
    }


@router.get('/{category_id}/with-store/{store_id}/products', summary='Get Products by category with store_id')
async def get_products_by_category_in_store(category_id: int, store_id: int, limit: Optional[int] = 20,
                                            page: Optional[int] = 1, db: Session = Depends(get_db)):
    list_products_code = categories.get_products_code_by_category_in_store(db=db, category_id=category_id,
                                                                           store_id=store_id)

    products_list = []
    for code in list_products_code:
        product_info = await redis_drivers.get_product_detail(code)
        if product_info:
            product_info = {**product_info,
                            **await redis_drivers.get_product_price(code),
                            }
            products_list.append(product_info)

    return {
        "detail": "success",
        "data": products_list
    }


@router.post("/add-category", description=docs_categories.addCategoryDescription)
async def add_category(img: UploadFile = File(...), name: str = Form(...), parent_id: int = Form(...),
                       db: Session = Depends(get_db), current_staff: CurrentStaff = Depends(get_current_staff)):
    current_role = current_staff.role
    roles = ['admin', 'owner']
    if current_role not in roles:
        raise HTTPException(status_code=403, detail="not authorization")
    s3 = S3()
    path_file = 'category/{}'.format(img.filename)
    url_img = s3.upload_file_to_s3(img, path_file)

    if parent_id != 0:
        parent_category = categories.update_category(
            db=db, category_id=parent_id, name=None, slug=None, image=None, parent_id=None, has_child=True,
            is_active=None)

    slug = slugify(name)
    new_category = categories.add_category(
        db=db, name=name, slug=slug, image=url_img, parent_id=parent_id, has_child=False, is_active=True)

    if not new_category:
        raise HTTPException(status_code=400, detail="Lỗi không thể tạo danh mục mới")

    # Add this categories to redis
    await redis_drivers.set_category_info(category_id=new_category.id, data=jsonable_encoder(new_category))

    return {
        "detail": "success",
        "data": new_category
    }


@router.put("/update-category/{category_id}", description=docs_categories.updateCategoryDescription)
async def update_category(category_id: int, img: Optional[UploadFile] = File(None), name: str = Form(...),
                          parent_id: int = Form(...), db: Session = Depends(get_db),
                          current_staff: CurrentStaff = Depends(get_current_staff)):
    current_role = current_staff.role
    roles = ['admin', 'owner']
    if current_role not in roles:
        raise HTTPException(status_code=403, detail="not authorization")

    current_category = categories.get_category_by_id(
        db=db, category_id=category_id)
    if current_category == None:
        raise HTTPException(status_code=404, detail="find not found")

    if name != None:
        slug = slugify(name)
    else:
        slug = None

    if img != None:
        s3 = S3()
        path_file = 'category/{}'.format(img.filename)
        url_img = s3.upload_file_to_s3(img, path_file)
    else:
        url_img = None

    category = categories.update_category(db=db, category_id=category_id, name=name,
                                          slug=slug, image=url_img, parent_id=parent_id, has_child=None, is_active=None)

    if not category:
        raise HTTPException(status_code=400, detail="Lỗi không thể cập nhật danh mục!")

    # Update this category to redis
    await redis_drivers.set_category_info(category_id=category_id, data=jsonable_encoder(category))

    return {
        "detail": "success",
        "data": category
    }


@router.put("/lock-unlock-category/{category_id}", description=docs_categories.lockUnlockCategoryDescription)
async def lock_unlock_category(category_id: int, data: category_schemas.LockCategory, db: Session = Depends(get_db),
                               current_staff: CurrentStaff = Depends(get_current_staff)):
    current_role = current_staff.role
    roles = ['admin', 'owner']
    if current_role not in roles:
        raise HTTPException(status_code=403, detail="not authorization")

    current_category = categories.get_category_by_id(
        db=db, category_id=category_id)
    if current_category is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy danh mục sản phẩm")

    category = categories.update_category(db=db, category_id=category_id, name=None,
                                          slug=None, image=None, parent_id=None, has_child=None,
                                          is_active=data.is_active)
    # Update this category to redis
    await redis_drivers.set_category_info(category_id=category_id, data=jsonable_encoder(category))

    return {
        "detail": "success",
        "data": category
    }


@router.get("/get-list-category", description=docs_categories.getListCategoryDescription)
async def get_list_category(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                            current_staff: CurrentStaff = Depends(get_current_staff)):
    current_role = current_staff.role
    roles = ['admin', 'owner']
    if current_role not in roles:
        raise HTTPException(status_code=403, detail="not authorization")

    results = categories.get_categories(db, skip, limit)
    return {
        "detail": "success",
        "data": results
    }


@router.get("/get-category-by-id/{category_id}", description=docs_categories.getCategoryByIdDescription)
async def get_category_by_id(category_id: int, db: Session = Depends(get_db),
                             current_staff: CurrentStaff = Depends(get_current_staff)):
    current_category = categories.get_category_by_id(
        db=db, category_id=category_id)
    return {
        "detail": "success",
        "data": current_category
    }


@router.get("/user-get-category-by-id/{category_id}", description=docs_categories.userGetCategoryByIdDescription)
async def user_get_category_by_id(category_id: int, db: Session = Depends(get_db)):
    current_category = categories.get_category_by_id(
        db=db, category_id=category_id)
    return {
        "detail": "success",
        "data": current_category
    }


@router.get("/get-children-category-by-id/{category_id}", description=docs_categories.getChidlenCategoryByIdDescription)
async def get_children_category_by_id(category_id: int, db: Session = Depends(get_db)):
    children_category = categories.get_children_category_by_id(
        db=db, category_id=category_id, is_active=True)
    return {
        "detail": "success",
        "data": children_category
    }


@router.get('/sync-categories-info', summary="Sync categories info to redis")
async def sync_categories_info_to_redis(db: Session = Depends(get_db),
                                        current_staff: CurrentStaff = Depends(get_current_staff)):
    current_role = current_staff.role
    roles = ['admin', 'owner']
    if current_role not in roles:
        raise HTTPException(status_code=403, detail="not authorization")

    active_category_list = categories.get_active_categories(db=db)

    for category in active_category_list:
        await redis_drivers.set_category_info(category_id=category.id, data=jsonable_encoder(category))

    for category in active_category_list:
        await redis_drivers.set_category_with_score(category_id=category.id, score=category.id)

    return {
        "detail": "success"
    }
