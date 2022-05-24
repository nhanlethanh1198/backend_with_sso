import enum
import math
from datetime import datetime
from typing import Optional, List

from fastapi.encoders import jsonable_encoder

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Form
from sqlalchemy.orm import Session

from app.schemas import user_schemas, task_schemas, task_schedule_schemas

from app import firebase, response_models

from app import constants

from app.dependencies import get_timestamp, generate_timestamp

from app.backgrounds.tasks import invite_staff_join_job, update_task_status
from app.backgrounds.notifications import send_notify_by_user_id, create_notify_on_firebase

from app.database import get_db
from app.get_current_staff import get_current_staff, CurrentStaff
from app.get_current_user import get_current_user, CurrentUser
from app.logger import AppLog
from app.repositories import tasks, staffs, locations, task_of_staff, task_schedule, notification
from app.services.tasks import fee_odd_shift, check_fee_tool, discount, fee_fixed_shift, update_task_history_status

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    responses={404: {"description": "Not found"}},
)


class TypeTask(str, enum.Enum):
    odd_shift = "odd_shift"
    fixed_shift = "fixed_shift"


class TaskStatus(enum.IntEnum, enum.Enum):
    WAITING = 1
    ACCEPTED = 2
    WORKING = 3
    COMPLETED = 4
    CANCELED = 5


class TaskStatusHistory(enum.IntEnum, enum.Enum):
    COMPLETED = 4
    CANCELED = 5


@router.post("/user-get-list-task", summary="Lấy danh sách công việc đã tạo của user",
             response_model=response_models.UserGetListTaskResponse)
async def user_get_list_task(request: task_schemas.QueryTask, db: Session = Depends(get_db),
                             current_user: CurrentUser = Depends(get_current_user)):
    user_id = current_user.user_id
    limit = request.limit
    page = request.page
    status = request.status
    type_task = request.type_task

    count_task = tasks.count_list_task_by_user_id(db=db, user_id=user_id, type_task=type_task, status=status)
    total_page = math.ceil(count_task / limit)
    skip = (page - 1) * limit

    task_list = tasks.get_list_task_by_user_id(db=db, user_id=user_id, type_task=type_task, status=status, skip=skip,
                                               limit=limit)

    json_task = jsonable_encoder(task_list)
    data_response = []
    for each_task in json_task:
        json_each_task = jsonable_encoder(each_task)
        temp = {
            **json_each_task,
            "status_vi": constants.translate_task_status(json_each_task['status'])
        }
        data_response.append(temp)

    prev_page = page - 1
    if prev_page <= 0:
        prev_page = None

    next_page = page + 1
    if next_page > total_page:
        next_page = None

    return {
        "detail": "success",
        "data": data_response,
        "total_tasks": count_task,
        "limit": limit,
        "prev_page": prev_page,
        "current_page": page,
        "next_page": next_page,
        "total_page": total_page
    }


@router.get('/user-history-task', summary="Lấy danh sách task đã hoàn thành hoặc hủy của user",
            response_model=response_models.UserGetListTaskResponse, description="""
params: 
- type_task: Loại công việc (odd_shift, fixed_shift), mặc định để trống không kèm theo giá trị nào.
- status: Default là None, hoặc 4 (đã hoàn thành) hoặc 5 (hủy). nếu status khác 4 hoặc 5 thì sẽ xem như là None.
""")
async def user_history_task(type_task: Optional[TypeTask] = None, limit: int = 20, page: int = 1,
                            status: Optional[TaskStatusHistory] = None, db: Session = Depends(get_db),
                            current_user: CurrentUser = Depends(get_current_user)):
    user_id = current_user.user_id
    task_list = []
    count_task = 0
    total_page = 0
    if type_task is not None:
        count_task = tasks.count_task_history_by_user(db=db, user_id=user_id, type_task=type_task, status=status)
        total_page = math.ceil(count_task / limit)
        skip = (page - 1) * limit
        task_list = tasks.get_task_history_by_user(db=db, user_id=user_id, type_task=type_task, skip=skip, limit=limit,
                                                   status=status)
    else:
        count_task = tasks.count_task_history_by_user(db=db, user_id=user_id, status=status)
        total_page = math.ceil(count_task / limit)
        skip = (page - 1) * limit
        task_list = tasks.get_task_history_by_user(db=db, user_id=user_id, skip=skip, limit=limit, status=status)

    prev_page = page - 1
    if prev_page <= 0:
        prev_page = None

    next_page = page + 1
    if next_page > total_page:
        next_page = None

    return {
        "detail": "success",
        "data": task_list,
        "total_tasks": count_task,
        "limit": limit,
        "prev_page": prev_page,
        "current_page": page,
        "next_page": next_page,
        "total_page": total_page
    }


