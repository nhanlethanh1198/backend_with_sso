from typing import Optional

from datetime import datetime

import firebase_admin
from fastapi import HTTPException
from firebase_admin import credentials, db, auth, messaging

from app.logger import AppLog

cred = credentials.Certificate("app/cleangreenvn.json")
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://cleangreenvn-18b02-default-rtdb.asia-southeast1.firebasedatabase.app/'})


# Realtime Database

def create_task(task_id: str, data_create):
    ref = db.reference('/tasks')
    tasks_ref = ref.child(task_id)
    try:
        tasks_ref.set(data_create)
    except Exception as e:
        AppLog('Add Task').info(str(e))


def create_task_realtime(user_id: str, task_id: str, data_create):
    ref = db.reference('/staffs')
    current_user = ref.child(user_id).get()
    if current_user is None:
        # firebase chưa có user_id
        users_ref = ref.child(user_id)
        try:
            users_ref.child('list_task').child(task_id).set(data_create)
        except Exception as e:
            AppLog('add realtime task into user').info(str(e))
    else:
        # firebase đã tồn tại user_id
        snapshot = ref.child(user_id).child('list_task')
        if snapshot.get() is None:
            ref.child(user_id).child('list_task').child(task_id).update(data_create)
        else:
            snapshot.child(task_id).update(data_create)


def update_user_task(task_id: str, staff_accept: dict):
    try:
        ref = db.reference('/tasks')
        snapshot = ref.child(task_id).child('staff_accept')
        if snapshot.get() is None:
            snapshot.child('0').update(staff_accept)
        else:
            staff_accept_list = snapshot.get()
            staff_accept_list.append(staff_accept)
            for idx, val in enumerate(staff_accept_list):
                snapshot.child(str(idx)).update(val)
        return True
    except Exception as e:
        AppLog('Update Task').info(str(e))
        return False


def update_task_status(task_id: str, status: int):
    ref = db.reference('/tasks')
    current_task = ref.child(task_id).get()
    if current_task is None:
        raise HTTPException(status_code=404, detail='Task not found')
    else:
        ref.child(task_id).update({
            'status': status
        })
        return True


def user_cancel_task(task_id: str, user_id: str):
    try:
        ref = db.reference('/tasks')
        current_task = ref.child(task_id).get()
        if current_task is None:
            raise HTTPException(status_code=404, detail='Task not found')
        elif current_task['user_id'] != user_id:
            raise HTTPException(status_code=403, detail='You are not allowed to access this task')
        else:
            ref.child(task_id).update({
                'status': 5
            })
            return True
    except Exception as e:
        AppLog('Update Task').info(str(e))
        return False


def get_staff_accept_list(task_id: str, user_id: str):
    ref = db.reference('/tasks')
    current_task = ref.child(task_id).get()
    if current_task is None:
        raise HTTPException(status_code=404, detail='Task not found')
    elif current_task['user_id'] != user_id:
        raise HTTPException(status_code=403, detail='You are not allowed to access this task')
    else:
        try:
            staff_accept_list = current_task['staff_accept']
            return staff_accept_list
        except Exception as e:
            print(str(e))
            return []


def verify_token(id_token):
    try:
        decoded_token = auth.verify_id_token(id_token=id_token, app=None, check_revoked=True)
        uid = decoded_token['uid']
        return uid
    except Exception as e:
        return False


# FCM

def send_notification_multicast(tokens, data):
    try:
        message = messaging.MulticastMessage(
            data=data,
            tokens=tokens
        )
        messaging.send_multicast(message)
        return True
    except Exception as e:
        AppLog('Send Notification').info(str(e))
        return False


def send_notification_single(token, data):
    try:
        notification = messaging.Notification(
            title="Test Notification",
            body="This is a test notification",
            image='https://image.shutterstock.com/image-vector/combo-offer-banner-design-on-260nw-1546693094.jpg'
        )

        message = messaging.Message(
            notification=notification,
            token=token
        )
        result = messaging.send(message)
        return result
    except Exception as e:
        AppLog('Send Notification').info(str(e))
        print(e)
        return False


