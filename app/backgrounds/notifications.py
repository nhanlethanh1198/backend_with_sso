from typing import Optional

from datetime import datetime

from fastapi.encoders import jsonable_encoder

from app.firebase import notify_single_device

from app.repositories import users, notification

from app.logger import AppLog

from app.firebase import create_notify_on_fb


async def send_notify_by_user_id(db, user_id: int, data_notify: any, device_info: Optional[str] = 'all'):
    if device_info == 'all':
        device_info = None
    fcm_user = users.get_user_device_info(db=db, user_id=user_id, device_info=device_info)
    if len(list(fcm_user)) == 0:
        return {
            "detail": "Cannot find any device"
        }

    result_response = []
    for device in fcm_user:
        response = await notify_single_device(token=device.FCM_token, title=data_notify['title'],
                                              body=data_notify['body'], image=data_notify['image'],
                                              device_type=device.device_info)
        if not response:
            result_response.append({
                "detail": "Cannot send notification to user",
                "device_id": device.id,
                "device_info": device.device_info,
                "token": device.FCM_token,
            })
        else:
            result_response.append({
                "count": len(result_response) + 1,
                "response": response,
                "device_id": device.id,
                "device_info": device.device_info,
                "token": device.FCM_token,
            })

    AppLog('send notify').info(result_response)
    return result_response


async def create_notify_on_firebase(db, user_id: int, data: dict):
    dict_data = {
        **data,
        "user_id": user_id,
        "image": "https://tiing-storage.s3.ap-southeast-1.amazonaws.com/icons/icon_notifi.png",
        "is_read": False,
        "created_at": str(datetime.now()),
        "updated_at": str(datetime.now())
    }
    result = notification.create_notification(db=db, data=dict_data)
    await create_notify_on_fb(user_id=str(user_id), noti_id=str(result.id), data_create=dict_data)
    return result
