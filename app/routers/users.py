import enum
import hashlib
import math
import os
from datetime import datetime, timedelta
from typing import Optional

import jwt
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.schemas import user_schemas, location_schemas, staff_schemas

from app import models, dependencies, response_models
from app.backgrounds import users as users_background
from app.database import get_db
from app.get_current_staff import get_current_staff, CurrentStaff
from app.get_current_user import get_current_user, CurrentUser
from app.repositories import users, tasks, locations
from app.upload_file_to_s3 import S3
from docs import user as user_docs

load_dotenv()

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post('/login', description='User login with phone number and password',
             response_model=response_models.UserLoginInfoResponse)
async def user_login(request: user_schemas.UserLoginWithPhoneNumberAndPassword, db: Session = Depends(get_db)):
    user_phone = request.phone
    user_password = request.password

    phone_validate = await dependencies.validate_phone_number(user_phone)
    if phone_validate is False:
        raise HTTPException(status_code=400, detail="phone number invalid")

    # check user not exist
    current_user = users.get_user_by_phone(db, user_phone)
    if current_user is None:
        raise HTTPException(status_code=401, detail="Tài khoản không tồn tại!")

    # Hash password and compare with database
    hashed_password = hashlib.sha256(user_password.encode()).hexdigest()

    check_user_password = users.check_password_of_user(db=db, phone=user_phone, hashed_password=hashed_password)

    if not check_user_password:
        raise HTTPException(status_code=401, detail="Sai tài khoản hoặc mật khẩu!")

    else:
        # return token
        payload_of_token = {
            "user_id": check_user_password.id,
            "fullname": check_user_password.fullname,
            "phone": check_user_password.phone,
            "email": check_user_password.email,
            "address": check_user_password.address,
            "exp": datetime.utcnow() + timedelta(minutes=43200)
        }
        HASH_KEY = os.getenv('HASH_KEY')
        encoded_jwt = jwt.encode(payload_of_token, HASH_KEY, algorithm="HS256")
        current_location = locations.get_current_location(db=db, user_id=payload_of_token['user_id'])
        return {
            "detail": "success",
            "access_token": encoded_jwt,
            "token_type": "Bearer",
            "is_update_user_info": False if payload_of_token['address'] != None else True,
            "user_info": {
                "user_id": payload_of_token['user_id'],
                "fullname": payload_of_token['fullname'],
                "phone": payload_of_token['phone'],
                "email": payload_of_token['email'],
                "address": payload_of_token['address'],
                "title_address": current_location.title_location if current_location else None,
                "location_id": current_location.id if current_location else None
            }
        }


@router.post('/check-user-exist', description="Check User Exist", response_model=response_models.CheckUserExist)
async def check_user_existed(request: user_schemas.CheckUserExist, db: Session = Depends(get_db)):
    phone = request.phone
    if await dependencies.validate_phone_number(phone) == False:
        raise HTTPException(status_code=400, detail="phone number invalid")
    else:
        user = users.get_user_by_phone(db, phone)
        if user is None:
            return {
                "detail": "success",
                "is_exist": False,
                "message": "Tài khoản không tồn tại!"
            }
        else:
            return {
                "detail": "success",
                "is_exist": True,
                "message": "Tài khoản đã tồn tại!"
            }


@router.post('/register', description="User Register new account with password",
             response_model=response_models.UserLoginInfoResponse)
async def user_register(request: user_schemas.RegisterNewUser, db: Session = Depends(get_db)):
    user_phone = request.phone
    user_password = request.password

    phone_validate = await dependencies.validate_phone_number(user_phone)
    if phone_validate is False:
        raise HTTPException(status_code=400, detail="Số điện thoại quý khách nhập không hợp lệ!")

    # check user not exist
    current_user = users.get_user_by_phone(db, user_phone)
    if current_user is not None:
        raise HTTPException(status_code=400, detail="Tài khoản đã tồn tại!")

    # Hash password and compare with database
    hashed_password = hashlib.sha256(user_password.encode()).hexdigest()

    # insert user to database
    payload_of_user = {
        "phone": user_phone,
        "hashed_password": hashed_password,
    }
    new_user = users.create_new_user(db=db, payload_of_user=payload_of_user)

    # return token
    payload_of_token = {
        "user_id": new_user.id,
        "fullname": None,
        "phone": user_phone,
        "email": None,
        "address": None,
        "exp": datetime.utcnow() + timedelta(minutes=43200)
    }

    HASH_KEY = os.getenv('HASH_KEY')
    encoded_jwt = jwt.encode(payload_of_token, HASH_KEY, algorithm="HS256")

    return {
        "detail": "success",
        "access_token": encoded_jwt,
        "token_type": "Bearer",
        "is_update_user_info": True,
        "user_info": {
            "user_id": payload_of_token['user_id'],
            "phone": payload_of_token['phone'],
        }
    }


