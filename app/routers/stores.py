import math
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.schemas import store_schemas
from app import response_models, redis_drivers
from app.database import get_db
from app.get_current_staff import get_current_staff, CurrentStaff
from app.get_current_user import get_current_user, CurrentUser
from app.repositories import stores, products, locations
from app.upload_file_to_s3 import S3

router = APIRouter(
    prefix="/stores",
    tags=["stores"],
    responses={404: {"description": "Not found"}},
)


@router.get("/get-list-store", response_model=response_models.ListStoreResponse, summary='Admin get list store')
async def get_list_store(limit: int = 20, page: int = 1, db: Session = Depends(get_db),
                         current_staff: CurrentStaff = Depends(get_current_staff)):
    total_store = stores.count_store(db=db)
    total_page = math.ceil(total_store / limit)
    skip = limit * (page - 1)
    results = stores.get_list_store(db=db, limit=limit, skip=skip)

    prev_page = page - 1
    if prev_page <= 0:
        prev_page = None
    next_page = page + 1
    if next_page > total_page:
        next_page = None

    return {
        "detail": "success",
        "data": results,
        "prev_page": prev_page,
        'next_page': next_page,
        'current_page': page,
        'total_page': total_page,
        'limit': limit
    }


@router.get("/get-store-by-id/{store_id}", response_model=response_models.StoreInfoResponse)
async def get_store_by_id(store_id: int, db: Session = Depends(get_db),
                          current_staff: CurrentStaff = Depends(get_current_staff)):
    result = stores.get_store_by_id(db=db, store_id=store_id)
    return {
        "detail": "success",
        "data": result
    }


@router.post("/add-new-store", response_model=response_models.StoreInfoResponse)
async def add_new_store(request: store_schemas.StoreBase = Depends(store_schemas.StoreBase.as_form), db: Session = Depends(get_db),
                        current_staff: CurrentStaff = Depends(get_current_staff)):
    url_avatar = None
    if request.avatar is not None:
        s3 = S3()
        file_part_avatar_store = '{}/{}/{}'.format(request.name, request.phone, request.avatar.filename)
        url_avatar = s3.upload_file_to_s3(request.avatar, file_part_avatar_store)

    data = {
        **request.dict(),
        "avatar": url_avatar
    }

    new_store = stores.add_new_store(db=db, data=data)

    if not new_store:
        raise HTTPException(status_code=400, detail="Lỗi khi thêm cửa hàng mới")

    # add new store to redis
    await redis_drivers.set_store_info(store_id=new_store.id, data=jsonable_encoder(new_store))

    return {
        "detail": "success",
        "data": new_store
    }


@router.put("/lock-store/{store_id}")
async def add_new_store(store_id: int, data: store_schemas.LockStore, db: Session = Depends(get_db),
                        current_staff: CurrentStaff = Depends(get_current_staff)):
    current_store = stores.lock_store(db=db, store_id=store_id, is_active=data.is_active)

    if not current_store:
        raise HTTPException(status_code=400, detail="Lỗi khi khóa/mở khoá cửa hàng")

    # update store to redis
    await redis_drivers.set_store_info(store_id=current_store.id, data=jsonable_encoder(current_store))

    return {
        "detail": "success",
        "data": current_store
    }


@router.put("/update-store/{store_id}", response_model=response_models.StoreInfoResponse)
async def update_store(store_id: int, request: store_schemas.UpdateStore = Depends(store_schemas.UpdateStore.as_form),
                       db: Session = Depends(get_db), current_staff: CurrentStaff = Depends(get_current_staff)):
    db_store = stores.get_store_by_id(db=db, store_id=store_id)

    if db_store is None:
        raise HTTPException(status_code=404, detail="Store not found")
    # Check current_store_avatar isValid
    current_store_avatar = db_store.avatar
    url_avatar = current_store_avatar  # prev_avatar
    if request.avatar is not None:  # new_avatar
        s3 = S3()
        file_part_avatar_store = '{}/{}/{}'.format(request.name, request.phone, request.avatar.filename)
        url_avatar = s3.upload_file_to_s3(request.avatar, file_part_avatar_store)

    data = {
        **request.dict(),
        "avatar": url_avatar
    }

    current_store = stores.update_store(db=db, store_id=store_id, data=data)

    # update store to redis
    await redis_drivers.set_store_info(store_id=store_id, data=jsonable_encoder(current_store))

    return {
        "detail": "success",
        "data": current_store
    }


