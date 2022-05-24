from fastapi import Depends

from app.repositories import users, staffs

from app.database import get_db

from sqlalchemy.orm import Session

from fastapi.encoders import jsonable_encoder

from app import firebase

from app.logger import AppLog

from app.repositories import tasks


def invite_staff_join_job(db, current_task):
    # step 1: lấy danh sách nhân viên
    # lấy danh sách nhân viên yêu thích

    list_staff_id = []

    if current_task.is_choice_staff_favorite is True:

        user_id = current_task.user_id

        favorite_staff_list = jsonable_encoder(users.get_favorite_staff_list(db=db, user_id=user_id, is_favorite=True))

        list_staff_id = list(map(lambda x: x['staff_id'], favorite_staff_list))

    else:

        # lấy danh sách nhân viên theo đánh giá star
        list_staff_id = staffs.get_list_staff_with_high_star(db=db)

    # step 2: kiểm tra xem nhân viên có trống lịch hay không
    # lấy danh sách id nhân viên có trống lịch
    staff_list_id_not_busy = tasks.check_staff_list_is_not_busy(db=db, staff_list_id=list_staff_id,
                                                                start_time=current_task.start_time,
                                                                end_time=current_task.end_time)

    # staff_list_info = jsonable_encoder(users.get_staff_list_info(db=db, staff_list_id=staff_list_id_not_busy))

    start_time = current_task.start_time.strftime("%Y-%m-%d %H:%M:%S")
    end_time = current_task.end_time.strftime("%Y-%m-%d %H:%M:%S")

    for e_id_staff in staff_list_id_not_busy:

        # step 3: gửi công việc lên firebase
        current_task = jsonable_encoder(current_task)

        data_send_firebase = {
            **current_task,
            "start_time": start_time,
            "end_time": end_time
        }

        if current_task['type_task'] == 'fixed_shift':
            message = 'create_fixed_shift_send_firebase send to user_id: {}'.format(e_id_staff)
            AppLog(message).info(str(data_send_firebase))
        else:
            message = 'create_odd_shift_send_firebase send to user_id: {}'.format(e_id_staff)
            AppLog(message).info(str(data_send_firebase))

        firebase.create_task_realtime(user_id=str(e_id_staff), task_id=str(current_task['task_id']), data_create=data_send_firebase)


def update_task_status(task_id: int, status: int):
    firebase.update_task_status(task_id=str(task_id), status=status)