class AdminGetTaskByStatus(enum.IntEnum, enum.Enum):
    WAITING = 1
    ACCEPTED = 2
    WORKING = 3
    COMPLETED = 4
    CANCELED = 5
    SIX = 6
    SEVEN = 7


@router.get("/staff-get-list-task", summary='Admin get task list',
            response_model=response_models.UserGetListTaskResponse)
async def staff_get_list_task(type_task: Optional[TypeTask] = None, status: Optional[AdminGetTaskByStatus] = None,
                              phone: Optional[str] = None, limit: Optional[int] = 50,
                              page: Optional[int] = 1, db: Session = Depends(get_db),
                              current_staff: CurrentStaff = Depends(get_current_staff)):
    if current_staff.role != 'admin':
        raise HTTPException(status_code=403, detail="Bạn không có quyền truy cập")

    if phone is None:
        count_task = tasks.count_task(db=db, type_task=type_task, status=status)
        total_page = math.ceil(count_task / limit)
        skip = (page - 1) * limit
        task_list = tasks.staff_get_list_task(db=db, type_task=type_task, skip=skip, limit=limit, status=status)

        prev_page = page - 1
        if prev_page <= 0:
            prev_page = None

        next_page = page + 1
        if next_page > total_page:
            next_page = None

        return {
            "detail": "success",
            "total_tasks": count_task,
            "limit": limit,
            "prev_page": prev_page,
            "current_page": page,
            "next_page": next_page,
            "total_page": total_page,
            "data": task_list
        }
    else:
        results = tasks.get_list_task_has_phone_number(db=db, phone=phone)
        return {
            "detail": "success",
            "limit": limit,
            "prev_page": None,
            "current_page": 1,
            "next_page": None,
            "total_page": 1,
            "data": results
        }


@router.get("/get-detail-task/{task_id}")
async def get_detail_task(task_id: str, db: Session = Depends(get_db),
                          current_user: CurrentUser = Depends(get_current_user)):
    current_task = tasks.get_detail_task(db=db, user_id=current_user.user_id, task_id=task_id)

    staff_info = None
    if current_task.staff_id is not None:
        staff_info = staffs.get_staff_info(db=db, staff_id=current_task.staff_id)

    list_schedule = None
    if current_task.type_task == constants.FIXED_SHIFT:
        current_schedules = task_schedule.get_list_task_schedule(db=db, task_id=current_task.task_id,
                                                                 user_id=current_user.user_id)
        list_schedule = []
        for schedule in current_schedules:
            json_schedule = jsonable_encoder(schedule)
            temp = {
                **json_schedule,
                "status_vi": constants.translate_schedule_status(json_schedule['schedule_status'])
            }
            list_schedule.append(temp)

    jsonTask = jsonable_encoder(current_task)
    data_response = {
        **jsonTask,
        "status_vi": constants.translate_task_status(current_task.status),
        "staff_info": jsonable_encoder(staff_info) if staff_info is not None else staff_info,
        "list_schedule": list_schedule
    }

    return {
        "detail": "success",
        "data": data_response
    }


@router.get('/get-task-schedule/{task_id}')
async def get_task_schedule(task_id: str, db: Session = Depends(get_db),
                            current_user: CurrentUser = Depends(get_current_user)):
    current_task = tasks.get_detail_task(db=db, user_id=current_user.user_id, task_id=task_id)
    if current_task.type_task == constants.FIXED_SHIFT:
        current_schedules = task_schedule.get_list_task_schedule(db=db, task_id=current_task.task_id,
                                                                 user_id=current_user.user_id)
        list_schedule = []
        for schedule in current_schedules:
            json_schedule = jsonable_encoder(schedule)
            temp = {
                **json_schedule,
                "status_vi": constants.translate_schedule_status(json_schedule['schedule_status'])
            }
            list_schedule.append(temp)
        return {
            "detail": "success",
            "data": list_schedule
        }
    else:
        return {
            "detail": "success",
            "data": None
        }


@router.post('/calculate-odd-shift-fee', summary="Caculate odd shift fee",
             response_model=response_models.CalculateOddShiftFeeResponse)
