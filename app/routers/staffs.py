import hashlib
import os
from datetime import datetime, timedelta, date
from typing import Optional

import jwt
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas import staff_schemas
from app import response_models
from app.database import get_db
from app.get_current_staff import get_current_staff, CurrentStaff
from app.get_current_user import get_current_user, CurrentUser
from app.repositories import staffs
from app.upload_file_to_s3 import S3

router = APIRouter(
    prefix="/staffs",
    tags=["staffs"],
    responses={404: {"description": "Not found"}},
)


@router.post("/staff-login/")
async def staff_login(data: staff_schemas.LoginStaff, db: Session = Depends(get_db)):
    phone = data.phone
    password = data.password
    hash_password = hashlib.md5(password.encode('utf-8')).hexdigest()
    staff = staffs.staff_login(db=db, phone=phone, hash_password=hash_password)
    if not staff:
        raise HTTPException(
            status_code=401, detail="Incorrect phone or password")
    else:
        payload = {
            "staff_id": staff.id,
            "role": staff.role,
            "phone": staff.phone,
            "fullname": staff.fullname,
            "email": staff.email,
            "address": staff.address,
            "exp": datetime.utcnow() + timedelta(minutes=10080)
        }

        store_id = None
        if staff.item_store is not None:
            store_id = staff.item_store.id

        HASH_KEY = os.getenv('HASH_KEY')
        encoded_jwt = jwt.encode(payload, HASH_KEY, algorithm="HS256")
        return {
            "detail": "success",
            "access_token": encoded_jwt,
            "token_type": "Bearer",
            "store_id": store_id,
            "role": staff.role,
            "staff_info": {
                "staff_id": staff.id,
                "phone": staff.phone,
                "fullname": staff.fullname,
                "email": staff.email,
                "address": staff.address,
            }
        }


@router.get("/check-login", summary="Staff check login to system", description="""
Staff check token login to system
if token is valid, return True,
if token is invalid, return False with status 401
""")
async def check_staff_login(current_staff: CurrentStaff = Depends(get_current_staff)):
    # Feature: if inValid token, send refresh token to client (comming soon...)
    return {
        "detail": "success",
        "data": True
    }


# tạo nhân viên

def caculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


@router.post("/add-staff/", response_model=staff_schemas.StaffResponse)
async def add_staff(form: staff_schemas.CreateStaff = Depends(staff_schemas.CreateStaff.as_form), db: Session = Depends(get_db),
                    current_staff: CurrentStaff = Depends(get_current_staff)):
    current_role = current_staff.role
    roles = ['admin', 'owner']
    if current_role not in roles:
        raise HTTPException(status_code=403, detail="not authorization")

    staff = staffs.get_staff_by_phone(db=db, phone=form.phone)
    if staff is not None:
        raise HTTPException(status_code=400, detail="staff exist")

    s3 = S3()
    file_path_avatar_img = '{}/{}'.format(form.phone, form.avatar_img.filename)
    file_path_id_card_img_1 = '{}/{}'.format(form.phone, form.id_card_img_1.filename)
    file_path_id_card_img_2 = '{}/{}'.format(form.phone, form.id_card_img_2.filename)
    url_avatar = s3.upload_file_to_s3(form.avatar_img, file_path_avatar_img)
    url_id_card_img_1 = s3.upload_file_to_s3(
        form.id_card_img_1, file_path_id_card_img_1)
    url_id_card_img_2 = s3.upload_file_to_s3(
        form.id_card_img_2, file_path_id_card_img_2)

    hash_password = hashlib.md5(form.password.encode('utf-8')).hexdigest()

    data = {
        **form.dict(),
        "age": caculate_age(form.dob),
        "hash_password": hash_password,
        "avatar_img": url_avatar,
        "id_card_img_1": url_id_card_img_1,
        "id_card_img_2": url_id_card_img_2,
    }

    new_staff = staffs.add_staff(db=db, data=data)

    return {
        "detail": "success",
        "data": new_staff
    }


