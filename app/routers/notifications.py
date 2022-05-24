import math
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from app import response_models
from app.backgrounds import cloud_messaging
from app.database import get_db
from app.firebase import send_all_notification, notify_multiple_devices, notify_single_device, read_notify_on_fb
from app.get_current_staff import get_current_staff, CurrentStaff
from app.repositories import notification, users
from app.upload_file_to_s3 import S3

from app.schemas import notification_schemas

from app.get_current_user import get_current_user, CurrentUser

from app.backgrounds.notifications import send_notify_by_user_id

router = APIRouter(
    prefix="/notification",
    tags=["notification"],
    responses={404: {"description": "Not found"}},
)


@router.get('/user-get-list-notification')
async def get_list_notification(db: Session = Depends(get_db), limit: Optional[int] = 20, page: Optional[int] = 1,
                                current_user: CurrentUser = Depends(get_current_user)):
    user_id = current_user.user_id

    total_notification = notification.user_count_notification(db=db, user_id=user_id)

    total_page = math.ceil(total_notification / limit)

    skip = (page - 1) * limit

    results = notification.user_get_list_notification(db=db, user_id=user_id, limit=limit, skip=skip)

    prev_page = page - 1
    if prev_page <= 0:
        prev_page = None

    next_page = page + 1
    if next_page > total_page:
        next_page = None

    return {
        "detail": "Success",
        "data": results,
        "total_notifications": total_notification,
        "limit": limit,
        "prev_page": prev_page,
        "next_page": next_page,
        "current_page": page,
        "total_page": total_page
    }


@router.get('/system', summary="Get system notification", response_model=response_models.SystemNotificationListResponse)
async def get_system_notification(db: Session = Depends(get_db), limit: Optional[int] = 10, page: Optional[int] = 1):
    count_notification = notification.count_system_notification(db)
    total_page = math.ceil(count_notification / limit)
    skip = (page - 1) * limit
    notification_list = notification.get_list_system_notification(db=db, limit=limit, skip=skip)

    prev_page = page - 1
    if prev_page <= 0:
        prev_page = None

    next_page = page + 1
    if next_page > total_page:
        next_page = None

    return {
        "detail": "Success",
        "data": notification_list,
        "total_notifications": count_notification,
        "limit": limit,
        "prev_page": prev_page,
        "next_page": next_page,
        "current_page": page,
        "total_page": total_page
    }


@router.post('/system', summary="Create new system notification")
async def add_new_system_notification(
        background_tasks: BackgroundTasks,
        data: notification_schemas.CreateSystemNotification = Depends(
            notification_schemas.CreateSystemNotification.as_form),
        db: Session = Depends(get_db), current_staff: CurrentStaff = Depends(get_current_staff)):
    role = current_staff.role

    if role != "admin":
        raise HTTPException(status_code=403, detail="You are not allowed to do this action")

    else:
        staff_id = current_staff.staff_id

        if data.image is not None:
            s3 = S3()
            part_file = 'system_notification/{}'.format(data.image.filename)
            url_img = s3.upload_file_to_s3(data.image, part_file)
            data.image = url_img

        db_notification = {
            **data.dict(),
            "staff_id": staff_id,
            "created_at": datetime.now(),
        }

        result = notification.create_system_notification(db=db, notification=db_notification)

        if result is None:
            raise HTTPException(status_code=400, detail="Cannot create new system notification")
        else:
            # Backgroud Task
            background_tasks.add_task(cloud_messaging.push_new_system_notification, data=result)

        return {
            "detail": "Success",
            "data": result
        }


@router.get('/system/{notification_id}', summary="Get system notification by id",
            response_model=response_models.SystemNotificationResponse)
async def get_notification_by_id(notification_id: int, db: Session = Depends(get_db)):
    result = notification.get_system_notification_by_id(db=db, notification_id=notification_id)

    if result is None:
        raise HTTPException(status_code=403, detail="Not found notification or this was removed!")

    return {
        "detail": "Success",
        "data": result
    }


@router.get('/test/system')
async def send_test_notification():
    data = {
        "title": "Test Notification",
        "body": "This is test notification",
    }

    result = send_all_notification(data)

    return result