async def calculate_odd_shift_fee(data: task_schemas.CalculateOddShift):
    start_time = data.start_time
    end_time = data.end_time
    if start_time.hour < 8 or start_time.hour > 18 or end_time.hour < 8 or end_time.hour > 18:
        raise HTTPException(status_code=400, detail="Thời gian đặt lịch hẹn phải từ 8h - 18h")
    hours = end_time.hour - start_time.hour
    minutes = end_time.minute - start_time.minute

    if minutes == 0:
        pass
    elif minutes > 0:
        hours = hours + 0.5
    else:
        hours = hours - 0.5

    if hours < 2:
        raise HTTPException(status_code=400, detail="Thời gian làm tối thiểu để nhân viên làm phải nhiều hơn 2h.")
    fee_task = fee_odd_shift(hours)
    fee_tool = check_fee_tool(data.has_tool)
    discount_price = discount(data.voucher)
    total_price = fee_task + fee_tool - discount_price

    return {
        "hours": hours,
        "fee_task": fee_task,
        "fee_tool": fee_tool,
        "discount_price": discount_price,
        "total_price": total_price,
        "price_per_hour": constants.PRICE_FOR_ODD_SHIFT
    }


@router.post("/create-odd-shift", summary="User tạo việc làm ca lẻ",
             response_model=response_models.CreateOddShiftResponse)
async def create_odd_shift(data: task_schemas.CreateOddShift, background_tasks: BackgroundTasks,
                           db: Session = Depends(get_db),
                           current_user: CurrentUser = Depends(get_current_user)):
    start_time = data.start_time
    end_time = data.end_time
    year = start_time.year
    month = start_time.month
    day = start_time.day

    start_time_stamp = get_timestamp(start_time)
    end_time_stamp = get_timestamp(end_time)

    AppLog('Create odd shift data1: ').info(data)

    current_time = datetime.now()
    if start_time_stamp <= current_time.timestamp():
        raise HTTPException(status_code=400, detail="Thời gian đặt lịch không hợp lệ!")

    if end_time_stamp < start_time_stamp:
        raise HTTPException(status_code=400, detail="Thời gian đặt lịch không hợp lệ!")

    min_time_stamp = generate_timestamp(year=year, month=month, day=day, hour=8, minute=0)
    max_time_stamp = generate_timestamp(year=year, month=month, day=day, hour=16, minute=0)

    if start_time_stamp < min_time_stamp:
        raise HTTPException(status_code=400, detail="Thời gian đặt lịch hẹn phải từ 8h - 16h")

    if start_time_stamp > max_time_stamp:
        raise HTTPException(status_code=400, detail="Thời gian đặt lịch hẹn phải từ 8h - 16h")

    if end_time_stamp < min_time_stamp:
        raise HTTPException(status_code=400, detail="Thời gian đặt lịch hẹn phải từ 8h - 16h")

    total_hours = end_time.hour - start_time.hour

    if total_hours < 2:
        raise HTTPException(status_code=400, detail="Thời gian làm tối thiểu để nhân viên làm phải nhiều hơn 2h.")

    fee_task = fee_odd_shift(total_hours)

    fee_tool = check_fee_tool(data.has_tool)

    discount_price = discount(data.voucher)

    total_price = fee_task + fee_tool - discount_price

    location = locations.get_location_by_id(db=db, location_id=data.location_id, user_id=current_user.user_id)
    if location is None:
        raise HTTPException(status_code=400, detail="Địa chỉ không hợp lệ")

    address = "{}, {}, {}".format(location.address, location.district, location.city)

    data_task = {
        "type_task": "odd_shift",
        "address": address,
        "start_time": start_time,
        "end_time": end_time,
        "is_choice_staff_favorite": data.is_choice_staff_favorite,
        "status": constants.TASK_STATUS_NEW,
        "status_history": [update_task_history_status(status=1)],
        "note": data.note,
        "voucher": data.voucher,
        "discount": discount_price,
        "payment_method": data.payment_method,
        "has_tool": data.has_tool,
        "user_id": current_user.user_id,
        "fullname": location.fullname,
        "phone": location.phone,
        "fee_tool": fee_tool,
        "total_price": total_price,
    }

    AppLog('Create odd shift data2: ').info(data_task)

    new_task = tasks.create_odd_shift(db=db, data=data_task)

    if not new_task:
        AppLog('Create odd shift fail').info('User {} create odd shift fail'.format(current_user.user_id))
        raise HTTPException(
            status_code=400, detail="Đã có lỗi xảy ra, vui lòng thao tác lại")

    # tạo notification
    start_time = new_task.start_time.strftime("%Y-%m-%d %H:%M")
    json_detail = {
        "task_id": new_task.task_id,
        "type_task": new_task.type_task
    }
    data = {
        "title": "Tạo công việc mới",
        "content": "Bạn đã tạo công việc dọn dẹp ca lẻ <b>{}</b>, công việc sẽ bắt đầu vào lúc {}".format(
            new_task.task_id, start_time),
        "type": "create_task",
        "detail": json_detail
    }
    background_tasks.add_task(create_notify_on_firebase, db=db, user_id=current_user.user_id, data=data)

    # step 2: xử lý chạy nền
    task_id = new_task.task_id
    created_at = new_task.created_at.strftime("%Y-%m-%d %H:%M:%S")
    data_notify = {
        "title": "Thông báo giúp việc",
        "body": 'Quý khách tạo yêu cầu giúp việc ca lẻ {} thành công vào lúc {}'.format(task_id, created_at),
        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ9z1dlCAXT0U2-9CCeiTltXGF4sIp5pqhxQ6Bqz6rQusISXKBL_0r5CbFZ1W6o7BnuR9M&usqp=CAU"
    }

    background_tasks.add_task(send_notify_by_user_id, db=db, user_id=current_user.user_id, data_notify=data_notify)

    background_tasks.add_task(invite_staff_join_job, db=db, current_task=new_task)

    return {
        "detail": "success",
        "data": new_task
    }