def send_all_notification(data: dict):
    try:
        message1 = messaging.Message(
            data=data,
            topic='all'
        )
        messages = [message1]
        result = messaging.send_all(messages=messages, dry_run=False)
        return result
    except Exception as e:
        AppLog('Send Notification').info(str(e))
        print(e)
        return False


# Firebase cloud message
async def notify_single_device(token: str, title: str, body: any, image: str, device_type: Optional[str] = None):
    try:
        notification = messaging.Notification(title=title, body=body, image=image)
        android_config = None
        # if device_type == 'android':
        #     # See documentation: https://firebase.google.com/docs/reference/fcm/rest/v1/projects.messages#androidnotification
        #     notification = messaging.AndroidNotification(
        #         title=title,
        #         body=body,
        #         image="https://www.motivation.africa/wp-content/uploads/2021/08/remote-working-in-Africa.jpg",
        #         default_sound=True,
        #     )
        #     # See documentation: https://firebase.google.com/docs/reference/fcm/rest/v1/projects.messages#androidconfig
        #     android_config = messaging.AndroidConfig(ttl=3600, priority='normal', notification=notification)
        message = messaging.Message(notification=notification, android=android_config, token=token)
        return messaging.send(message)
    except Exception as e:
        AppLog('notify_single_device').info(str(e))
        return False


async def notify_multiple_devices(tokens, title, body):
    try:
        message = messaging.MulticastMessage(
            notification=messaging.Notification(title=title, body=body),
            tokens=tokens
        )
        response = messaging.send_multicast(message)
        return response
    except Exception as e:
        AppLog('notify_multiple_devices').info(str(e))
        return False


async def notify_multicast_devices(topic, title, body):
    return 1


async def create_notify_on_fb(user_id: int, noti_id: int, data_create):
    ref = db.reference('/notifications')
    current_user = ref.child(user_id).get()
    if current_user is None:
        # firebase chưa có user_id
        users_ref = ref.child(user_id)
        try:
            users_ref.child('list_noti').child(noti_id).set(data_create)
        except Exception as e:
            AppLog('add realtime noti into user').info(str(e))
    else:
        # firebase đã tồn tại user_id
        snapshot = ref.child(user_id).child('list_noti')
        if snapshot.get() is None:
            ref.child(user_id).child('list_noti').child(noti_id).update(data_create)
        else:
            snapshot.child(noti_id).update(data_create)


async def read_notify_on_fb(user_id: str, noti_id: str, is_read: bool):
    ref = db.reference('/notifications')
    current_user = ref.child(user_id).get()
    if current_user is not None:
        current_noti = ref.child(user_id).child('list_noti').child(noti_id).get()
        if current_noti is not None:
            data_update = {
                **current_noti,
                "is_read": is_read,
                "updated_at": str(datetime.now())
            }
            ref.child(user_id).child('list_noti').child(noti_id).update(data_update)
        else:
            return None
    else:
        return None


async def add_staff_into_task_fb(user_id: str, task_id: str, staff_id: str):
    ref = db.reference('/users')
    current_user = ref.child(user_id).get()
    if current_user is not None:
        current_task = ref.child(user_id).child('tasks').child(task_id).get()
        if current_task is not None:
            current_staff = ref.child(user_id).child('tasks').child(task_id).child('staffs').child(staff_id)
            if current_staff is None:
                json_staff_join = {
                    "staff_id": staff_id,
                    "join_from": str(datetime.now())
                }
                ref.child(user_id).child('tasks').child(task_id).child('staffs').child(staff_id).update(json_staff_join)
                return True
        else:
            json_staff_join = {
                "task_id": staff_id,
                "staffs": {
                    staff_id: {
                        "staff_id": staff_id,
                        "join_from": str(datetime.now())
                    }
                }
            }
            ref.child(user_id).child('tasks').child(task_id).set(json_staff_join)
            return True
    else:
        json_staff_join = {
            "tasks": {
                task_id: {
                    "task_id": task_id,
                    "staffs": {
                        staff_id: {
                            "staff_id": staff_id,
                            "join_from": str(datetime.now())
                        }
                    }
                }
            }
        }
        ref.child(user_id).set(json_staff_join)
        return True
