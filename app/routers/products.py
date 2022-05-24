import enum
import math
from typing import Optional

import numpy as np
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from slugify import slugify
from sqlalchemy.orm import Session

from app import redis_drivers
from app import response_models
from app.database import get_db
from app.dependencies import random_number
from app.get_current_staff import get_current_staff, CurrentStaff
from app.get_current_user import get_current_user, CurrentUser
from app.repositories import products
from app.schemas import product_schemas
from app.upload_file_to_s3 import S3
from docs import products as docs_products, product_vote as docs_product_vote

router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={404: {"description": "Not found"}},
)


@router.get("/get-list-product-by-category-id/{category_id}",
            description=docs_products.getListProductInCategoryDescription)
async def get_list_product_by_category_id(category_id: int, limit: int = 20, page: int = 1,
                                          location: Optional[int] = None,
                                          is_show_on_homepage: Optional[bool] = None,
                                          is_show_on_store: Optional[bool] = None,
                                          is_show_on_combo: Optional[bool] = None,
                                          db: Session = Depends(get_db)):
    products_code_list = products.query_products_list_code(db=db, category_id=category_id, location=location,
                                                           is_show_on_homepage=is_show_on_homepage,
                                                           is_show_on_store=is_show_on_store,
                                                           is_show_on_combo=is_show_on_combo)

    total_page = math.ceil(len(products_code_list) / limit)
    skip = limit * (page - 1)

    prev_page = page - 1
    if prev_page <= 0:
        prev_page = None

    next_page = page + 1
    if next_page > total_page:
        next_page = None

    results = []

    for code in products_code_list[skip: skip + limit]:
        product_info = await redis_drivers.get_product_detail(code)
        if product_info:
            product_info = {
                **product_info,
                "stock": await redis_drivers.get_product_stock(code),
                "price": await redis_drivers.get_product_price(code)
            }
        results.append(product_info)

    return {
        "detail": "success",
        "prev_page": prev_page,
        "current_page": page,
        "next_page": next_page,
        "total_page": total_page,
        "limit": limit,
        "total_products": len(products_code_list),
        "data": results
    }


@router.get("/get-product-by-code/{code}", description=docs_products.getProductByCode)
async def get_product_by_code(code: str):
    result = await redis_drivers.get_product_detail(code)
    if not result:
        raise HTTPException(status_code=404, detail="Product not found")

    result = {
        **result,
        "stock": await redis_drivers.get_product_stock(code),
        "price": await redis_drivers.get_product_price(code)
    }

    return {
        "detail": "success",
        "data": result
    }


@router.get('/get-list-product', description=docs_products.getLístProduct,
            response_model=response_models.ResponseListProduct)
async def get_list_product(category_id: Optional[int] = None, status: Optional[int] = None,
                           location: Optional[int] = None,
                           store_id: Optional[int] = None, limit: Optional[int] = 20,
                           is_show_on_homepage: Optional[bool] = None,
                           is_show_on_store: Optional[bool] = None,
                           is_show_on_combo: Optional[bool] = None,
                           page: Optional[int] = 1, db: Session = Depends(get_db),
                           current_staff: CurrentStaff = Depends(get_current_staff)):
    products_code_list = products.query_products_list_code(db=db, category_id=category_id, status=status,
                                                           store_id=store_id, location=location,
                                                           is_show_on_homepage=is_show_on_homepage,
                                                           is_show_on_store=is_show_on_store,
                                                           is_show_on_combo=is_show_on_combo)

    total_page = math.ceil(len(products_code_list) / limit)

    skip = limit * (page - 1)

    results = []

    for code in products_code_list[skip: skip + limit]:
        product_info = await redis_drivers.get_product_detail(code)
        if product_info:
            product_info = {
                **product_info,
                "stock": await redis_drivers.get_product_stock(code),
                "price": await redis_drivers.get_product_price(code)
            }
        results.append(product_info)

    prev_page = page - 1
    if prev_page <= 0:
        prev_page = None

    next_page = page + 1
    if next_page > total_page:
        next_page = None

    return {
        "detail": "success",
        "prev_page": prev_page,
        "current_page": page,
        "next_page": next_page,
        "total_page": total_page,
        "total_products": len(products_code_list),
        "limit": limit,
        "data": results
    }