# cập nhật nhân viên
@router.put("/update-staff-info/{staff_id}", response_model=staff_schemas.StaffResponse)
async def update_staff_info(staff_id: int, form: staff_schemas.UpdateStaff = Depends(staff_schemas.UpdateStaff.as_form),
                            db: Session = Depends(get_db), current_staff: CurrentStaff = Depends(get_current_staff)):
    current_role = current_staff.role
    roles = ['admin', 'owner']
    if current_role not in roles:
        raise HTTPException(status_code=403, detail="not authorization")

    staff = staffs.get_staff_info(db=db, staff_id=staff_id)
    if staff is None:
        raise HTTPException(status_code=404, detail="Staff not exist")
    else:
        data = {**form.dict(), "age": caculate_age(form.dob)}
        s3 = S3()
        if form.avatar_img is not None:
            file_path_avatar_img = '{}/{}'.format(
                staff.phone, form.avatar_img.filename)
            url_avatar = s3.upload_file_to_s3(form.avatar_img, file_path_avatar_img)
            data['avatar_img'] = url_avatar

        if form.id_card_img_1 is not None:
            file_path_id_card_img_1 = '{}/{}'.format(
                staff.phone, form.id_card_img_1.filename)
            url_id_card_img_1 = s3.upload_file_to_s3(
                form.id_card_img_1, file_path_id_card_img_1)
            data['id_card_img_1'] = url_id_card_img_1

        if form.id_card_img_2 is not None:
            file_path_id_card_img_2 = '{}/{}'.format(
                staff.phone, form.id_card_img_2.filename)
            url_id_card_img_2 = s3.upload_file_to_s3(
                form.id_card_img_2, file_path_id_card_img_2)
            data['id_card_img_2'] = url_id_card_img_2

        if form.password is not None:
            hash_password = hashlib.md5(form.password.encode('utf-8')).hexdigest()
            data['hash_password'] = hash_password

        edit_staff = staffs.update_staff_info(db=db, staff_id=staff_id, data=data)

        return {
            "detail": "success",
            "data": edit_staff
        }


# Staff Location


@router.get('/locations', summary="Staff get Location")
async def staff_get_locations(db: Session = Depends(get_db), current_staff: CurrentStaff = Depends(get_current_staff)):
    staff_id = current_staff.staff_id
    locations = staffs.staff_get_locations(db=db, staff_id=staff_id)
    return locations


@router.post('/locations', summary='Staff add new Location')
async def staff_create_location(db: Session = Depends(get_db),
                                current_staff: CurrentStaff = Depends(get_current_staff)):
    return None


# khoá nhân viên


@router.put("/lock-unlock-staff/{staff_id}", response_model=staff_schemas.StaffResponse)
async def lock_staff(staff_id: int, data: staff_schemas.LockStaff, db: Session = Depends(get_db),
                     current_staff: CurrentStaff = Depends(get_current_staff)):
    current_role = current_staff.role
    roles = ['admin', 'owner']
    if current_role not in roles:
        raise HTTPException(status_code=403, detail="not authorization")

    staff = staffs.get_staff_info(db=db, staff_id=staff_id)
    if staff == None:
        raise HTTPException(status_code=404, detail="Staff not exist")
    else:
        staff.is_active = data.is_active
        db.commit()
        db.refresh(staff)
    return {
        "detail": "success",
        "data": staff
    }


@router.get("/user-get-staff-info/{staff_id}", response_model=staff_schemas.UserGetStaffResponse)
async def user_get_staff_info(staff_id: int, db: Session = Depends(get_db)):
    staff = staffs.get_staff_info(db=db, staff_id=staff_id)
    return {
        "detail": "success",
        "data": staff
    }


@router.get("/get-staff-info", response_model=staff_schemas.StaffResponse)
async def get_staff_info(db: Session = Depends(get_db), current_staff: CurrentStaff = Depends(get_current_staff)):
    staff = staffs.get_staff_info(db=db, staff_id=current_staff.staff_id)
    return {
        "detail": "success",
        "data": staff
    }