@router.post('/forgot-password', description="User forgot password",
             response_model=response_models.UserLoginInfoResponse)
async def user_forgot_password(request: user_schemas.ForgotPassword, db: Session = Depends(get_db)):
    user_phone = request.phone
    user_password = request.password

    phone_validate = await dependencies.validate_phone_number(user_phone)
    if phone_validate is False:
        raise HTTPException(status_code=400, detail="Số điện thoại quý khách nhập không hợp lệ!")

    # check user not exist
    current_user = users.get_user_by_phone(db, user_phone)
    if current_user is None:
        raise HTTPException(status_code=400, detail="Tài khoản không tồn tại!")

    # Hash password and compare with database
    hashed_password = hashlib.sha256(user_password.encode()).hexdigest()

    # update password to database
    current_user_update = users.update_password(db=db, user_id=current_user.id, hashed_password=hashed_password)

    # return token
    payload_of_token = {
        "user_id": current_user_update.id,
        "fullname": current_user_update.fullname,
        "phone": current_user_update.phone,
        "email": current_user_update.email,
        "address": current_user_update.address,
        "exp": datetime.utcnow() + timedelta(minutes=43200)
    }

    HASH_KEY = os.getenv('HASH_KEY')
    encoded_jwt = jwt.encode(payload_of_token, HASH_KEY, algorithm="HS256")

    # Get current_location
    user_current_location = locations.get_current_location(db, current_user.id)

    return {
        "detail": "success",
        "access_token": encoded_jwt,
        "token_type": "Bearer",
        "is_update_user_info": False if payload_of_token['address'] != None else True,
        "user_info": {
            "user_id": payload_of_token['user_id'],
            "phone": payload_of_token['phone'],
            "email": payload_of_token['email'],
            "fullname": payload_of_token['fullname'],
            "address": payload_of_token['address'],
            "title_address": user_current_location.title_location if user_current_location else None,
            "location_id": user_current_location.id if user_current_location else None
        }
    }


@router.put("/update-info", description=user_docs.userUpdateDescription)
async def update_info(data: user_schemas.UpdateUser, db: Session = Depends(get_db),
                      current_user: CurrentUser = Depends(get_current_user)):
    email = None
    if hasattr(data, 'email'):
        email = data.email

    dob = None
    if hasattr(data, 'dob'):
        dob = data.dob

    updated_user = users.update_user_info(db=db, user_id=current_user.user_id, fullname=data.fullname,
                                          address=data.address,
                                          dob=dob, email=email)
    if updated_user is None:
        raise HTTPException(status_code=400, detail="Không thể cập nhật thông tin user!")

    payload = {
        "user_id": updated_user.id,
        "fullname": updated_user.fullname,
        "phone": updated_user.phone,
        "email": updated_user.email,
        "address": updated_user.address,
        "exp": datetime.utcnow() + timedelta(minutes=43200)
    }

    HASH_KEY = os.getenv('HASH_KEY')
    encoded_jwt = jwt.encode(payload, HASH_KEY, algorithm="HS256")
    current_location = locations.get_current_location(db=db, user_id=payload['user_id'])

    return {
        "detail": "success",
        "access_token": encoded_jwt,
        "token_type": "Bearer",
        "is_update_user_info": False if payload['address'] is not None else True,
        "user_info": {
            "user_id": payload['user_id'],
            "fullname": payload['fullname'],
            "phone": payload['phone'],
            "email": payload['email'],
            "address": payload['address'],
            "title_address": None if current_location is None else current_location.title_location,
            "location_id": current_location.id if current_location else None
        }
    }


# Update user avatar
@router.post('/update-avatar', description="User cập nhật avatar mới, reponse trả về URL Avatar mới",
             summary='User Update Avatar', response_model=response_models.UserUpdateAvatarResponse)
async def user_update_avatar(request_body: user_schemas.UserAvatar = Depends(user_schemas.UserAvatar.as_form),
                             db: Session = Depends(get_db), current_user: CurrentUser = Depends(get_current_user)):
    user_id = current_user.user_id
    avatar = request_body.avatar

    s3 = S3()
    part_file = "users/avatar/{}/{}".format(user_id, avatar.filename)
    url_avatar_img = s3.upload_file_to_s3(avatar, part_file)

    result = users.update_user_avatar(db=db, user_id=user_id, avatar=url_avatar_img)

    if not result:
        raise HTTPException(status_code=400, detail="Can not update user avatar")

    return {
        "detail": "success",
        "message": "Cập nhật ảnh đại diện thành công!",
        "avatar": result.avatar
    }