@router.get('/user-get-product', description=docs_products.userGettLístProduct)
async def user_get_product(category_id: Optional[int] = None, status: Optional[int] = None,
                           location: Optional[int] = None,
                           is_show_on_homepage: Optional[bool] = None,
                           is_show_on_store: Optional[bool] = None,
                           is_show_on_combo: Optional[bool] = None,
                           limit: Optional[int] = 20,
                           page: Optional[int] = 1, db: Session = Depends(get_db)):
    products_code_list = products.query_products_list_code(
        db=db, category_id=category_id, status=status, location=location)

    total_page = math.ceil(len(products_code_list) / limit)
    skip = limit * (page - 1)

    results = []

    for code in products_code_list[skip: skip + limit]:
        product_info = await redis_drivers.get_product_detail(code)
        if product_info:
            product_info = {
                **product_info,
                "stock": await redis_drivers.get_product_stock(code),
                "price": await redis_drivers.get_product_price(code)
            }
        results.append(product_info)

    prev_page = page - 1
    if prev_page <= 0:
        prev_page = None

    next_page = page + 1
    if next_page > total_page:
        next_page = None

    return {
        "detail": "success",
        "prev_page": prev_page,
        "current_page": page,
        "next_page": next_page,
        "total_page": total_page,
        "limit": limit,
        "total_products": len(products_code_list),
        "data": results
    }


@router.post('/add-product', description=docs_products.addProduct)
async def add_product(form: product_schemas.CreateProductForm = Depends(product_schemas.CreateProductForm.as_form),
                      db: Session = Depends(get_db), current_staff: CurrentStaff = Depends(get_current_staff)):
    code = await random_number(6)
    slug = slugify(form.name)

    # image s3
    s3 = S3()
    n = await random_number(6)
    filename_avatar = 'a{}_{}'.format(code, n)
    path_file = 'product/{}/{}'.format(code, filename_avatar)
    url_avatar = s3.upload_file_to_s3(form.avatar_img, path_file)

    images = []
    if form.image_1 is not None:
        n1 = await random_number(6)
        file1 = 'd{}_{}'.format(code, n1)
        path1 = 'product/{}/{}'.format(code, file1)
        url1 = s3.upload_file_to_s3(form.image_1, path1)
        images.append({
            "index": 1,
            "url": url1
        })

    if form.image_2 is not None:
        n2 = await random_number(6)
        file2 = 'd{}_{}'.format(code, n2)
        path2 = 'product/{}/{}'.format(code, file2)
        url2 = s3.upload_file_to_s3(form.image_2, path2)
        images.append({
            "index": 2,
            "url": url2
        })

    if form.image_3 is not None:
        n3 = await random_number(6)
        file3 = 'd{}_{}'.format(code, n3)
        path3 = 'product/{}/{}'.format(code, file3)
        url3 = s3.upload_file_to_s3(form.image_3, path3)
        images.append({
            "index": 3,
            "url": url3
        })

    if form.image_4 is not None:
        n4 = await random_number(6)
        file4 = 'd{}_{}'.format(code, n4)
        path4 = 'product/{}/{}'.format(code, file4)
        url4 = s3.upload_file_to_s3(form.image_4, path4)
        images.append({
            "index": 4,
            "url": url4
        })

    data_product = {
        **form.dict(),
        "slug": slug,
        "status": 1,
        "code": code,
        "avatar_img": url_avatar,
        "image_list": images,
        "price_sale": form.price_sale if form.price_sale is not None else form.price,
    }

    # handle delete key in data_product to store in db
    del_key = ['image_1', 'image_2', 'image_3', 'image_4']
    for key in del_key:
        data_product.pop(key, None)

    new_product = products.add_product(db=db, data=data_product)

    if new_product:
        redis_product_detail = {
            "id": new_product.id,
            "name": new_product.name,
            "code": new_product.code,
            "category_id": new_product.category_id,
            "belong_to_store": new_product.belong_to_store,
            "avatar_img": new_product.avatar_img,
            "slug": new_product.slug,
            "status": new_product.status,
            "is_show_on_homepage": new_product.is_show_on_homepage,
            "is_show_on_store": new_product.is_show_on_store,
            "tag": new_product.tag,
            "description": new_product.description,
            "note": new_product.note,
            "brand": new_product.brand,
            "guide": new_product.guide,
            "preserve": new_product.preserve,
            "made_by": new_product.made_by,
            "made_in": new_product.made_in,
            "day_to_shipping": new_product.day_to_shipping,
            "is_active": True,
            "image_list": new_product.image_list,
            "vote_average_score": new_product.vote_average_score
        }

        redis_product_stock = new_product.stock

        redis_product_price = {
            "price": new_product.price,
            "price_sale": new_product.price_sale,
            "unit": new_product.unit,
            "weight": new_product.weight
        }

        # save data into redis
        await redis_drivers.set_product_detail(code, redis_product_detail)
        await redis_drivers.set_product_stock(code, redis_product_stock)
        await redis_drivers.set_product_price(code, redis_product_price)

        # add product to new product
        await redis_drivers.set_product_newest(code, score=1)

    return {
        "detail": "success",
        "data": new_product
    }