@router.post('/fcm1/test')
async def fcm_test(data: notification_schemas.FCMtest1):
    title = data.title
    body = data.body
    tokens = data.tokens
    response = await notify_multiple_devices(title, body, tokens)
    return {
        "detail": "gửi tin nhắn thành công",
        "title": title,
        "body": body,
        "tokens": tokens,
        "response": response
    }


@router.post('/fcm2/test')
async def fcm_test(data: notification_schemas.FCMtest2):
    title = data.title
    body = data.body
    token = data.token
    response = await notify_single_device(title, body, token)
    return {
        "detail": "gửi tin nhắn thành công",
        "title": title,
        "body": body,
        "token": token,
        "response": response
    }


@router.post('/fcm/test/{user_id}')
async def fcm_test(user_id: int, device_info: Optional[str] = 'all', db: Session = Depends(get_db)):
    if device_info == 'all':
        device_info = None
    fcm_user = users.get_user_device_info(db=db, user_id=user_id, device_info=device_info)
    if len(list(fcm_user)) == 0:
        raise HTTPException(status_code=403, detail="Không tìm thấy thiết bị của User này")
    title = "Test Single Notification by Nhàn bự :3"
    body = "This is test notification"
    image = "https://png.pngtree.com/background/20210709/original/pngtree-creative-simple-background-wall-picture-image_371930.jpg"
    result_response = []
    for device in fcm_user:
        response = await notify_single_device(title=title, body=body, token=device.FCM_token,
                                              device_type=device.device_info)
        if not response:
            # raise HTTPException(status_code=403, detail="Cannot send notification to user")
            result_response.append({
                "detail": "Cannot send notification to user",
                "device_id": device.id,
                "device_info": device.device_info,
                "token": device.FCM_token,
            })
        else:
            result_response.append({
                "count": len(result_response) + 1,
                "response": response
            })
    return result_response


@router.post('/fcm/test/by_phone/{user_phone}')
async def fcm_test(user_phone: str, device_info: Optional[str] = 'all', db: Session = Depends(get_db)):
    current_user = users.get_user_by_phone(db=db, phone=user_phone)
    if current_user is None:
        raise HTTPException(status_code=403, detail="Không tìm thấy User này")
    user_id = current_user.id

    if device_info == 'all':
        device_info = None
    fcm_user = users.get_user_device_info(db=db, user_id=user_id, device_info=device_info)
    if len(list(fcm_user)) == 0:
        raise HTTPException(status_code=403, detail="Không tìm thấy thiết bị của User này")
    title = "Test Single Notification by Nhàn bự :3"
    body = "This is test notification"
    image = "https://png.pngtree.com/background/20210709/original/pngtree-creative-simple-background-wall-picture-image_371930.jpg"
    result_response = []
    for device in fcm_user:
        response = await notify_single_device(title=title, body=body, token=device.FCM_token,
                                              device_type=device.device_info)
        if not response:
            # raise HTTPException(status_code=403, detail="Cannot send notification to user")
            result_response.append({
                "detail": "Cannot send notification to user",
                "device_id": device.id,
                "device_info": device.device_info,
                "token": device.FCM_token,
            })
        else:
            result_response.append({
                "count": len(result_response) + 1,
                "response": response
            })
    return result_response


@router.post('/fcm/test')
async def test_fcm(background_tasks: BackgroundTasks, db: Session = Depends(get_db),
                   current_user: CurrentUser = Depends(get_current_user)):
    user_id = current_user.user_id
    task_id = "tasktest"
    created_at = "ngay test"
    data_notify = {
        "title": "Thông báo giúp việc",
        "body": 'Quý khách tạo yêu cầu giúp việc ca lẻ {} thành công vào lúc {}'.format(task_id, created_at),
        "image": "http://tiing-storage.s3.amazonaws.com/product/315870/a315870_986861"
    }
    background_tasks.add_task(send_notify_by_user_id, db=db, user_id=user_id, data_notify=data_notify)
    return True


@router.post('/read-notification/{noti_id}')
async def read_notification(noti_id: int, db: Session = Depends(get_db),
                            current_user: CurrentUser = Depends(get_current_user)):
    user_id = current_user.user_id

    # update on firebase
    await read_notify_on_fb(user_id=str(user_id), noti_id=str(noti_id), is_read=True)

    # update on database
    result = notification.user_update_notification(db=db, noti_id=noti_id, user_id=user_id, is_read=True)
    return {
        "detail": "Success",
        "data": result
    }
