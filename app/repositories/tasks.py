from datetime import datetime, timedelta
from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from app import models

from app import constants

from app.services.tasks import update_task_history_status


def create_odd_shift(db: Session, data: dict):
    start_time = data['start_time'] - timedelta(hours=2)
    end_time = data['end_time']
    user_id = data['user_id']

    check_task = db.query(models.Task).filter(models.Task.user_id == user_id, or_(
        and_(models.Task.start_time >= start_time, models.Task.start_time <= end_time),
        and_(end_time >= models.Task.start_time, end_time <= models.Task.end_time))).first()
    if check_task is not None:
        return False

    else:
        db_task = models.Task(
            **data,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.add(db_task)
        db.commit()
        db_task.task_id = "TCL{:06d}".format(db_task.id)
        db.commit()
        db.refresh(db_task)
        return db_task


def create_fixed_shift(db: Session, data: dict):
    start_time = data['start_time'] - timedelta(hours=1)
    end_time = data['end_time'] + timedelta(hours=1)
    start_date = data['start_date']
    end_date = data['end_date']
    user_id = data['user_id']

    # Check task existing

    current_time = datetime.now()
    time_stamp = current_time.timestamp()

    db_task = models.Task(
        **data,
        created_at=current_time,
        updated_at=current_time
    )
    db.add(db_task)
    db.commit()
    db_task.task_id = "TCD{:06d}".format(db_task.id)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_tasks(db: Session, user_id: int, type_task: Optional[str] = None):
    if type_task is None:
        return db.query(models.Task).filter(models.Task.user_id == user_id).all()
    else:
        return db.query(models.Task).filter(models.Task.user_id == user_id, models.Task.type_task == type_task).all()


def update_task_status(db: Session, task_id: int, status: int,
                       content: Optional[str] = 'Cập nhật trạng thái mới thành công!'):
    db_task = db.query(models.Task).filter_by(id=task_id).first()
    if db_task is not None:
        time = datetime.now()
        str_time = time.strftime("%H:%M:%S, %d/%m/%Y")
        db_task.status = status
        db_task.status_history = db_task.status_history.append({'status': status, 'time': str_time, 'content': content})
        db_task.updated_at = time
        db.commit()
        db.refresh(db_task)
        return db_task
    else:
        return False


def count_task(db: Session, type_task: Optional[str] = None, status: Optional[int] = None):
    if type_task:
        if status:
            return db.query(models.Task).filter(models.Task.type_task == type_task,
                                                models.Task.status == status).count()
        else:
            return db.query(models.Task).filter(models.Task.type_task == type_task).count()
    else:
        if status:
            return db.query(models.Task).filter(models.Task.status == status).count()
        else:
            return db.query(models.Task).count()


def staff_get_list_task(db: Session, type_task: Optional[str] = None, status: Optional[int] = None, limit: int = 20,
                        skip: int = 0):
    if type_task:
        if status:
            return db.query(models.Task).filter(models.Task.type_task == type_task,
                                                models.Task.status == status).order_by(models.Task.created_at).offset(
                skip).limit(limit).all()
        else:
            return db.query(models.Task).filter(models.Task.type_task == type_task).order_by(
                models.Task.created_at).offset(skip).limit(limit).all()
    else:
        if status:
            return db.query(models.Task).filter(models.Task.status == status).order_by(models.Task.created_at).offset(
                skip).limit(limit).all()
        else:
            return db.query(models.Task).order_by(models.Task.created_at).offset(skip).limit(limit).all()


def get_list_task_has_phone_number(db: Session, phone: str):
    return db.query(models.Task).filter(models.Task.phone.like('{}%'.format(phone))).all()


def get_detail_task(db: Session, user_id: int, task_id: str):
    return db.query(models.Task).filter(models.Task.task_id == task_id, models.Task.user_id == user_id).first()


def get_task_by_id(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def get_task_by_task_id(db: Session, task_id: str):
    return db.query(models.Task).filter(models.Task.task_id == task_id).first()


def get_task_of_staff_by_task_id(db: Session, staff_id: int, task_id: str):
    return db.query(models.Task).filter(models.Task.staff_id == staff_id, models.Task.task_id == task_id).first()


def update_status_by_task_id(db: Session, task_id: str, status: int, status_history: Optional[any] = None):
    current_task = db.query(models.Task).filter(models.Task.task_id == task_id).first()
    if current_task is not None:
        current_task.updated_at = datetime.now()
        current_task.status = status
        if status_history is not None:
            current_task.status_history = current_task.status_history + [status_history]
        db.commit()
        db.refresh(current_task)
        return current_task
    else:
        return False


def user_accept_staff(db: Session, user_id: int, task_id: str, staff_id: int):
    current_task = db.query(models.Task).filter(
        models.Task.task_id == task_id, models.Task.user_id == user_id).first()
    if current_task is not None:
        if current_task.status == constants.TASK_STATUS_INVITE_STAFF and current_task.staff_id is None:
            current_task.staff_id = staff_id
            current_task.status = constants.TASK_STATUS_WAITTING
            current_task.status_history = current_task.status_history + [
                update_task_history_status(status=3, time=current_task.start_time)]
            db.commit()
            db.refresh(current_task)
            return current_task
    return None


def check_staff_list_is_not_busy(db: Session, staff_list_id: List[int], start_time: datetime, end_time: datetime):
    start_time = start_time - timedelta(hours=1)
    end_time = end_time + timedelta(hours=1)
    staff_list = jsonable_encoder(db.query(models.TaskOfStaff).outerjoin(models.Task).filter(
        models.TaskOfStaff.staff_id.in_(staff_list_id),
        and_(models.Task.start_time >= start_time, models.Task.end_time <= end_time)).all())
    if len(staff_list) == 0:
        return staff_list_id
    else:
        list_id = list(map(lambda x: x['staff_id'], staff_list))
        for staff_id in list_id:
            if staff_id in staff_list_id:
                staff_list_id.remove(staff_id)
        return staff_list_id


def count_list_task_by_user_id(db: Session, user_id: int, type_task: str, status: List[int]):
    return db.query(models.Task).filter(models.Task.user_id == user_id, models.Task.type_task == type_task,
                                        models.Task.status.in_(status)).count()


def get_list_task_by_user_id(db: Session, user_id: int, type_task: str, status: List[int],
                             limit: int = 20, skip: int = 0):
    return db.query(models.Task).filter(models.Task.user_id == user_id, models.Task.type_task == type_task).filter(
        models.Task.status.in_(status)).order_by(models.Task.id.desc()).offset(skip).limit(limit).all()


def count_task_history_by_user(db: Session, user_id: int, type_task: Optional[str] = None,
                               status: Optional[int] = None):
    if type_task:
        if status == 4 or status == 5:
            return db.query(models.Task).filter(models.Task.user_id == user_id, models.Task.type_task == type_task,
                                                models.Task.status == status).count()
        return db.query(models.Task).filter(models.Task.user_id == user_id, models.Task.type_task == type_task,
                                            or_(models.Task.status == 4, models.Task.status == 5)).count()
    else:
        if status == 4 or status == 5:
            return db.query(models.Task).filter(models.Task.user_id == user_id,
                                                models.Task.status == status).count()
        return db.query(models.Task).filter(models.Task.user_id == user_id,
                                            or_(models.Task.status == 4, models.Task.status == 5)).count()


def get_task_history_by_user(db: Session, user_id: int, type_task: Optional[str] = None, status: Optional[int] = None,
                             limit: int = 20, skip: int = 0):
    if type_task:
        if status == 4 or status == 5:
            return db.query(models.Task).filter(models.Task.user_id == user_id, models.Task.type_task == type_task,
                                                models.Task.status == status).order_by(
                models.Task.updated_at.asc()).offset(skip).limit(limit).all()
        return db.query(models.Task).filter(models.Task.user_id == user_id, models.Task.type_task == type_task,
                                            or_(models.Task.status == 4, models.Task.status == 5)).order_by(
            models.Task.updated_at.asc()).offset(skip).limit(limit).all()

    else:
        if status == 4 or status == 5:
            return db.query(models.Task).filter(models.Task.user_id == user_id, models.Task.status == status).order_by(
                models.Task.updated_at.asc()).offset(skip).limit(limit).all()
        return db.query(models.Task).filter(models.Task.user_id == user_id,
                                            or_(models.Task.status == 4, models.Task.status == 5)).order_by(
            models.Task.updated_at.asc()).offset(skip).limit(limit).all()


def check_staff_is_working(db: Session, staff_id: int, user_id: int):
    # checking staff has done task with status is 5 or 6 (completed task)
    checking = db.query(models.Task).filter(models.Task.staff_id == staff_id, models.Task.user_id == user_id,
                                            models.Task.status.in_([5, 6])).first()
    return True if checking else False


def get_list_task_by_staff_id(db: Session,
                              type_task: str,
                              staff_id: int,
                              time_from: str,
                              time_to: str,
                              status: Optional[List] = None):
    if status is not None:
        return db.query(models.Task).filter(models.Task.staff_id == staff_id,
                                            models.Task.status.in_(status),
                                            models.Task.start_time >= time_from,
                                            models.Task.start_time <= time_to,
                                            models.Task.type_task == type_task
                                            ).all()
    else:
        return db.query(models.Task).filter(models.Task.staff_id == staff_id,
                                            models.Task.start_time >= time_from,
                                            models.Task.start_time <= time_to,
                                            models.Task.type_task == type_task
                                            ).all()


def get_detail_task_by_id(db: Session, task_id: str, staff_id: int):
    return db.query(models.Task).filter(models.Task.task_id == task_id, models.Task.staff_id == staff_id).first()


def get_task_by_list_task_id(db: Session, list_task_id: List[str], staff_id: int, status: List[int]):
    return db.query(models.Task).filter(models.Task.task_id.in_(list_task_id),
                                        models.Task.staff_id == staff_id,
                                        models.Task.status.in_(status)
                                        ).all()