@router.post('/logout', description="Logout for user")
async def user_logout(current_user: CurrentUser = Depends(get_current_user)):
    # clean user session
    # clean user device session

    return {
        "detail": "success",
        "message": "Logout success"
    }


@router.get('/get-list-user', description=user_docs.getListUserDescription)
async def get_list_user(phone: Optional[str] = None, limit: Optional[int] = 20, page: Optional[int] = 1,
                        db: Session = Depends(get_db), current_staff: CurrentStaff = Depends(get_current_staff)):
    total_user = users.count_user(db=db, phone=phone)
    total_page = math.ceil(total_user / limit)
    skip = limit * (page - 1)
    results = users.get_list_user(db=db, phone=phone, skip=skip, limit=limit)

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
        "data": results
    }


@router.get("/get-user-info", response_model=response_models.UserInfoResponse)
async def get_user_info(db: Session = Depends(get_db), current_user: CurrentUser = Depends(get_current_user)):
    user = users.get_user_by_id(db, user_id=current_user.user_id)

    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    return {
        "detail": "success",
        "data": user
    }


@router.post("/user-add-location", description=user_docs.userAddLocationDescription)
async def user_add_location(request: location_schemas.AddLocation, db: Session = Depends(get_db),
                            current_user: CurrentUser = Depends(get_current_user)):
    is_active = request.is_active

    if is_active == True:
        locations.update_location(db=db, user_id=current_user.user_id, is_active=False)

    data = {
        "user_id": current_user.user_id,
        **request.dict()
    }

    new_location = locations.add_location(db=db, data=data)

    if is_active is True:
        location = '{}, {}, {}, {}'.format(new_location.address, new_location.district, new_location.city,
                                           new_location.country)
        current_user = users.user_update_location(db=db, user_id=current_user.user_id, location=location)

    return {
        "detail": "success",
        "data": jsonable_encoder(new_location)
    }


@router.put("/user-update-location/{location_id}", description=user_docs.userUpdateLocationDescription)
async def user_update_location(location_id: int, data: location_schemas.AddLocation, db: Session = Depends(get_db),
                               current_user: CurrentUser = Depends(get_current_user)):
    title_location = data.title_location
    type_location = data.type_location
    city = data.city
    country = data.country
    district = data.district
    address = data.address
    is_active = data.is_active
    fullname = data.fullname
    phone = data.phone

    if is_active is True:
        locations.update_location(db=db, user_id=current_user.user_id, is_active=False)

    data_update = {
        "type_location": type_location,
        "title_location": title_location,
        "address": address,
        "district": district,
        "city": city,
        "country": country,
        "is_active": is_active,
        "fullname": fullname,
        "phone": phone
    }

    current_location = locations.upd_location(db=db, user_id=current_user.user_id, location_id=location_id,
                                              data=data_update)

    if is_active is True:
        location = '{}, {}, {}, {}'.format(current_location.address, current_location.district, current_location.city,
                                           current_location.country)
        current_user = users.user_update_location(db=db, user_id=current_user.user_id, location=location)

    return {
        "detail": "success",
        "data": current_location
    }


@router.get("/user-get-list-location", description=user_docs.userGetListLocationDescription)
async def user_get_list_location(db: Session = Depends(get_db), current_user: CurrentUser = Depends(get_current_user)):
    results = locations.get_list_location(db=db, user_id=current_user.user_id)
    return {
        "detail": "success",
        "data": results
    }


@router.put("/lock-user/{user_id}", description=user_docs.lockUserDescription)
async def lock_user(user_id: int, data: user_schemas.LockUser, db: Session = Depends(get_db),
                    current_staff: CurrentStaff = Depends(get_current_staff)):
    current_user = users.lock_user(db, user_id=user_id, is_active=data.is_active)
    return {
        "detail": "success",
        "data": current_user
    }


@router.get("/get-user-by-id/{user_id}", description=user_docs.getUserByIdDescription)
async def get_user_by_id(user_id: int, db: Session = Depends(get_db),
                         current_staff: CurrentStaff = Depends(get_current_staff)):
    current_user = users.get_user_by_id(db, user_id=user_id)
    return {
        "detail": "success",
        "data": current_user
    }