@router.get("/get-staff/{staff_id}", response_model=staff_schemas.StaffResponse)
async def get_staff(staff_id: int, db: Session = Depends(get_db),
                    current_staff: CurrentStaff = Depends(get_current_staff)):
    staff = staffs.get_staff_info(db=db, staff_id=staff_id)
    return {
        "detail": "success",
        "data": staff
    }


@router.get("/get-list-staff", response_model=staff_schemas.ListStaffResponse)
async def get_staff_info(db: Session = Depends(get_db), current_staff: CurrentStaff = Depends(get_current_staff)):
    results = staffs.get_staff_list(db=db)
    return {
        "detail": "success",
        "data": results
    }


@router.get('/user-get-list-staff', response_model=response_models.UserGetStaffList,
            description="User get List Staff is being active, and role is 'staff'")
async def user_get_list_staff(limit: Optional[int] = 20, db: Session = Depends(get_db),
                              current_user: CurrentUser = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(
            status_code=401, detail="You are not authorized to access this resource")
    else:
        results = staffs.user_get_staff_list(db=db, limit=limit)
        return {
            "detail": "success",
            "data": results
        }


# Staff Vote
@router.post('/vote/{staff_id}', tags=['Staff Vote'], description='Add Staff Vote By User',
             response_model=response_models.AddStaffVote)
async def add_staff_vote(staff_id: int, vote: staff_schemas.VoteStaff, db: Session = Depends(get_db),
                         current_user: CurrentUser = Depends(get_current_user)):
    user_id = current_user.user_id
    result = staffs.add_staff_vote(
        db=db, staff_id=staff_id, vote=vote, user_id=user_id)
    return result


@router.get('/vote/{staff_id}/vote-list', tags=['Staff Vote'], description='Get List vote of Staff'
    , response_model=response_models.StaffVoteInfoResponse)
async def get_list_vote_of_staff(staff_id: int, db: Session = Depends(get_db)):
    result = staffs.get_list_vote_of_staff(db=db, staff_id=staff_id)
    return {
        "detail": "success",
        "data": result
    }


@router.get('/vote/vote-info/{vote_id}', tags=['Staff Vote'], description='Get Vote Info',
            response_model=response_models.ElementInVoteStaffList)
async def get_vote_info_by_id(vote_id: int, db: Session = Depends(get_db)):
    result = staffs.get_vote_info_by_id(db=db, vote_id=vote_id)
    return


@router.put('/vote/{vote_id}', tags=['Staff Vote'], description='Update Vote Info',
            response_model=response_models.AddStaffVote)
async def update_vote_info(vote_id: int, vote: staff_schemas.UpdateVoteStaff, db: Session = Depends(get_db),
                           current_user=Depends(get_current_user)):
    user_id = current_user.user_id
    result = staffs.update_vote_info(
        db=db, vote_id=vote_id, user_id=user_id, vote=vote)
    return result


@router.get('/vote/{staff_id}/check', tags=['Staff Vote'], description='Check Staff is worked with user successful?')
async def check_user_worked(staff_id: int, db: Session = Depends(get_db),
                            current_user: CurrentUser = Depends(get_current_user)):
    return {
        "staff_id": staff_id,
        "user_id": current_user.user_id,
        "message": "Chưa có api cập nhật trạng thái staff đã hoàn thành công việc nên chưa làm được :)))))"
    }


@router.post("/user-get-list-staff-in-task", response_model=staff_schemas.ListStaffResponse)
async def get_list_staff_in_task(data: staff_schemas.ListStaffId,
                                 db: Session = Depends(get_db),
                                 current_user: CurrentUser = Depends(get_current_user)):
    user_id = current_user.user_id
    list_staff_id = data.list_staff_id
    results = staffs.get_list_staff_by_list_id(db=db, list_staff_id=list_staff_id)
    return {
        "detail": "success",
        "data": results
    }