@router.put('/update-product/{code}', description=docs_products.updateProduct)
async def update_product(code: str, request: product_schemas.UpdateProductForm = Depends(
    product_schemas.UpdateProductForm.as_form),
                         db: Session = Depends(get_db), current_staff: CurrentStaff = Depends(get_current_staff)):
    current_product_to_update = products.get_product_by_code(db=db, code=code)

    if not current_product_to_update:
        raise HTTPException(status_code=404, detail="Không tìm thấy sản phẩm!")

    slug = slugify(request.name if request.name else current_product_to_update.name)

    # image s3
    s3 = S3()
    url_img = None
    if request.avatar_img is not None:
        n = await random_number(6)
        filename_avatar = 'a{}_{}'.format(code, n)
        path_file = 'product/{}/{}'.format(code, filename_avatar)
        url_img = s3.upload_file_to_s3(request.avatar_img, path_file)

    image_list = list(current_product_to_update.image_list)

    def find_and_replace_image_url(index, url):
        for i, item in enumerate(image_list):
            if item.get('index') == index:
                image_list[i] = {
                    "index": index,
                    "url": url
                }
                break
        else:
            image_list.append({
                "index": index,
                "url": url
            })

    if request.image_1 is not None:
        n1 = await random_number(6)
        file1 = 'd{}_{}'.format(code, n1)
        path1 = 'product/{}/{}'.format(code, file1)
        url1 = s3.upload_file_to_s3(request.image_1, path1)
        find_and_replace_image_url(1, url1)

    if request.image_2 is not None:
        n2 = await random_number(6)
        file2 = 'd{}_{}'.format(code, n2)
        path2 = 'product/{}/{}'.format(code, file2)
        url2 = s3.upload_file_to_s3(request.image_2, path2)
        find_and_replace_image_url(2, url2)

    if request.image_3 is not None:
        n3 = await random_number(6)
        file3 = 'd{}_{}'.format(code, n3)
        path3 = 'product/{}/{}'.format(code, file3)
        url3 = s3.upload_file_to_s3(request.image_3, path3)
        find_and_replace_image_url(3, url3)

    if request.image_4 is not None:
        n4 = await random_number(6)
        file4 = 'd{}_{}'.format(code, n4)
        path4 = 'product/{}/{}'.format(code, file4)
        url4 = s3.upload_file_to_s3(request.image_4, path4)
        find_and_replace_image_url(4, url4)

    data_product = {
        **request.dict(),
        "avatar_img": url_img,
        "image_list": image_list,
        "slug": slug,
    }

    # handle delete key in data_product to store in db
    del_key = ['image_1', 'image_2', 'image_3', 'image_4']
    for key in del_key:
        data_product.pop(key, None)

    current_product = products.update_product(
        db=db, code=code, data=data_product)

    redis_product_detail = {
        "name": current_product.name,
        "code": current_product.code,
        "category_id": current_product.category_id,
        "avatar_img": current_product.avatar_img,
        "slug": current_product.slug,
        "tag": current_product.tag,
        "description": current_product.description,
        "belong_to_store": current_product.belong_to_store,
        "note": current_product.note,
        "brand": current_product.brand,
        "guide": current_product.guide,
        "preserve": current_product.preserve,
        "made_by": current_product.made_by,
        "made_in": current_product.made_in,
        "day_to_shipping": current_product.day_to_shipping,
        "image_list": current_product.image_list,
        "status": current_product.status,
        "vote_average_score": current_product.vote_average_score
    }
    redis_product_stock = current_product.stock
    redis_product_price = {
        "price": current_product.price,
        "price_sale": current_product.price_sale,
        "unit": current_product.unit,
        "weight": current_product.weight
    }

    # set data into redis
    await redis_drivers.set_product_detail(code, redis_product_detail)
    await redis_drivers.set_product_stock(code, redis_product_stock)
    await redis_drivers.set_product_price(code, redis_product_price)

    return {
        "detail": "success",
        "data": current_product
    }


