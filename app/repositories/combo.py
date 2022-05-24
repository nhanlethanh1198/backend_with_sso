import json
from datetime import datetime
from functools import partial
from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app import models


def get_count_combo_list(db: Session, location: Optional[int] = None, is_active: Optional[bool] = None):
    filter_ = ()
    if location:
        filter_ = (*filter_, models.Combo.f_location == location)
    if is_active is not None:
        filter_ = (*filter_, models.Combo.is_active == is_active)

    return db.query(models.Combo).filter(*filter_).count()


def get_product_in_combo(db: Session, combo_id: int):
    list_product_of_combo = jsonable_encoder(
        db.query(models.ComboProduct).filter(models.ComboProduct.combo_id == combo_id).all())
    for product in list_product_of_combo:
        columns = (models.Product.code, models.Product.name, models.Product.avatar_img, models.Product.weight,
                   models.Product.unit,
                   models.Product.price, models.Product.price_sale)
        p = db.query(*columns).filter(models.Product.id == product['product_id']).first()
        product['code'] = p.get('code')
        product['name'] = p.get('name')
        product['avatar_img'] = p.get('avatar_img')
        product['weight'] = p.get('weight')
        product['unit'] = p.get('unit')
        product['price'] = p.get('price')
        product['price_sale'] = p.get('price_sale')
    return list_product_of_combo


def get_combo_list(db: Session,
                   limit: Optional[int] = 20,
                   offset: Optional[int] = 0,
                   is_active: Optional[bool] = None,
                   location: Optional[int] = None):
    filter_ = ()
    if is_active is not None:
        filter_ = (*filter_, models.Combo.is_active == is_active)
    if location:
        filter_ = (*filter_, models.Combo.f_location == location)

    list_combo = jsonable_encoder(
        db.query(models.Combo).filter(*filter_).order_by(desc(models.Combo.created_at)).limit(limit).offset(
            offset).all())

    for item in list_combo:
        item['products'] = get_product_in_combo(db=db, combo_id=item.get('id'))

    return list_combo


def get_suggest_combo(db: Session, combo_id: int):
    suggest_combo_list = jsonable_encoder(
        db.query(models.Combo).filter(models.Combo.id != combo_id, models.Combo.is_active == True).all())

    for combo in suggest_combo_list:
        combo['products'] = get_product_in_combo(db=db, combo_id=combo.get('id'))
    return suggest_combo_list


def get_combo_by_id(db: Session, combo_id: int):
    combo = db.query(models.Combo).get({"id": combo_id})

    if combo is None:
        return None

    product_list = get_product_in_combo(db=db, combo_id=combo_id)

    return {
        'info': combo,
        'products': product_list
    }


def get_combo_by_code(db: Session, code: str):
    current_combo = jsonable_encoder(db.query(models.Combo).filter(models.Combo.code == code).first())
    if current_combo is None:
        return None

    products_in_combo = jsonable_encoder(
        db.query(models.ComboProduct).filter_by(combo_id=current_combo.get('id')).all())

    for product in products_in_combo:
        p = jsonable_encoder(db.query(models.Product).filter_by(id=product.get('product_id')).first())

        product['code'] = p.get('code')
        product['name'] = p.get('name')
        product['avatar_img'] = p.get('avatar_img')
        product['weight'] = p.get('weight')
        product['unit'] = p.get('unit')
        product['price'] = p.get('price')
        product['price_sale'] = p.get('price_sale')

    return {
        **current_combo,
        "products": products_in_combo
    }


def get_detail_combo(db: Session, products: List[int]):
    combo_details = db.query(models.Product).filter(
        models.Product.code.in_(products)).all()
    return combo_details