@router.get("/user-get-point", description=user_docs.userGetPointDescription, response_model=response_models.UserPoint)
async def user_get_point(background_tasks: BackgroundTasks, db: Session = Depends(get_db),
                         current_user: CurrentUser = Depends(get_current_user)):
    user_id = current_user.user_id
    current_user = users.get_total_accumulated_points(db=db, user_id=user_id)

    # Background Task to check point
    background_tasks.add_task(users_background.check_point, db=db, user=current_user)

    total_accumulated_points: int = current_user.accumulated_points
    current_user_rank: str = current_user.rank

    return {
        "detail": "success",
        "message": "Điểm tích luỹ hiện tại của bạn là {} điểm".format(total_accumulated_points),
        "notice": "Bạn đang ở mức hạng {}.".format(current_user_rank),
        "current_rank": current_user_rank,
        "current_accumulated_points": total_accumulated_points
    }


@router.get('/favorite-staff', summary="Get Favorite Staff List of User",
            response_model=response_models.FavoriteStaffListResponse)
async def get_favorite_staff_list(limit: int = 10, page: int = 1, db: Session = Depends(get_db),
                                  current_user: CurrentUser = Depends(get_current_user)):
    user_id = current_user.user_id

    count = users.count_favorite_staff_list(db=db, user_id=user_id, is_favorite=True)
    total_page = math.ceil(count / 10)
    skip = limit * (page - 1)
    prev_page = page - 1
    if prev_page <= 0:
        prev_page = None

    next_page = page + 1
    if next_page > total_page:
        next_page = None

    staff_list = jsonable_encoder(
        users.get_favorite_staff_list(db=db, user_id=user_id, is_favorite=True, limit=limit, skip=skip))

    staff_list_id = list(map(lambda x: x['staff_id'], staff_list))

    staff_list_info = jsonable_encoder(users.get_staff_list_info(db=db, staff_list_id=staff_list_id))

    return {
        "detail": "success",
        "data": staff_list_info,
        "count": count,
        "prev_page": prev_page,
        'next_page': next_page,
        'current_page': page,
        'total_page': total_page,
        'limit': limit
    }


@router.post('/favorite-staff', response_model=response_models.FavoriteStaffResponse)
async def user_set_favorite_staff(request: staff_schemas.FavoriteStaff, db: Session = Depends(get_db),
                                  current_user: CurrentUser = Depends(get_current_user)):
    user_id = current_user.user_id

    data = {
        'user_id': user_id,
        **request.dict()
    }
    favorite_staff = users.set_favorite_staff(db, data)
    return favorite_staff


@router.post('/banned-staff', summary="User thêm hoặc xóa nhân viên trong danh sách nhân viên bị chặn",
             response_model=response_models.BannedStaffByUserResponse)
async def user_handle_banned_staff(request: staff_schemas.BannedStaffByUser, db: Session = Depends(get_db),
                                   current_user: CurrentUser = Depends(get_current_user)):
    user_id = current_user.user_id
    banned_staff_id = request.staff_id
    action = request.is_banned

    if action is True:
        # Check staff is already working for this user
        # if not, raise "Staff did not work for this user"
        # else: continue
        checking_staff_is_working = tasks.check_staff_is_working(db=db, user_id=user_id, staff_id=banned_staff_id)
        if checking_staff_is_working is False:
            raise HTTPException(status_code=400, detail="Nhân viên này chưa làm việc cho bạn!")

        # remove if staff in already in favorite list
        users.check_staff_in_favorite_staff_list(db=db, user_id=user_id, staff_id=banned_staff_id)

        # check staff is in banned list
        result = users.add_banned_staff(db, user_id=user_id, staff_id=banned_staff_id)
        if not result:
            raise HTTPException(status_code=400, detail="Nhân viên đã tồn tại trong danh sách bị chặn")
        return {
            "detail": result,
        }
    elif action is False:
        result = users.remove_banned_staff(db, user_id=user_id, staff_id=banned_staff_id)
        if not result:
            raise HTTPException(status_code=400, detail="Nhân viên không tồn tại trong danh sách bị chặn")
        return {
            "detail": result,
        }
    else:
        raise HTTPException(status_code=400, detail="Action không hợp lệ")


@router.get('/banned-staff', summary="Get Banned Staff List of User", status_code=200,
            response_model=response_models.FavoriteStaffListResponse)