@router.post("/caculate-fixed-shift-fee", summary="Caculate fixed shift fee",
             response_model=response_models.CalculateFixedShiftFeeResponse)
async def caculate_fixed_shift_fee(data: task_schemas.CaculateFixedShift):
    start_time = data.start_time
    end_time = data.end_time

    if start_time.hour < 8 or start_time.hour > 18 or end_time.hour < 8 or end_time.hour > 18:
        raise HTTPException(status_code=400, detail="Thời gian đặt lịch hẹn phải từ 8h - 18h")
    day_count = len(data.schedule)
    hours_per_day = end_time.hour - start_time.hour
    minutes = end_time.minute - start_time.minute

    if minutes == 0:
        pass
    elif minutes > 0:
        hours_per_day = hours_per_day + 0.5
    else:
        hours_per_day = hours_per_day - 0.5

    if hours_per_day < 2:
        raise HTTPException(status_code=400, detail="Thời gian làm tối thiểu để nhân viên làm phải nhiều hơn 2h.")
    fee_task = fee_fixed_shift(hours_per_day * day_count)
    fee_tool = check_fee_tool(data.has_tool)
    discount_price = discount(data.voucher)
    total_price = fee_task + fee_tool - discount_price

    return {
        "day_count": day_count,
        "hours_per_day": hours_per_day,
        "total_day": day_count,
        "fee_task": fee_task,
        "fee_tool": fee_tool,
        "discount_price": discount_price,
        "total_price": total_price,
        "price_per_hour": constants.PRICE_FOR_FIXED_SHIFT
    }


@router.post("/create-fixed-shift", summary='Create New Fixed Shift',
             response_model=response_models.CreateFixedShiftResponse)