@router.put('/update-status-product/{code}', description=docs_products.updateStatusProduct)
async def update_status_product(code: str, data: product_schemas.StatusProduct, db: Session = Depends(get_db),
                                current_staff: CurrentStaff = Depends(get_current_staff)):
    status = data.status
    current_product = products.update_status_product(
        db=db, code=code, status=status)

    if not current_product:
        raise HTTPException(status_code=400, detail="can not update product")

    # set product into redis
    redis_product_detail = {
        "name": current_product.name,
        "code": current_product.code,
        "category_id": current_product.category_id,
        "avatar_img": current_product.avatar_img,
        "slug": current_product.slug,
        "tag": current_product.tag,
        "description": current_product.description,
        "note": current_product.note,
        "brand": current_product.brand,
        "guide": current_product.guide,
        "preserve": current_product.preserve,
        "made_by": current_product.made_by,
        "made_in": current_product.made_in,
        "day_to_shipping": current_product.day_to_shipping,
        "image_list": current_product.image_list,
        "status": status,
        "vote_average_score": current_product.vote_average_score
    }
    await redis_drivers.set_product_detail(code, redis_product_detail)

    return {
        "detail": "success",
        "data": current_product
    }


@router.get("/user-get-product-sale", description=docs_products.userGetProductSale)
async def user_get_product_sale(limit: Optional[int] = 20, page: Optional[int] = 1, db: Session = Depends(get_db)):
    # get product sale from redis
    products = await redis_drivers.get_product_sale()

    # pagination
    total_product = len(products)
    total_page = math.ceil(total_product / limit)
    skip = limit * (page - 1)

    prev_page = page - 1
    if prev_page <= 0:
        prev_page = None

    next_page = page + 1
    if next_page > total_page:
        next_page = None

    # slice array
    arr = np.array(products)
    temp_product = arr[skip:limit]

    # push data into array
    results = []
    for code in temp_product:
        product_detail = await redis_drivers.get_product_detail(code)
        price = await redis_drivers.get_product_price(code)
        stock = await redis_drivers.get_product_stock(code)
        if price is not None and stock is not None:
            product_detail["price"] = price
            product_detail['stock'] = stock
        results.append(product_detail)

    return {
        "detail": "success",
        "prev_page": prev_page,
        "current_page": page,
        "next_page": next_page,
        "total_page": total_page,
        "limit": limit,
        "data": results
    }


@router.get("/get-product-sale", description=docs_products.getProductSale)
async def get_product_sale(current_staff: CurrentStaff = Depends(get_current_staff)):
    try:
        # get product sale from redis
        products = await redis_drivers.get_product_sale()
        # push data into array
        results = []
        for code in products:
            product_detail = await redis_drivers.get_product_detail(code)
            if (product_detail is not None):
                product_detail['price'] = await redis_drivers.get_product_price(code)
                product_detail['stock'] = await redis_drivers.get_product_stock(code)
                results.append(product_detail)
        return {
            "detail": "success",
            "data": results
        }

    except Exception as e:
        print(e)
        return {
            "detail": "error",
            "data": str(e)
        }


@router.post("/sync-product-sale", description=docs_products.syncProductSale)
async def sync_product_sale(db: Session = Depends(get_db), current_staff: CurrentStaff = Depends(get_current_staff)):
    await redis_drivers.del_product_sale()
    results = products.get_all_product(db=db, is_active=True, status=1)
    counter = 1
    for row in results:
        # Check product is active (status = 1)
        if row.status == 1:
            code = row.code
            await redis_drivers.set_product_sale(code, counter)
            counter += 1
    return True