async def user_get_list_staff_banned(limit: Optional[int] = 20, page: Optional[int] = 1, db: Session = Depends(get_db),
                                     current_user: CurrentUser = Depends(get_current_user)):
    user_id = current_user.user_id

    total_staff_banned = users.count_staff_banned(db=db, user_id=user_id)
    total_page = math.ceil(total_staff_banned / 20)
    skip = limit * (page - 1)
    prev_page = page - 1
    if prev_page <= 0:
        prev_page = None

    next_page = page + 1
    if next_page > total_page:
        next_page = None

    staff_list = users.get_list_staff_banned(db, user_id=user_id, limit=limit, skip=skip)
    return {
        "detail": "success",
        "data": staff_list,
        "count": total_staff_banned,
        "prev_page": prev_page,
        'next_page': next_page,
        'current_page': page,
        'total_page': total_page,
        'limit': limit
    }


@router.post('/device-info', summary='User Update device info after first login')
async def user_update_device_info(request: user_schemas.UserDeviceInfo, db: Session = Depends(get_db),
                                  current_user: CurrentUser = Depends(get_current_user)) -> models.UserDevices:
    user_id = current_user.user_id
    device_info = users.update_user_device_info(db=db, user_id=user_id, device_info=request)
    return device_info


@router.get('/check-device-info', summary="check user has a token device already or not yet",
            response_model=user_schemas.UserCheckDeviceExistResponse)
async def user_check_device_info(FCM_token: str, device_info: str, db: Session = Depends(get_db),
                                 current_user: CurrentUser = Depends(get_current_user)):
    user_id = current_user.user_id
    device_info = users.get_user_device_info_by_token(db=db, user_id=user_id, device_info=device_info, token=FCM_token)
    if device_info is not None:
        return {
            "detail": "success",
            "has_device_token": True,
            "FCM_token": device_info.FCM_token
        }
    else:
        return {
            "detail": "success",
            "has_device_token": False,
            "FCM_token": None
        }


class FavoriteType(str, enum.Enum):
    product = 'product'
    combo = 'combo'
    store = 'store'


@router.post('/user-favorites/{favorite_type}', summary="User set Favorite Product/Combo/Store", description="""
User set Favorite Product/Combo/Store with Product_id, Combo_id, Store_id

## request (JSON):
- is_add: Bool (True is add new favorite, False is remove favorite)
- product_id: Int (Optional)
- combo_id: Int (Optional)
- store_id: Int (Optional)
""")
async def user_set_favorite(favorite_type: FavoriteType, request: user_schemas.UserFavorite,
                            db: Session = Depends(get_db),
                            current_user: CurrentUser = Depends(get_current_user)):
    user_id = current_user.user_id
    action = request.is_add

    check_favorite_type = {
        "product": {"product_id": request.item_id},
        "combo": {"combo_id": request.item_id},
        "store": {"store_id": request.item_id}
    }

    data = {
        **check_favorite_type.get(favorite_type.value),
    }

    if action is True:
        # Them favorite moi

        result = users.add_new_favorite(db=db, user_id=user_id, data=data)

        if not result:
            raise HTTPException(status_code=400, detail="Đã tồn tại trong danh sách yêu thích!")

        return {
            "detail": result,
        }

    if action is False:

        result = users.remove_favorite(db=db, user_id=user_id, data=data)

        if not result:
            raise HTTPException(status_code=400, detail="Không tồn tại trong danh sách yêu thích!")

        return {
            "detail": result,
        }


@router.get('/user-favorites/{favorite_type}', summary="User get Favorite list of Product/Combo/Store", description="""
User get Favorite Product/Combo/Store""", status_code=200
            # , response_model=response_models.FavoriteListResponse
            )
async def get_list_favorite_items(favorite_type: FavoriteType, limit: Optional[int] = 20, page: Optional[int] = 1,
                                  db: Session = Depends(get_db),
                                  current_user: CurrentUser = Depends(get_current_user)):
    user_id = current_user.user_id
    favor_type = favorite_type.value

    count_favorite = users.count_favorite(db=db, user_id=user_id, favorite_type=favor_type)
    print(count_favorite)
    if not count_favorite:
        raise HTTPException(status_code=404, detail="Không tồn tại danh sách yêu thích!")

    total_page = math.ceil(count_favorite / limit)
    skip = limit * (page - 1)
    prev_page = page - 1
    if prev_page <= 0:
        prev_page = None

    next_page = page + 1
    if next_page > total_page:
        next_page = None

    result = users.get_list_favorite(db=db, user_id=user_id, favor_type=favor_type, limit=limit, skip=skip)

    return {
        "detail": "success",
        "data": result,
        "count": count_favorite,
        "prev_page": prev_page,
        "next_page": next_page,
        "total_page": total_page,
        "limit": limit,
        "current_page": page
    }