async def create_fixed_shift(data: task_schemas.CreateFixedShift, background_tasks: BackgroundTasks,
                             db: Session = Depends(get_db),
                             current_user: CurrentUser = Depends(get_current_user)):
    user_id = current_user.user_id
    start_time = data.start_time
    end_time = data.end_time
    if start_time.hour < 8 or start_time.hour > 18 or end_time.hour < 8 or end_time.hour > 18:
        raise HTTPException(status_code=400, detail="Thời gian đặt lịch hẹn phải từ 8h - 18h")
    day_count = len(data.schedule)
    hours_per_day = end_time.hour - start_time.hour
    if hours_per_day < 2:
        raise HTTPException(status_code=400, detail="Thời gian làm tối thiểu để nhân viên làm phải nhiều hơn 2h.")
    fee_task = fee_fixed_shift(hours_per_day * day_count)
    fee_tool = check_fee_tool(data.has_tool)
    discount_price = discount(data.voucher)
    total_price = fee_task + fee_tool - discount_price
    location = locations.get_location_by_id(db=db, location_id=data.location_id, user_id=user_id)
    address = "{}, {}, {}".format(location.address, location.district, location.city)

    data_task = {
        "type_task": "fixed_shift",
        "packaging": data.packaging,
        "fullname": location.fullname,
        "address": address,
        "start_date": data.start_date,
        "end_date": data.end_date,
        "start_time": start_time,
        "end_time": end_time,
        "is_choice_staff_favorite": data.is_choice_staff_favorite,
        "status": constants.TASK_STATUS_NEW,
        "note": data.note,
        "voucher": data.voucher,
        "discount": discount_price,
        "payment_method": data.payment_method,
        "has_tool": data.has_tool,
        "user_id": current_user.user_id,
        "phone": location.phone,
        "fee_tool": fee_tool,
        "total_price": total_price,
        "schedule": data.schedule,
        "status_history": [update_task_history_status(status=1)],
    }

    AppLog('create fixed shift data').info(data_task)

    # Step 1: Tạo task (kiểm tra đồng thời user có tạo staff bị trùng hoặc vừa tạo hay ko)

    task = tasks.create_fixed_shift(db=db, data=data_task)

    if not task:
        AppLog('create fixed shift').info('User {} create fixed shift fail'.format(current_user.user_id))
        raise HTTPException(status_code=400, detail="Đã có lỗi xảy ra, vui lòng thao tác lại")

    # tạo notification
    start_time = task.start_time.strftime("%Y-%m-%d %H:%M")
    json_detail = {
        "task_id": task.task_id,
        "type_task": task.type_task
    }
    data = {
        "title": "Tạo công việc mới",
        "content": "Bạn đã tạo công việc dọn dẹp ca cố định <b>{}</b>, công việc sẽ bắt đầu vào lúc {}".format(
            task.task_id, start_time),
        "type": "create_task",
        "detail": json_detail
    }
    background_tasks.add_task(create_notify_on_firebase, db=db, user_id=current_user.user_id, data=data)

    # Step 2: Xử lý chạy nền

    background_tasks.add_task(invite_staff_join_job, db=db, current_task=task)

    return {
        "detail": "success",
        "data": task
    }


@router.post("/user-cancel-task/{task_id}", summary="User hủy task bằng id của task")
async def user_cancel_staff(task_id: str, request: user_schemas.UserCancelWithReason, db: Session = Depends(get_db),
                            current_user: CurrentUser = Depends(get_current_user)):
    task_db = tasks.get_detail_task(db=db, task_id=task_id, user_id=current_user.user_id)

    if task_db is None:
        raise HTTPException(status_code=400, detail="Không thể tìm thấy task hoặc task đã hoàn thành")
    else:
        if task_db.status == constants.TASK_STATUS_NEW:
            # Chỉ cho phép hủy task khi user chưa chọn nhân viên nhận việc
            # Cập nhật tại firebase
            fb_task = firebase.user_cancel_task(str(task_id),
                                                user_id=str(current_user.user_id))  # Cần thêm lý do hủy tại chỗ này
            if fb_task is False:
                raise HTTPException(status_code=400, detail="Không thể tìm thấy task hoặc task đã hoàn thành")

            # Hủy task
            status_history = task_db.status_history
            if task_db.type_task == constants.ODD_SHIFT:
                task_db.status = constants.TASK_STATUS_CANCEL
                status_history.append(update_task_history_status(status=6))
                task_db.status_history = status_history

            if task_db.type_task == constants.FIXED_SHIFT:
                task_db.status = constants.TASK_STATUS_CANCEL
                status_history.append(update_task_history_status(status=4))
                task_db.status_history = status_history

            task_db.user_cancel_task_reason = request.reason
            db.commit()
            db.refresh(task_db)

        else:
            raise HTTPException(status_code=400, detail="Không thể hủy task khi đã chọn nhân viên")

    return {
        "detail": "success",
        "data": task_db
    }