@router.put("/update-position-product-sale", description=docs_products.updatePositionProductSale)
async def update_position_product_sale(data: product_schemas.UpdatePositionProductSale, db: Session = Depends(get_db),
                                       current_staff: CurrentStaff = Depends(get_current_staff)):
    if len(data.list_product) > 0:
        await redis_drivers.del_product_sale()
        for val in data.list_product:
            await redis_drivers.set_product_sale(str(val.code), val.score)
    return True


class TrendFilter(str, enum.Enum):
    newest = "newest"
    vote = "vote"
    trend = "trend"


@router.get("/get-product-trend", description=docs_products.getProductTrend)
async def get_product_trend(filter: Optional[TrendFilter] = 'newest', limit: Optional[int] = 20,
                            page: Optional[int] = 1,
                            db: Session = Depends(get_db)):
    # get product sale from redis
    if filter == 'vote':
        products = await redis_drivers.get_product_vote()
    elif filter == 'trend':
        products = await redis_drivers.get_product_trend()
    else:
        products = await redis_drivers.get_product_newest()

    # pagination
    total_product = len(products)
    total_page = math.ceil(total_product / limit)
    skip = limit * (page - 1)

    prev_page = page - 1
    if prev_page <= 0:
        prev_page = None

    next_page = page + 1
    if next_page > total_page:
        next_page = None

    # slice array
    arr = np.array(products)
    temp_product = arr[skip:limit]

    # push data into array
    results = []
    for code in temp_product:
        product_detail = await redis_drivers.get_product_detail(code)
        product_detail['price'] = await redis_drivers.get_product_price(code)
        product_detail['stock'] = await redis_drivers.get_product_stock(code)
        results.append(product_detail)

    return {
        "detail": "success",
        "prev_page": prev_page,
        "current_page": page,
        "next_page": next_page,
        "total_page": total_page,
        "limit": limit,
        "data": results
    }


@router.get("/get-product-relation", description=docs_products.getProductRelation)
async def get_product_relation(product_code: str, category_id: int, db: Session = Depends(get_db)):
    results = await products.get_list_product_by_category_id(
        db=db, category_id=category_id, limit=5, skip=0, is_active=True)
    data = []
    for row in results:
        if row.code != product_code:
            detail = await redis_drivers.get_product_detail(row.code)
            if detail is not None:
                detail['price'] = await redis_drivers.get_product_price(row.code)
                detail['stock'] = await redis_drivers.get_product_stock(row.code)
                data.append(detail)
    return {
        "detail": "success",
        "data": data
    }


@router.get("/get-product-suggest", description=docs_products.getProductSuggest)
async def get_product_suggest(db: Session = Depends(get_db)):
    results = await products.get_list_product_by_category_id(
        db=db, category_id=4, limit=5, skip=0, is_active=True)
    data = []
    for row in results:
        code = row.code
        detail = await redis_drivers.get_product_detail(code)
        if detail is not None:
            price = await redis_drivers.get_product_price(code)
            stock = await redis_drivers.get_product_stock(code)
            detail.update({'price': price, 'stock': stock})
            data.append(detail)
    return {
        "detail": "success",
        "data": data
    }


# Vote for products


@router.get('/vote/{product_code}', tags=['Product Vote'], response_model=response_models.ProductVote,
            description=docs_product_vote.voteListInProduct)
async def get_vote_list_in_product(product_code: str, db: Session = Depends(get_db)):
    results = products.get_product_vote_list(db=db, product_code=product_code)
    if results is not None:
        return results


@router.get('/vote/check-user-buy/{product_code}', tags=['Product Vote'],
            response_model=response_models.UserCheckReceivingSuccessFull,
            description=docs_product_vote.checkUserIsBuyThisProduct)
async def check_user_receiving_product_successfull(product_code: str, db: Session = Depends(get_db),
                                                   current_user: CurrentUser = Depends(get_current_user)):
    user_id = current_user.user_id
    result = products.check_user_receiving_product_successfull(
        db=db, product_code=product_code, user_id=user_id)
    return result


@router.post("/vote/{product_code}", tags=['Product Vote'], response_model=product_schemas.ProductUserVoteBase,
             description=docs_product_vote.addNewVoteForProduct)