@router.get("/get-list-store-active", response_model=response_models.ListStoreResponse)
async def get_list_store_active(limit: int = 20, page: int = 1, db: Session = Depends(get_db),
                                current_staff: CurrentStaff = Depends(get_current_staff)):
    total_store_active = stores.count_store(db=db, status=True)
    total_page = math.ceil(total_store_active / limit)
    skip = limit * (page - 1)
    results = stores.get_list_store_active(db=db, limit=limit, skip=skip)
    prev_page = page - 1
    if prev_page <= 0:
        prev_page = None
    next_page = page + 1
    if next_page > total_page:
        next_page = None

    return {
        "detail": "success",
        "data": results,
        "prev_page": prev_page,
        'next_page': next_page,
        'current_page': page,
        'total_page': total_page,
        'limit': limit
    }


@router.get('/user-get-list-store', summary='Get list store by user', response_model=response_models.ListStoreResponse)
async def user_get_list_store(limit: int = 20, page: int = 1, db: Session = Depends(get_db)):
    total_store_active = stores.count_store(db=db, status=True)
    total_page = math.ceil(total_store_active / limit)
    skip = limit * (page - 1)
    results = stores.get_list_store_active(db=db, limit=limit, skip=skip)

    prev_page = page - 1
    if prev_page <= 0:
        prev_page = None

    next_page = page + 1
    if next_page > total_page:
        next_page = None

    return {
        "detail": "success",
        "data": results,
        "prev_page": prev_page,
        'next_page': next_page,
        'current_page': page,
        'total_page': total_page,
        'limit': limit,
        'total_stores': total_store_active
    }


@router.get('/{store_id}/categories', summary='User get list Categories from store',
            response_model=response_models.CategoriesResponse)
async def user_get_list_categories(store_id: int, limit: Optional[int] = 20, page: Optional[int] = 1,
                                   db: Session = Depends(get_db)):
    list_id = stores.get_list_id_categories_from_store(db=db, store_id=store_id)

    total_page = math.ceil(len(list_id) / limit)
    skip = (page - 1) * limit

    categories = []

    prev_page = page - 1
    if prev_page <= 0:
        prev_page = None

    next_page = page + 1
    if next_page > total_page:
        next_page = None

    for item in list_id[skip: skip + limit: 1]:
        category = await redis_drivers.get_category_info(category_id=item)
        categories.append(category)

    return {
        "detail": "success",
        "prev_page": prev_page,
        "next_page": next_page,
        "total_page": total_page,
        "current_page": page,
        "limit": limit,
        "total_categories": len(list_id),
        "data": categories
    }


@router.get('/user-get-list-hot-selling-store', summary='User get list of hot selling store',
            response_model=response_models.ListStoreResponse)
async def user_get_list_hot_selling_store(limit: int = 20, db: Session = Depends(get_db)):
    results = stores.user_get_list_hot_selling_store(db=db, limit=limit)
    return {
        "detail": "success",
        "data": results
    }


@router.get('/user-get-list-store-by-category/{category_id}', summary='User get list of store by category',
            response_model=response_models.ListStoreResponse)
