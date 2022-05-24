from datetime import datetime
from functools import partial
from typing import Optional

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app import models
from app.schemas import product_schemas


async def get_list_product_by_category_id(db: Session, category_id: int, limit: int, skip: int, is_active: bool):
    return db.query(models.Product.code).filter_by(
        category_id=category_id,
        is_active=is_active,
        status=1
    ).offset(skip).limit(limit).all()


def get_product_by_code(db: Session, code: str):
    return db.query(models.Product).filter(models.Product.code == code).first()


def get_products_code_by_store(db: Session, store_id: int, category_id: Optional[int] = None,
                               status: Optional[int] = 1):
    filters = {
        "belong_to_store": store_id,
        "status": status
    }
    if category_id:
        filters = {
            **filters,
            "category_id": category_id
        }

    product_list = db.query(models.Product.code).filter_by(**filters).distinct().all()
    product_list = [product[0] for product in product_list]
    return product_list


def count_products_in_store(db: Session, store_id: int, category_id: Optional[int] = None, status: Optional[int] = 1):
    filters = {
        "belong_to_store": store_id,
        "status": status
    }
    if category_id:
        filters = {
            **filters,
            "category_id": category_id
        }

    return db.query(models.Product).filter_by(**filters).count()


def get_product_list_by_store_id(db: Session, store_id: int, limit: int = 10, skip: int = 0, status: Optional[int] = 1):
    return db.query(models.Product).filter_by(belong_to_store=store_id, status=status).order_by(
        desc(models.Product.updated_at)).limit(limit).offset(skip).all()