@router.post("/user-accept-staff")
async def user_accept_staff(data: user_schemas.UserAcceptStaff, db: Session = Depends(get_db),
                            current_user: CurrentUser = Depends(get_current_user)):
    task_id = data.task_id
    staff_id = data.staff_id

    # kiểm tra 1 lần nữa user có rảnh hay không

    current_task = tasks.user_accept_staff(db=db, user_id=current_user.user_id, task_id=task_id, staff_id=staff_id)
    if current_task is None:
        raise HTTPException(status_code=400, detail="Không thể chọn nhân viên này!")
    else:
        # Tạo danh sách task trong bảng task_schedules
        if current_task.type_task == constants.ODD_SHIFT:
            data = {
                "f_user_id": current_user.user_id,
                "f_staff_id": current_task.staff_id,
                "f_task_id": current_task.id,
                "task_id": current_task.task_id,
                "type_task": current_task.type_task,
                "schedule_status": constants.SCHEDULE_STATUS_NEW,
                "time_from": current_task.start_time,
                "time_to": current_task.end_time
            }
            new_task_schedule = task_schedule.create_task_schedule(db=db, data=data)
            if not new_task_schedule:
                raise HTTPException(status_code=400, detail="Không thể chọn nhân viên này!")
        elif current_task.type_task == constants.FIXED_SHIFT:
            schedule = current_task.schedule
            for day in schedule:
                working_hour = current_task.end_time - current_task.start_time
                data = {
                    "f_user_id": current_user.user_id,
                    "f_staff_id": current_task.staff_id,
                    "f_task_id": current_task.id,
                    "task_id": current_task.task_id,
                    "type_task": current_task.type_task,
                    "schedule_status": constants.SCHEDULE_STATUS_NEW,
                    "time_from": day,
                    "time_to": day + working_hour
                }
                new_task_schedule = task_schedule.create_task_schedule(db=db, data=data)
                if not new_task_schedule:
                    raise HTTPException(status_code=400, detail="Không thể chọn nhân viên này!")
    return {
        "detail": "success",
        "data": jsonable_encoder(current_task)
    }


@router.post("/staff-decline-task/{task_id}")
async def staff_decline_staff(task_id: int, db: Session = Depends(get_db),
                              current_user: CurrentUser = Depends(get_current_user)):
    return {
        "detail": "success"
    }


@router.post("/staff-accept-task/{task_id}", summary="Staff accept task bằng task_id")
async def staff_accept_task(task_id: str,
                            background_tasks: BackgroundTasks,
                            db: Session = Depends(get_db),
                            current_staff: CurrentStaff = Depends(get_current_staff)):
    staff = staffs.get_staff_info(db=db, staff_id=current_staff.staff_id)

    current_task = tasks.get_task_by_task_id(db=db, task_id=task_id)
    if current_task is not None:
        json_current_task = jsonable_encoder(current_task)
        if json_current_task['status'] == constants.TASK_STATUS_NEW:
            status_history = update_task_history_status(2)
            tasks.update_status_by_task_id(db=db, task_id=task_id, status=constants.TASK_STATUS_INVITE_STAFF,
                                           status_history=status_history)
        await firebase.add_staff_into_task_fb(user_id=str(current_task.user_id), task_id=str(task_id),
                                              staff_id=str(current_staff.staff_id))

        # tạo notification
        json_detail = {
            "task_id": current_task.task_id,
            "type_task": current_task.type_task,
            "staff_id": current_staff.staff_id
        }
        type_task = "ca lẻ" if current_task.type_task == "odd_shift" else "ca cố định"
        staff_full_name = staff.fullname
        data = {
            "title": "Có nhân viên mới",
            "content": "Dọn dẹp nhà {} <b>{}</b> - nhân viên <b>{}</b> đã nhận công việc".format(type_task,
                                                                                                 current_task.task_id,
                                                                                                 staff_full_name),
            "type": "staff_accept_task",
            "detail": json_detail
        }
        background_tasks.add_task(create_notify_on_firebase, db=db, user_id=current_task.user_id, data=data)
    return {
        "detail": "success"
    }


@router.get('/user-get-staff-accept/{task_id}', summary="User get staff accept list bằng id của task")
async def get_staff_accept_list(task_id: int, current_user: CurrentUser = Depends(get_current_user)):
    user_id = current_user.user_id

    staff_accept_list = firebase.get_staff_accept_list(task_id=str(task_id), user_id=str(user_id))

    return {
        "detail": "success",
        "data": staff_accept_list
    }


@router.post("/staff-change-task-status/{task_id}", summary='Staff change task status')
async def staff_change_task_status(task_id: int, status: AdminGetTaskByStatus, db=Depends(get_db),
                                   current_staff: CurrentStaff = Depends(get_current_staff)):
    staff_id = current_staff.staff_id
    status_value = status.value

    return {
        "detail": "success",
        "task_id": task_id,
        "staff_id": staff_id,
        "status": status_value
    }