def create_combo(db: Session, data: dict):
    combo = dict(data)
    combo.pop('products')

    new_combo = models.Combo(
        **combo,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    db.add(new_combo)
    db.commit()
    db.refresh(new_combo)

    result = jsonable_encoder(new_combo)

    # Add Product to combo
    if new_combo is not None:
        products = data['products']
        if products is not None:
            product_list = json.loads(products)
            for product in product_list:
                new_product_in_combo = models.ComboProduct(
                    combo_id=new_combo.id,
                    product_id=product['product_id'],
                    count=product['count'],
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                )
                db.add(new_product_in_combo)
                db.commit()
                db.refresh(new_product_in_combo)
    return result


def update_combo_by_id(db: Session, combo_id: int, data: dict):
    combo = db.query(models.Combo).get({"id": combo_id})
    if combo:
        for key, value in data.items():
            if value != '' and value is not None and key != 'products':
                setattr(combo, key, value)
        combo.updated_at = datetime.now()
        db.commit()
        db.refresh(combo)

        result = jsonable_encoder(combo)

        # Edit Product In Combo
        products = data['products']
        if products is not None:
            product_list = json.loads(products)
            if len(product_list) > 0:
                update_product_in_combo(db=db, combo_id=combo_id, product_list=product_list)
        return result
    return None


def add_product_in_combo(db: Session, combo_id: int, product_id: int, count: int):
    new_product_in_combo = models.ComboProduct(
        combo_id=combo_id,
        product_id=product_id,
        count=count,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    db.add(new_product_in_combo)
    db.commit()
    db.refresh(new_product_in_combo)
    return True


def delete_product_in_combo(db: Session, combo_id: int, product_id: int):
    combo_product = db.query(models.ComboProduct).filter_by(combo_id=combo_id, product_id=product_id).first()
    if combo_product:
        db.delete(combo_product)
        db.commit()
        return True
    return False


def update_product_in_combo(db: Session, combo_id: int, product_list: List):
    # Check how many products in combo?
    count_product_in_combo = db.query(models.ComboProduct).filter_by(combo_id=combo_id).count()
    # if len(product_list) > product_count:
    # add new product
    # if len(product_list) < product_count:
    # filter product not in list => delete
    # else: count_product = len(product_list))
    # edit
    if len(product_list) <= 0:
        return False
    else:
        # if len(product_list) > product_count:
        # add new product
        if len(product_list) > count_product_in_combo:
            for product in product_list:
                current_product = db.query(models.ComboProduct).get({"id": product['id']})
                if current_product is None:
                    add_product_in_combo(db=db, combo_id=combo_id, product_id=product['product_id'],
                                         count=product['count'])
                else:
                    current_product = db.query(models.ComboProduct).filter_by(id=product['id'],
                                                                              combo_id=combo_id).first()
                    current_product.product_id = product['product_id']
                    current_product.count = product['count']
                    current_product.updated_at = datetime.now()
                    db.commit()
                    db.refresh(current_product)
            return True

        # if len(product_list) < product_count:
        # filter product not in list => delete
        if len(product_list) < count_product_in_combo:
            # get product list in combo
            product_list_in_combo = db.query(models.ComboProduct.id).filter_by(combo_id=combo_id).all()
            list_product_id = list(map(lambda x: x['id'], product_list_in_combo))

            # Filter product not in list => delete
            list_product_id_update = list(map(lambda x: x['id'], product_list))
            list_product_not_in_list = [id for id in list_product_id if id not in list_product_id_update]
            # delete
            for id in list_product_not_in_list:
                db.query(models.ComboProduct).filter_by(id=id).delete()
                db.commit()

            for product in product_list:
                current_product = db.query(models.ComboProduct).filter_by(id=product['id'], combo_id=combo_id).first()
                if current_product is not None:
                    current_product.product_id = product['product_id']
                    current_product.count = product['count']
                    current_product.updated_at = datetime.now()
                    db.commit()
                    db.refresh(current_product)
                else:
                    add_product_in_combo(db=db, combo_id=combo_id, product_id=product['product_id'],
                                         count=product['count'])
            return True

        # else: count_product = len(product_list))
        else:
            for product in product_list:
                current_product = db.query(models.ComboProduct).filter_by(id=product['id'], combo_id=combo_id).first()
                if current_product is not None:
                    current_product.product_id = product['product_id']
                    current_product.count = product['count']
                    current_product.updated_at = datetime.now()
                    db.commit()
                    db.refresh(current_product)
                else:
                    add_product_in_combo(db=db, combo_id=combo_id, product_id=product['product_id'],
                                         count=product['count'])
            return True


def active_combo_by_id(db: Session, combo_id: int, is_active: bool):
    combo = db.query(models.Combo).filter(models.Combo.id == combo_id).first()
    if combo:
        combo.is_active = is_active
        combo.updated_at = datetime.now()
        db.commit()
        db.refresh(combo)
        return combo
    return combo


# Vote
def update_vote_one_star(combo: any, type: str = 'add'):
    if type == 'add':
        combo.vote_one_star_count += 1
    elif type == 'sub':
        combo.vote_one_star_count -= 1
    return True


def update_vote_two_star(combo: any, type: str = 'add'):
    if type == 'add':
        combo.vote_two_star_count += 1
    elif type == 'sub':
        combo.vote_two_star_count -= 1
    return True


def update_vote_three_star(combo: any, type: str = 'add'):
    if type == 'add':
        combo.vote_three_star_count += 1
    elif type == 'sub':
        combo.vote_three_star_count -= 1
    return True


def update_vote_four_star(combo: any, type: str = 'add'):
    if type == 'add':
        combo.vote_four_star_count += 1
    elif type == 'sub':
        combo.vote_four_star_count -= 1
    return True


def update_vote_five_star(combo: any, type: str = 'add'):
    if type == 'add':
        combo.vote_five_star_count += 1
    elif type == 'sub':
        combo.vote_five_star_count -= 1
    return True


def update_vote_count_case(score: int, combo: any, type: str = 'add', ):
    switcher = {
        1: partial(update_vote_one_star, combo, type),
        2: partial(update_vote_two_star, combo, type),
        3: partial(update_vote_three_star, combo, type),
        4: partial(update_vote_four_star, combo, type),
        5: partial(update_vote_five_star, combo, type)
    }
    func = switcher.get(score, False)
    return func()


# tinh so diem vote trung binh


def calculate_average_vote_score(combo: any):
    average_vote_score = (
                                 combo.vote_one_star_count * 1 +
                                 combo.vote_two_star_count * 2 +
                                 combo.vote_three_star_count * 3 +
                                 combo.vote_four_star_count * 4 +
                                 combo.vote_five_star_count * 5) / combo.vote_count
    return "{:.1f}".format(average_vote_score)


def add_combo_vote(combo_id: int, user_id: int, data: dict, db: Session):
    combo = db.query(models.Combo).get(combo_id)

    score = data.get('vote_score')

    #  Update vote score count
    def update_vote_in_combo(score):

        result = update_vote_count_case(score=score, combo=combo, type='add')

        if result:
            combo.vote_count += 1
            combo.vote_average_score = float(calculate_average_vote_score(combo))
            combo.vote_count_updated_at = datetime.now()
            db.commit()
            db.refresh(combo)
            return True
        else:
            return False

    updated_combo = update_vote_in_combo(score)

    if updated_combo is not None:
        combo_user_vote = models.ComboVote(
            **data,
            user_id=user_id,
            combo_id=combo_id,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.add(combo_user_vote)
        db.commit()
        db.refresh(combo_user_vote)
        return combo_user_vote

    return None


def update_combo_vote(vote_id: int, user_id: int, data: any, db: Session):
    # try:
    score = data.vote_score

    currentVote = db.query(models.ComboVote).filter_by(id=vote_id, user_id=user_id).first()
    if currentVote is None:
        raise HTTPException(status_code=401, detail="Bạn không có quyền truy cập để cập nhật thông tin này!")

    tempCurrentComboVoteScore = currentVote.vote_score

    currentVote.comment = data.comment
    currentVote.tags = data.tags
    currentVote.updated_at = datetime.now()

    # Check vote score change
    if score != tempCurrentComboVoteScore:
        currentVote.vote_score = score
        currentCombo = db.query(models.Combo).filter_by(id=currentVote.combo_id).first()
        checkUpVote = update_vote_count_case(score=score, combo=currentCombo, type='add')
        checkDownVote = update_vote_count_case(score=tempCurrentComboVoteScore, combo=currentCombo, type='sub')

        if checkUpVote == True and checkDownVote == True:
            currentCombo.vote_average_score = calculate_average_vote_score(currentCombo)
            currentCombo.vote_count_updated_at = datetime.now()
            db.commit()
            db.refresh(currentCombo)
    return True

    # except Exception as e:
    #     print(e)
    #     return False


def get_list_vote_in_combo(combo_id: int, db: Session):
    current_combo = jsonable_encoder(db.query(
        models.Combo.id,
        models.Combo.name,
        models.Combo.vote_count,
        models.Combo.vote_average_score,
        models.Combo.vote_one_star_count,
        models.Combo.vote_two_star_count,
        models.Combo.vote_three_star_count,
        models.Combo.vote_four_star_count,
        models.Combo.vote_five_star_count,
    ).filter_by(id=combo_id).first())

    current_combo_vote_list = jsonable_encoder(db.query(
        models.ComboVote.id,
        models.ComboVote.comment,
        models.ComboVote.tags,
        models.ComboVote.vote_score,
        models.ComboVote.created_at,
        models.ComboVote.updated_at,
        models.User.fullname,
        models.User.address).outerjoin(models.User).filter(models.ComboVote.combo_id == combo_id).all())

    current_combo['vote_list'] = current_combo_vote_list

    return current_combo


def get_vote_info_by_vote_id(db: Session, vote_id: int):
    try:
        current_combo_vote = db.query(
            models.Combo.name,
            models.User.fullname,
            models.ComboVote.id,
            models.User.address,
            models.ComboVote.vote_score,
            models.ComboVote.comment,
            models.ComboVote.tags,
            models.ComboVote.created_at,
            models.ComboVote.updated_at
        ).join(models.User).filter(models.ComboVote.id == vote_id).first()
        return current_combo_vote
    except Exception as e:
        print(e)
        return False