def add_product(db: Session, data):
    db_product = models.Product(
        **data
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_list_product(db: Session, category_id: Optional[int] = None, status: Optional[int] = None,
                     store_id: Optional[int] = None, skip: int = 0,
                     limit: int = 20):
    if category_id:
        if status:
            if store_id:
                return db.query(models.Product).filter(models.Product.category_id == category_id,
                                                       models.Product.status == status,
                                                       models.Product.belong_to_store == store_id).order_by(
                    desc(models.Product.updated_at)).offset(skip).limit(limit).all()

            return db.query(models.Product).filter(models.Product.category_id == category_id,
                                                   models.Product.status == status).order_by(
                desc(models.Product.updated_at)).offset(skip).limit(limit).all()
        else:
            if store_id:
                return db.query(models.Product).filter(models.Product.category_id == category_id,
                                                       models.Product.belong_to_store == store_id).order_by(
                    desc(models.Product.updated_at)).offset(skip).limit(limit).all()
            return db.query(models.Product).filter(models.Product.category_id == category_id).order_by(
                desc(models.Product.updated_at)).offset(skip).limit(limit).all()
    else:
        if status:
            if store_id:
                return db.query(models.Product).filter(models.Product.status == status,
                                                       models.Product.belong_to_store == store_id).order_by(
                    desc(models.Product.updated_at)).offset(skip).limit(limit).all()

            return db.query(models.Product).filter(models.Product.status == status).order_by(
                desc(models.Product.updated_at)).offset(skip).limit(limit).all()
        else:
            if store_id:
                return db.query(models.Product).filter(models.Product.belong_to_store == store_id).order_by(
                    desc(models.Product.updated_at)).offset(skip).limit(limit).all()
            return db.query(models.Product).order_by(desc(models.Product.updated_at)).offset(skip).limit(limit).all()


def query_products_list_code(db: Session,
                             category_id: Optional[int] = None,
                             status: Optional[int] = None,
                             location: Optional[int] = None,
                             store_id: Optional[int] = None,
                             is_show_on_homepage: Optional[bool] = None,
                             is_show_on_store: Optional[bool] = None,
                             is_show_on_combo: Optional[bool] = None,
                             ):
    filter_ = ()
    if status:
        filter_ = (*filter_, models.Product.status == status if status else 1)
    if category_id:
        filter_ = (*filter_, models.Product.category_id == category_id)
    if store_id:
        filter_ = (*filter_, models.Product.belong_to_store == store_id)
    if location:
        filter_ = (*filter_, models.Product.location == location)
    if is_show_on_homepage is not None:
        filter_ = (*filter_, models.Product.is_show_on_homepage == is_show_on_homepage)
    if is_show_on_store is not None:
        filter_ = (*filter_, models.Product.is_show_on_store == is_show_on_store)
    if is_show_on_combo is not None:
        filter_ = (*filter_, models.Product.is_show_on_combo == is_show_on_combo)

    list_products_code = db.query(models.Product.code).filter(*filter_).distinct().all()

    # convert to list
    list_products_code = [product[0] for product in list_products_code]
    return list_products_code


def update_product(db: Session, code: str, data: any):
    current_product = db.query(models.Product).filter(
        models.Product.code == code).first()
    if current_product is not None:
        for key, value in data.items():
            if key != 'avatar_img' and key != 'image_list' and value is not None:
                setattr(current_product, key, value)

        if data.get('avatar_img') is not None:
            current_product.avatar_img = data.get('avatar_img')

        if data.get('image_list') is not None:
            current_product.image_list = data.get('image_list')

        current_product.updated_at = datetime.now()
        db.commit()
        db.refresh(current_product)
        return current_product
    else:
        return current_product


def update_status_product(db: Session, code, status):
    current_product = db.query(models.Product).filter(
        models.Product.code == code).first()
    if current_product != None:
        current_product.status = status
        db.commit()
        db.refresh(current_product)
        return current_product
    else:
        return current_product


def get_all_product(db: Session, is_active: bool, status: int):
    return db.query(models.Product).filter(
        models.Product.is_active == is_active,
        models.Product.status == status,
        models.Product.price > models.Product.price_sale).order_by(models.Product.sale_count).all()


def get_product_newest(db: Session, limit: int = 10):
    return db.query(models.Product.code).filter(models.Product.status == 1).order_by(
        desc(models.Product.created_at)).limit(limit).all()


def get_all_product_for_vote(db: Session, limit: int = 10):
    return db.query(models.Product.code).filter(models.Product.status == 1, models.Product.vote_count > 0).order_by(
        desc(models.Product.vote_count)).limit(limit).all()


def get_list_product_trend(db: Session, limit: int = 10):
    return db.query(models.Product.code).filter(models.Product.status == 1, models.Product.sale_count > 0).order_by(
        desc(models.Product.sale_count)).limit(limit).all()


def get_list_product_sale_for_fix(db: Session, limit: int = 20):
    return db.query(models.Product.code).filter(models.Product.status == 1).order_by(
        desc(models.Product.sale_count)).limit(limit).all()


def get_product_vote_list(db: Session, product_code: str):
    try:
        current_product = db.query(
            models.Product.id,
            models.Product.code,
            models.Product.name,
            models.Product.vote_count,
            models.Product.vote_average_score,
            models.Product.vote_five_star_count,
            models.Product.vote_four_star_count,
            models.Product.vote_three_star_count,
            models.Product.vote_two_star_count,
            models.Product.vote_one_star_count
        ).filter(
            models.Product.code == product_code).first()

        current_product_vote_list = db.query(
            models.ProductUserVote.id,
            models.ProductUserVote.comment,
            models.ProductUserVote.tags,
            models.ProductUserVote.vote_score,
            models.ProductUserVote.created_at,
            models.ProductUserVote.updated_at,
            models.User.fullname,
            models.User.address
        ).outerjoin(models.User).filter(models.ProductUserVote.product_id == current_product.id).all()

        return {
            "product": current_product,
            "vote_list": current_product_vote_list
        }
    except Exception as e:
        print(e)
        return False


def check_user_receiving_product_successfull(db: Session, product_code: str, user_id: int):
    try:
        current_detail_order_list = db.query(models.OrderDetail.order_id).filter_by(
            code=product_code, user_id=user_id).order_by(models.OrderDetail.id.desc()).all()

        order_list = jsonable_encoder(current_detail_order_list)

        order_id_list = map(
            lambda x: x['order_id'], order_list)

        id_list = list(order_id_list)

        if len(id_list) > 0:
            user_order = db.query(models.Order.status).filter(
                models.Order.user_id == user_id,
                models.Order.id.in_(id_list),
                models.Order.status == 5).order_by(desc(models.Order.updated_at)).first()
            print(jsonable_encoder(user_order))
            if user_order is not None:
                return {
                    "result": True
                }
            else:
                return {
                    "result": False
                }
        return {
            "result": False
        }
    except Exception as e:
        print(str(e))

        return {
            "result": False
        }


def add_product_vote(product_code: str, user_id: int, vote: product_schemas.ProductUserVote, db: Session):
    product = db.query(models.Product).filter(
        models.Product.code == product_code).first()

    def update_vote_one_star():
        product.vote_one_star_count += 1
        return True

    def update_vote_two_star():
        product.vote_two_star_count += 1
        return True

    def update_vote_three_star():
        product.vote_three_star_count += 1
        return True

    def update_vote_four_star():
        product.vote_four_star_count += 1
        return True

    def update_vote_five_star():
        product.vote_five_star_count += 1
        return True

    def update_vote_count_case(score):
        # switch case
        switcher = {
            1: update_vote_one_star,
            2: update_vote_two_star,
            3: update_vote_three_star,
            4: update_vote_four_star,
            5: update_vote_five_star
        }

        # chay switch case voi score truyen vao
        func = switcher.get(score, False)
        return func()

    # Tinh so sao trung binh
    def calculate_average_vote_score():
        average_vote_score = (
                                     product.vote_one_star_count * 1 +
                                     product.vote_two_star_count * 2 +
                                     product.vote_three_star_count * 3 +
                                     product.vote_four_star_count * 4 +
                                     product.vote_five_star_count * 5) / product.vote_count
        return "{:.1f}".format(average_vote_score)

    # update vote score count
    def update_vote_in_product(score):

        result = update_vote_count_case(score)

        if (result):
            product.vote_count += 1
            product.vote_average_score = float(calculate_average_vote_score())
            product.vote_count_updated_at = datetime.now()
            db.commit()
            db.refresh(product)
            return True
        else:
            return False

    updated_product = update_vote_in_product(vote['vote_score'])

    if (updated_product):
        productUserVote = models.ProductUserVote(
            **vote,
            user_id=user_id,
            product_id=product.id,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.add(productUserVote)
        db.commit()
        db.refresh(productUserVote)
        return productUserVote


def get_product_vote_by_id(db: Session, vote_id: int):
    try:
        current_product_vote = db.query(
            models.ProductUserVote.id,
            models.Product.code,
            models.User.fullname,
            models.User.address,
            models.Product.name,
            models.ProductUserVote.vote_score,
            models.ProductUserVote.comment,
            models.ProductUserVote.tags,
            models.Product.name,
            models.ProductUserVote.created_at,
            models.ProductUserVote.updated_at).join(
            models.Product).join(models.User).filter(models.ProductUserVote.id == vote_id).first()
        return current_product_vote
    except Exception as e:
        print(e)
        return False


def update_product_vote(product_code: str, vote_id: int, user_id: int, vote: product_schemas.ProductUserVote,
                        db: Session):
    try:
        vote_score = vote['vote_score']
        currentProductVote = db.query(
            models.ProductUserVote).get({'id': vote_id})

        if (currentProductVote.user_id != user_id):
            raise HTTPException(
                status_code=401, detail='Bạn không có quyền truy cập để cập nhật thông tin này!')

        tempCurrentProductVoteScore = currentProductVote.vote_score

        currentProductVote.comment = vote['comment']
        currentProductVote.tags = vote['tags']
        currentProductVote.vote_score = vote_score
        currentProductVote.updated_at = datetime.now()

        # Update Product when change score

        def update_score_in_product(vote_score, previous_vote_score):
            try:
                product = db.query(models.Product).filter(
                    models.Product.code == product_code).first()

                def update_vote_one_star(type: str):
                    if (type == 'add'):
                        product.vote_one_star_count += 1
                    elif (type == 'sub'):
                        product.vote_one_star_count -= 1
                    return True

                def update_vote_two_star(type: str):
                    if (type == 'add'):
                        product.vote_two_star_count += 1
                    elif (type == 'sub'):
                        product.vote_two_star_count -= 1
                    return True

                def update_vote_three_star(type: str):
                    if (type == 'add'):
                        product.vote_three_star_count += 1
                    elif (type == 'sub'):
                        product.vote_three_star_count -= 1
                    return True

                def update_vote_four_star(type: str):
                    if (type == 'add'):
                        product.vote_four_star_count += 1
                    elif (type == 'sub'):
                        product.vote_four_star_count -= 1
                    return True

                def update_vote_five_star(type: str):
                    if (type == 'add'):
                        product.vote_five_star_count += 1
                    elif (type == 'sub'):
                        product.vote_five_star_count -= 1
                    return True

                def update_vote_count_case(score: int, type: str):
                    # switch case
                    switcher = {
                        1: partial(update_vote_one_star, type),
                        2: partial(update_vote_two_star, type),
                        3: partial(update_vote_three_star, type),
                        4: partial(update_vote_four_star, type),
                        5: partial(update_vote_five_star, type)
                    }

                    # chay switch case voi score truyen vao
                    func = switcher.get(score, False)
                    return func()

                # Check vote_score and previous_vote_score is different
                # If different, update score in product

                if (vote_score != previous_vote_score):
                    try:
                        # Không chạy được switch case chỗ này
                        checkUpvote = update_vote_count_case(
                            score=vote_score, type='add')
                        checkDownVote = update_vote_count_case(
                            score=previous_vote_score, type='sub')

                        if (checkUpvote == True and checkDownVote == True):
                            # Tinh lai diem trung binh
                            average_vote_score = (
                                                         product.vote_one_star_count * 1 +
                                                         product.vote_two_star_count * 2 +
                                                         product.vote_three_star_count * 3 +
                                                         product.vote_four_star_count * 4 +
                                                         product.vote_five_star_count * 5) / product.vote_count
                            product.vote_average_score = float(
                                "{:.1f}".format(average_vote_score))
                            db.commit()
                            db.refresh(product)
                            return True

                        product.vote_count_updated_at = datetime.now()

                        db.commit()
                        db.refresh(product)
                    except Exception as e:
                        print(str(e))
                        return False
                return True

            except Exception as e:
                print(e)
                return False

        updated_product = update_score_in_product(
            vote_score, tempCurrentProductVoteScore)

        if (updated_product):
            db.commit()
            db.refresh(currentProductVote)
            return currentProductVote
        else:
            return False
    except Exception as e:
        print(str(e))
        return False


def get_product_list_for_fix(db: Session):
    db_products_list = db.query(models.Product).all()
    return db_products_list