@router.post("/staff-start-doing/{task_id}", summary="Nhân viên bắt đầu làm việc")
async def staff_start_doing(task_id: str, data: task_schedule_schemas.UpdateStatusSchedule, db=Depends(get_db),
                            current_staff: CurrentStaff = Depends(get_current_staff)):
    staff_id = current_staff.staff_id
    schedule_id = data.schedule_id
    schedule_status = constants.SCHEDULE_STATUS_DOING
    current_task = tasks.get_task_of_staff_by_task_id(db=db, staff_id=staff_id, task_id=task_id)
    list_status = [3, 4]
    if current_task is not None and current_task.status in list_status:
        result_update_schedule = task_schedule.update_task_schedule(db=db,
                                                                    task_id=task_id,
                                                                    schedule_id=schedule_id,
                                                                    status=schedule_status)
        status_history = update_task_history_status(status=4)
        tasks.update_status_by_task_id(db=db,
                                       task_id=task_id,
                                       status=constants.TASK_STATUS_PROCESSING,
                                       status_history=status_history)
        return {
            "detail": "success",
            "data": result_update_schedule
        }
    else:
        raise HTTPException(status_code=400, detail="Không thể cập nhật trạng thái công việc này!")


@router.post("/staff-finish-work/{task_id}", summary="Nhân viên hoàn thành buổi làm việc")
async def staff_finish_work(task_id: str,
                            background_tasks: BackgroundTasks,
                            data: task_schedule_schemas.UpdateStatusSchedule, db=Depends(get_db),
                            current_staff: CurrentStaff = Depends(get_current_staff)):
    staff_id = current_staff.staff_id
    schedule_id = data.schedule_id
    schedule_status = constants.SCHEDULE_STATUS_DONE

    current_task = tasks.get_task_of_staff_by_task_id(db=db, staff_id=staff_id, task_id=task_id)
    list_status = [3, 4]
    if current_task is not None and current_task.status in list_status:
        result_update_schedule = task_schedule.update_task_schedule(db=db,
                                                                    task_id=task_id,
                                                                    schedule_id=schedule_id,
                                                                    status=schedule_status)
        if result_update_schedule:

            if current_task.type_task == constants.ODD_SHIFT:
                status_history = update_task_history_status(5)
                tasks.update_status_by_task_id(db=db,
                                               task_id=task_id,
                                               status=constants.TASK_STATUS_SUCCESS,
                                               status_history=status_history)

            if current_task.type_task == constants.FIXED_SHIFT:
                list_schedule = task_schedule.get_lis_task_schedule_by_task(db=db, task_id=task_id)
                if len(list_schedule) == 1:
                    status_history = update_task_history_status(5)
                    tasks.update_status_by_task_id(db=db,
                                                   task_id=task_id,
                                                   status=constants.TASK_STATUS_SUCCESS,
                                                   status_history=status_history)
                else:
                    pass

            # tạo notification
            json_detail = {
                "task_id": current_task.task_id,
                "type_task": current_task.type_task,
                "staff_id": current_staff.staff_id
            }
            type_task = "ca lẻ" if current_task.type_task == "odd_shift" else "ca cố định"
            staff_full_name = current_staff.fullname
            data = {
                "title": "Hoàn thành công việc",
                "content": "Dọn dẹp nhà {} <b>{}</b> - nhân viên <b>{}</b> đã hoàn thành công việc, cám ơn quý khách đã "
                           "tin tưởng sử dụng dịch vụ".format(type_task,
                                                              current_task.task_id,
                                                              staff_full_name),
                "type": "staff_finish_task",
                "detail": json_detail
            }
            background_tasks.add_task(create_notify_on_firebase, db=db, user_id=current_task.user_id, data=data)
            return result_update_schedule
        else:
            raise HTTPException(status_code=400, detail="Không thể cập nhật công việc này!")

    else:
        raise HTTPException(status_code=400, detail="Không thể cập nhật công việc này!")