async def user_get_list_store_by_category(category_id: int, limit: int = 20, page: int = 1,
                                          db: Session = Depends(get_db)):
    total_store = stores.user_count_list_store_by_category(db=db, category_id=category_id)
    total_page = math.ceil(total_store / limit)
    skip = limit * (page - 1)

    prev_page = page - 1
    if prev_page <= 0:
        prev_page = None

    next_page = page + 1
    if next_page > total_page:
        next_page = None

    results = stores.user_get_list_store_by_category(db=db, category_id=category_id, limit=limit, skip=skip)
    return {
        "detail": "success",
        "data": results,
        "prev_page": prev_page,
        'next_page': next_page,
        'current_page': page,
        'total_page': total_page,
        'limit': limit
    }


@router.get('/user-get-list-store-have-promotions', summary="User get list of store have activating promotions",
            response_model=response_models.ListStoreHavePromotionResponse)
async def get_list_store_have_promotions(have_products: Optional[bool] = True, limit: int = 3, page: int = 1,
                                         db: Session = Depends(get_db)):
    count_store = stores.count_store(db=db)
    if limit > count_store:
        limit = count_store

    total_page = math.ceil(count_store / limit)

    skip = limit * (page - 1)
    prev_page = page - 1
    if prev_page <= 0:
        prev_page = None

    next_page = page + 1
    if next_page > total_page:
        next_page = None

    db_stores_id_list = jsonable_encoder(stores.user_get_list_store_have_promotions(db=db, limit=limit, skip=skip))

    if have_products:
        #    Get 10 products first of each store
        for store in db_stores_id_list:
            store_id = store['id']
            store['products'] = jsonable_encoder(
                products.get_product_list_by_store_id(db=db, store_id=store_id, limit=10))

    return {
        "detail": "success",
        "data": db_stores_id_list,
        "prev_page": prev_page,
        'next_page': next_page,
        'current_page': page,
        'total_page': total_page,
        'limit': limit
    }


# Lấy danh sách cửa hàng gần nhà khách hàng
# Mỗi cửa hàng lấy 10 sản phẩm đầu tiên
# Danh sách cửa hàng được quy định bằng limit (default = 3)
@router.get('/user-get-list-store-near-by-user', summary="User get list of store near by user")
async def get_list_store_near_by_user(limit: int = 3, db: Session = Depends(get_db),
                                      current_user: CurrentUser = Depends(get_current_user)):
    current_location_user = locations.get_current_location(db=db, user_id=current_user.user_id)
    print(current_location_user)

    return {
        "detail": "success",
        "data": current_location_user
    }


@router.get('/{store_id}/products', summary='Get Products In Store',
            response_model=response_models.ProductListInStoreResponse)
async def get_product_in_store(store_id: int, category_id: Optional[int] = None, limit: int = 20, page: int = 1,
                               db: Session = Depends(get_db)):
    product_code_list = products.get_products_code_by_store(db=db, store_id=store_id, category_id=category_id, status=1)

    total_page = math.ceil(len(product_code_list) / limit)

    skip = limit * (page - 1)
    prev_page = page - 1
    if prev_page <= 0:
        prev_page = None

    next_page = page + 1
    if next_page > total_page:
        next_page = None

    product_list = []

    for code in product_code_list[skip: skip + limit:1]:
        info = await redis_drivers.get_product_detail(code=code)
        if info:
            info = {
                **info,
                **await redis_drivers.get_product_price(code=code)
            }
            product_list.append(info)

    return {
        "detail": "success",
        "data": product_list,
        "prev_page": prev_page,
        'next_page': next_page,
        'current_page': page,
        'total_page': total_page,
        'limit': limit
    }


@router.get('/sync-stores-info', summary='Sync store info to redis')
async def sync_stores_to_redis(db: Session = Depends(get_db), current_staff: CurrentStaff = Depends(get_current_staff)):
    stores_list = stores.get_all_stores(db=db)

    for store in stores_list:
        await redis_drivers.set_store_info(store_id=store.id, data=jsonable_encoder(store))

    return {
        "detail": "success",
    }
