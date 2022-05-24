from datetime import datetime
from typing import Optional, List

from fastapi.encoders import jsonable_encoder
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app import models


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def check_password_of_user(db: Session, phone: str, hashed_password: str):
    return db.query(models.User).filter_by(phone=phone, hashed_password=hashed_password).first()


def update_password(db: Session, user_id: int, hashed_password: str):
    current_user = db.query(models.User).filter(models.User.id == user_id).first()
    if current_user is not None:
        current_user.updated_at = datetime.now()
        current_user.hashed_password = hashed_password
        db.commit()
        db.refresh(current_user)
    return current_user


def create_new_user(db: Session, payload_of_user: dict):
    new_user = models.User(**payload_of_user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_by_phone(db: Session, phone: str):
    return db.query(models.User).filter(models.User.phone == phone).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def update_user_info(db: Session, user_id: int, fullname: str, address: str, dob, email):
    current_user = db.query(models.User).filter(models.User.id == user_id).first()
    if current_user is not None:
        current_user.fullname = fullname
        current_user.address = address

        if dob is not None:
            current_user.dob = dob
        if email is not None:
            current_user.email = email

        db.commit()
        db.refresh(current_user)
    return current_user


def count_user(db: Session, phone):
    if phone is not None:
        return db.query(models.User).filter(models.User.phone == phone).count()
    else:
        return db.query(models.User).count()


def get_list_user(db: Session, phone, skip, limit):
    if phone is not None:
        return db.query(models.User).filter(models.User.phone == phone).offset(skip).limit(limit).all()
    else:
        return db.query(models.User).offset(skip).limit(limit).all()


def lock_user(db: Session, user_id, is_active):
    current_user = db.query(models.User).filter(models.User.id == user_id).first()
    if current_user is not None:
        current_user.is_active = is_active
        db.commit()
        db.refresh(current_user)
    return current_user


def user_update_location(db: Session, user_id: int, location: str):
    current_user = db.query(models.User).filter(models.User.id == user_id).first()
    if current_user is not None:
        current_user.address = location
        db.commit()
        db.refresh(current_user)
    return current_user


def count_favorite_staff_list(db: Session, user_id: int, is_favorite: Optional[bool] = None):
    if is_favorite is not None:
        return db.query(models.FavoriteStaffOfUser).filter(models.FavoriteStaffOfUser.user_id == user_id,
                                                           models.FavoriteStaffOfUser.is_favorite == is_favorite).count()
    else:
        return db.query(models.FavoriteStaffOfUser).filter(models.FavoriteStaffOfUser.user_id == user_id).count()


def get_favorite_staff_list(db: Session, user_id: int, is_favorite: Optional[bool] = None, limit: int = 20,
                            skip: int = 0):
    if is_favorite is not None:
        return db.query(models.FavoriteStaffOfUser).filter(models.FavoriteStaffOfUser.user_id == user_id,
                                                           models.FavoriteStaffOfUser.is_favorite == is_favorite).limit(
            limit).offset(skip).all()
    else:
        return db.query(models.FavoriteStaffOfUser).filter(models.FavoriteStaffOfUser.user_id == user_id).limit(
            limit).offset(skip).all()


def get_staff_list_info(db: Session, staff_list_id: List):
    staff_list = jsonable_encoder(db.query(models.Staff.id,
                                           models.Staff.fullname,
                                           models.Staff.phone,
                                           models.Staff.address,
                                           models.Staff.district_code,
                                           models.Staff.province_code,
                                           models.Staff.avatar_img,
                                           models.Staff.join_from_date,
                                           models.Staff.working_count,
                                           models.Staff.vote_count,
                                           models.Staff.vote_average_score).filter(
        models.Staff.id.in_(staff_list_id)).all())

    for staff in staff_list:
        district_code = staff['district_code']
        province_code = staff['province_code']
        district_fullname = db.query(models.LocationDistrict.fullname).filter(
            models.LocationDistrict.code == district_code).first()
        province_fullname = db.query(models.LocationProvince.fullname).filter(
            models.LocationProvince.code == province_code).first()
        staff['address'] = staff['address'] + ", " + district_fullname.fullname + ", " + province_fullname.fullname
        staff.pop('district_code')
        staff.pop('province_code')
    return staff_list


def set_favorite_staff(db: Session, data: dict):
    current_favorite_staff = db.query(models.FavoriteStaffOfUser).filter(
        models.FavoriteStaffOfUser.user_id == data['user_id'],
        models.FavoriteStaffOfUser.staff_id == data['staff_id']).first()
    if current_favorite_staff is None:
        db_favorite_staff = models.FavoriteStaffOfUser(**data)
        db.add(db_favorite_staff)
        db.commit()
        db.refresh(db_favorite_staff)
        return db_favorite_staff
    else:
        for key, value in data.items():
            setattr(current_favorite_staff, key, value)
        current_favorite_staff.updated_at = datetime.now()
        db.commit()
        db.refresh(current_favorite_staff)
        return current_favorite_staff


def check_staff_in_favorite_staff_list(db: Session, user_id: int, staff_id: int):
    # Check staff is already in favorite staff list
    # if not, pass
    # if yes, delete it from favorite staff list
    checking = db.query(models.FavoriteStaffOfUser).filter_by(user_id=user_id, staff_id=staff_id).first()
    if checking is None:
        pass
    else:
        db.query(models.FavoriteStaffOfUser).filter_by(user_id=user_id, staff_id=staff_id).delete()
        db.commit()
        db.refresh(checking)


def get_user_device_info(db: Session, user_id: int, device_info: Optional[str] = None):
    if device_info:
        return db.query(models.UserDevices).filter(models.UserDevices.user_id == user_id,
                                                   models.UserDevices.device_info == device_info).all()
    return db.query(models.UserDevices).filter(models.UserDevices.user_id == user_id).all()


def get_user_device_info_by_token(db: Session, user_id: int, device_info: str, token: str):
    return db.query(models.UserDevices).filter(models.UserDevices.user_id == user_id,
                                               models.UserDevices.device_info == device_info,
                                               models.UserDevices.FCM_token == token).first()


def update_user_device_info(db: Session, user_id: int, device_info: any):
    info = device_info.device_info

    current_device = db.query(models.UserDevices).filter(models.UserDevices.user_id == user_id,
                                                         models.UserDevices.device_info == info).first()

    if current_device is None:
        db_device = models.UserDevices(user_id=user_id, is_active=True, **device_info.dict())
        db.add(db_device)
        db.commit()
        db.refresh(db_device)
        return db_device

    else:
        current_device.FCM_token = device_info.FCM_token
        current_device.updated_at = datetime.now()
        db.commit()
        db.refresh(current_device)
        return current_device


def get_total_accumulated_points(db: Session, user_id: int):
    current_user = db.query(models.User).filter(models.User.id == user_id).first()
    return current_user


def update_user_avatar(db: Session, user_id: int, avatar: str):
    current_user = db.query(models.User).filter(models.User.id == user_id).first()

    if current_user is not None:
        current_user.avatar = avatar
        db.commit()
        db.refresh(current_user)
        return current_user
    else:
        return None


def add_banned_staff(db: Session, staff_id: int, user_id: int):
    #     Check if staff is already banned
    checking = db.query(models.StaffBannedByUser).filter(models.StaffBannedByUser.staff_id == staff_id,
                                                         models.StaffBannedByUser.user_id == user_id).first()
    if checking is None:
        db_banned_staff = models.StaffBannedByUser(staff_id=staff_id, user_id=user_id)
        db.add(db_banned_staff)
        db.commit()
        db.refresh(db_banned_staff)
        return "success"
    else:
        return None


def remove_banned_staff(db: Session, staff_id: int, user_id: int):
    # Checking staff not in banned list
    checking = db.query(models.StaffBannedByUser).filter(models.StaffBannedByUser.staff_id == staff_id,
                                                         models.StaffBannedByUser.user_id == user_id).first()
    if checking is None:
        return None
    else:
        db.query(models.StaffBannedByUser).filter(models.StaffBannedByUser.staff_id == staff_id,
                                                  models.StaffBannedByUser.user_id == user_id).delete()
        db.commit()
        return "success"


def count_staff_banned(db: Session, user_id: int):
    return db.query(models.StaffBannedByUser).filter_by(user_id=user_id).count()


def get_list_staff_banned(db: Session, user_id: int, limit: int = 20, skip: int = 0):
    list_staff_banned_id = db.query(models.StaffBannedByUser.staff_id).filter(
        models.StaffBannedByUser.user_id == user_id).offset(skip).limit(limit).all()
    staff_list_id = list(map(lambda x: x[0], list_staff_banned_id))
    list_staff = db.query(models.Staff).filter(models.Staff.id.in_(staff_list_id)).all()
    return list_staff


def check_favorite_existed(db: Session, user_id: int, data: dict):
    data = {
        **data,
        "user_id": user_id
    }
    query = db.query(models.UserFavorite).filter_by(**data).first()
    return bool(query)


def add_new_favorite(db: Session, user_id: int, data: dict):
    # Check favorite existed
    checking = check_favorite_existed(db, user_id, data)

    if checking is True:
        return None

    try:
        db_favorite = models.UserFavorite(user_id=user_id, **data)
        db.add(db_favorite)
        db.commit()
        db.refresh(db_favorite)
        return "success"
    except Exception as e:
        return "Lỗi: Không thêm được item yêu thích mới!"


def remove_favorite(db: Session, user_id: int, data: dict):
    # Check favorite existed
    checking = check_favorite_existed(db, user_id, data)

    if checking is False:  # If not existed
        return None

    try:
        db.query(models.UserFavorite).filter_by(user_id=user_id, **data).delete()
        db.commit()
        return "success"
    except Exception as e:
        return "Lỗi: Không xóa được item yêu thích này!"


def count_favorite(db: Session, user_id: int, favorite_type: str):
    if favorite_type not in ['product', 'combo', 'store']:
        return None

    if favorite_type == 'product':
        return db.query(models.UserFavorite).filter(models.UserFavorite.user_id == user_id,
                                                    models.UserFavorite.product_id.isnot(None)).count()
    elif favorite_type == 'combo':
        return db.query(models.UserFavorite).filter(models.UserFavorite.user_id == user_id,
                                                    models.UserFavorite.combo_id.isnot(None)).count()
    elif favorite_type == 'store':
        return db.query(models.UserFavorite).filter(models.UserFavorite.user_id == user_id,
                                                    models.UserFavorite.store_id.isnot(None)).count()


def get_list_favorite(db: Session, user_id: int, favor_type: str, limit: int = 20, skip: int = 0):
    if favor_type == 'product':
        list_favor = db.query(models.UserFavorite).filter(models.UserFavorite.user_id == user_id,
                                                          models.UserFavorite.product_id.isnot(None)).order_by(
            desc(models.UserFavorite.created_at)).offset(skip).limit(limit).all()
        id_list = list(map(lambda x: x.product_id, list_favor))

        return db.query(models.Product).filter(models.Product.id.in_(id_list)).all()

    elif favor_type == 'combo':
        list_favor = db.query(models.UserFavorite).filter(models.UserFavorite.user_id == user_id,
                                                          models.UserFavorite.combo_id.isnot(None)).order_by(
            desc(models.UserFavorite.created_at)).offset(skip).limit(limit).all()

        id_list = list(map(lambda x: x.combo_id, list_favor))

        return db.query(models.Combo).filter(models.Combo.id.in_(id_list)).all()

    elif favor_type == 'store':
        list_favor = db.query(models.UserFavorite).filter(models.UserFavorite.user_id == user_id,
                                                          models.UserFavorite.store_id.isnot(None)).order_by(
            desc(models.UserFavorite.created_at)).offset(skip).limit(limit).all()

        id_list = list(map(lambda x: x.store_id, list_favor))

        return db.query(models.Store).filter(models.Store.id.in_(id_list)).all()


def get_point_of_user(db: Session, user_id: int) -> int:
    return db.query(models.User.accumulated_points).filter(models.User.user_id == user_id).first()[0]


def decrease_accumulated_point(db: Session, user_id: int, amount: int):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not user:
        return None
    user.accumulated_points -= amount
    db.commit()
    db.refresh(user)
    return user.accumulated_points