@router.post("/staff-cancel-work/{task_id}", summary="Nhân viên huỷ làm việc vì bận việc đột xuất")
async def staff_cancel_work(background_tasks: BackgroundTasks, task_id: str,
                            data: task_schedule_schemas.UpdateStatusSchedule, db=Depends(get_db),
                            current_staff: CurrentStaff = Depends(get_current_staff)):
    staff_id = current_staff.staff_id
    schedule_id = data.schedule_id
    schedule_status = constants.SCHEDULE_STATUS_CANCEL
    reason = data.reason

    current_task = tasks.get_task_of_staff_by_task_id(db=db, staff_id=staff_id, task_id=task_id)
    list_status = [3, 4]
    if current_task is not None and current_task.status in list_status:
        result_update_schedule = task_schedule.update_task_schedule(db=db, task_id=task_id, schedule_id=schedule_id,
                                                                    status=schedule_status, cancel_reason=reason)
        if result_update_schedule:

            if current_task.type_task == constants.ODD_SHIFT:
                status_history = update_task_history_status(6)
                tasks.update_status_by_task_id(db=db, task_id=task_id,
                                               status=constants.TASK_STATUS_CANCEL,
                                               status_history=status_history)

            if current_task.type_task == constants.FIXED_SHIFT:
                list_schedule = task_schedule.get_lis_task_schedule_by_task(db=db, task_id=task_id)
                if len(list_schedule) == 1:
                    status_history = update_task_history_status(6)
                    tasks.update_status_by_task_id(db=db, task_id=task_id,
                                                   status=constants.TASK_STATUS_CANCEL,
                                                   status_history=status_history)
                else:
                    pass

            # tạo notification
            json_detail = {
                "task_id": current_task.task_id,
                "type_task": current_task.type_task,
                "staff_id": current_staff.staff_id
            }
            type_task = "ca lẻ" if current_task.type_task == "odd_shift" else "ca cố định"
            staff_full_name = current_staff.fullname
            data = {
                "title": "Huỷ công việc",
                "content": "Dọn dẹp nhà {} <b>{}</b> - nhân viên <b>{}</b> đã huỷ công việc vì lý do: {}".format(
                    type_task, current_task.task_id, staff_full_name, reason),
                "type": "staff_cancel_task",
                "detail": json_detail
            }
            background_tasks.add_task(create_notify_on_firebase, db=db, user_id=current_task.user_id, data=data)
        return result_update_schedule
    else:
        raise HTTPException(status_code=400, detail="Không thể huỷ công việc này!")


@router.get("/staff-get-list-schedule-task", response_model=task_schemas.ListTaskResponse)
async def get_list_schedule(time_from: str,
                            time_to: str,
                            db=Depends(get_db),
                            current_staff: CurrentStaff = Depends(get_current_staff)):
    staff_id = current_staff.staff_id
    status = [3, 4]
    list_task = task_schedule.get_list_schedule(db=db,
                                                time_from=time_from,
                                                time_to=time_to)

    list_task_id = []
    for item in list_task:
        list_task_id.append(item.task_id)
    list_task_id = list(dict.fromkeys(list_task_id))

    results = tasks.get_task_by_list_task_id(db=db,
                                             list_task_id=list_task_id,
                                             staff_id=staff_id,
                                             status=status)

    return {
        "detail": "success",
        "data": results
    }


@router.get("/staff-get-history-task", response_model=task_schemas.ListTaskResponse)
async def get_list_history_task(
        type_task: str,
        time_from: Optional[str] = None,
        time_to: Optional[str] = None,
        db=Depends(get_db),
        current_staff: CurrentStaff = Depends(get_current_staff)):
    staff_id = current_staff.staff_id
    status = [5, 6]
    list_task = tasks.get_list_task_by_staff_id(db=db,
                                                staff_id=staff_id,
                                                status=status,
                                                time_from=time_from,
                                                time_to=time_to,
                                                type_task=type_task)
    return {
        "detail": "success",
        "data": list_task
    }


@router.get("/staff-get-detail-schedule-task/{task_id}", response_model=task_schemas.TaskResponse)
async def get_list_schedule(task_id: str, db=Depends(get_db), current_staff: CurrentStaff = Depends(get_current_staff)):
    staff_id = current_staff.staff_id
    detail_task = tasks.get_detail_task_by_id(db=db, task_id=task_id, staff_id=staff_id)
    return {
        "detail": "success",
        "data": detail_task
    }


@router.get("/staff-get-calendar-task")
async def get_list_calendar_task(time_from: str,
                                 time_to: str,
                                 db=Depends(get_db),
                                 current_staff: CurrentStaff = Depends(get_current_staff)):
    list_date = task_schedule.get_list_schedule(db=db, time_from=time_from, time_to=time_to)
    results = []
    for item in list_date:
        date_temp = "{}-{}-{}".format(item.time_from.year, item.time_from.month, item.time_from.day)
        results.append(date_temp)
    results = list(dict.fromkeys(results))
    return {
        "detail": "success",
        "data": results
    }