async def add_vote_product(product_code: str, vote: product_schemas.ProductUserVote, db: Session = Depends(get_db),
                           current_user=Depends(get_current_user)):
    vote_obj = jsonable_encoder(vote)  # Convert schema to json
    user_id = current_user.user_id
    try:
        results = products.add_product_vote(
            product_code=product_code, user_id=user_id, vote=vote_obj, db=db)
        return results
    except Exception as e:
        print(e)
        return {
            "detail": "error",
            "error": str(e)
        }


@router.get('/vote/id/{vote_id}', tags=['Product Vote'], response_model=response_models.VoteInfoResponse,
            description=docs_product_vote.getVoteProductByVoteId)
async def get_vote_info_by_id(vote_id: int, db: Session = Depends(get_db)):
    results = products.get_product_vote_by_id(db=db, vote_id=vote_id)
    if results is not None:
        return {
            'detail': 'success',
            'data': results
        }
    else:
        return {
            "detail": 'Not found this vote',
            'data': None
        }


@router.put('/vote/{product_code}/id/{vote_id}', tags=['Product Vote'],
            response_model=product_schemas.ProductUserVoteBase,
            description=docs_product_vote.updateVoteForProduct)
async def update_vote_info(product_code: str, vote_id: int, vote: product_schemas.ProductUserVote,
                           db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    vote_obj = jsonable_encoder(vote)
    current_user_id = current_user.user_id
    try:
        results = products.update_product_vote(
            product_code=product_code, vote_id=vote_id, user_id=current_user_id, vote=vote_obj, db=db)
        return results
    except Exception as e:
        print(e)
        return {
            'detail': "error",
            'error': str(e)
        }


@router.get('/fix-product-redis', summary='For Admin Only')
async def fix_product_in_redis(db: Session = Depends(get_db), current_staff: CurrentStaff = Depends(get_current_staff)):
    if current_staff.role == 'admin':
        await redis_drivers.del_product_detail()
        await redis_drivers.del_product_stock()
        await redis_drivers.del_product_price()
        await redis_drivers.del_product_trend()
        await redis_drivers.del_product_newest()
        await redis_drivers.del_product_vote()
        await redis_drivers.del_product_sale()

        # set product newest
        score = 1
        list_product_newest = products.get_product_newest(db=db, limit=20)
        for product in list_product_newest:
            await redis_drivers.set_product_newest(product.code, score)
            score += 1

        # set product vote
        score = 1
        list_product_vote = products.get_all_product_for_vote(db=db, limit=20)
        for product in list_product_vote:
            await redis_drivers.set_product_vote(product.code, score)
            score += 1

        # set product trend
        score = 1
        list_product_trend = products.get_list_product_trend(db=db, limit=20)
        for product in list_product_trend:
            await redis_drivers.set_product_trend(product.code, score)
            score += 1

        score = 1
        list_product_sale = products.get_list_product_sale_for_fix(db=db, limit=20)
        for product in list_product_sale:
            await redis_drivers.set_product_sale(product.code, score)
            score += 1

        # set product detail
        db_products = products.get_product_list_for_fix(db=db)
        for current_product in db_products:
            redis_product_detail = {
                "id": current_product.id,
                "name": current_product.name,
                "code": str(current_product.code),
                "category_id": current_product.category_id,
                "avatar_img": current_product.avatar_img,
                "slug": current_product.slug,
                "tag": current_product.tag,
                "description": current_product.description,
                "belong_to_store": current_product.belong_to_store,
                "note": current_product.note,
                "brand": current_product.brand,
                "guide": current_product.guide,
                "preserve": current_product.preserve,
                "made_by": current_product.made_by,
                "made_in": current_product.made_in,
                "day_to_shipping": current_product.day_to_shipping,
                "image_list": current_product.image_list,
                "status": current_product.status,
                "sale_count": current_product.sale_count,
                "vote_average_score": current_product.vote_average_score
            }
            redis_product_stock = current_product.stock
            redis_product_price = {
                "price": current_product.price,
                "price_sale": current_product.price_sale,
                "unit": current_product.unit,
                "weight": current_product.weight
            }
            await redis_drivers.set_product_detail(current_product.code, redis_product_detail)
            await redis_drivers.set_product_stock(current_product.code, redis_product_stock)
            await redis_drivers.set_product_price(current_product.code, redis_product_price)
        return True
    return False
