from datetime import datetime
from typing import List, Optional

from fastapi import File, Form, UploadFile
from pydantic import BaseModel, Json

from app.schemas.staff_schemas import Staff

from app.schemas.task_schedule_schemas import TaskSchedule


class StatusHistory(BaseModel):
    time: float
    status: int
    content: str
    status_label: str
    image: str


# 7.Task
class TaskBase(BaseModel):
    type_task: str
    fullname: str
    address: str
    user_id: int
    fullname: str
    phone: str
    created_at: datetime
    updated_at: datetime
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    total_price: float
    is_choice_staff_favorite: bool
    type_package: Optional[str] = None
    fee_tool: Optional[float] = None
    status: int
    user_cancel_task_reason: Optional[str] = None
    has_tool: bool
    discount: float
    payment_method: str
    task_id: str
    note: Optional[str] = None
    staff_id: Optional[int] = None
    staff_info: Optional[Staff] = None
    status_history: List[StatusHistory]
    voucher: Optional[str] = None
    schedule: List[datetime] = None
    packaging: Optional[str] = None
    status_vi: Optional[str] = None
    info_schedules: Optional[List] = None


class CreateOddShift(BaseModel):
    location_id: int
    start_time: datetime
    end_time: datetime
    is_choice_staff_favorite: Optional[bool] = False
    note: Optional[str] = None
    has_tool: bool
    payment_method: str
    voucher: Optional[str] = None


class CalculateOddShift(BaseModel):
    start_time: datetime
    end_time: datetime
    has_tool: Optional[bool] = False
    voucher: Optional[str] = None


class CreateFixedShift(BaseModel):
    location_id: int
    packaging: str
    start_date: datetime
    end_date: datetime
    start_time: datetime
    end_time: datetime
    schedule: List[datetime]
    is_choice_staff_favorite: Optional[bool] = False
    note: Optional[str] = None
    has_tool: bool
    payment_method: str = "cash"
    voucher: Optional[str] = None

    class Config:
        orm_mode = True


class CaculateFixedShift(BaseModel):
    start_date: datetime
    end_date: datetime
    start_time: datetime
    end_time: datetime
    schedule: List[datetime]
    has_tool: bool
    voucher: Optional[str] = None


class GetTask(BaseModel):
    type_task: Optional[str] = None


class Task(TaskBase):
    id: int
    is_active: bool = True

    class Config:
        orm_mode = True


class ListTaskResponse(BaseModel):
    detail: str
    data: List[Task]


class TaskResponse(BaseModel):
    detail: str
    data: Task


class QueryTask(BaseModel):
    status: List[int]
    type_task: str
    limit: Optional[int] = 20
    page: Optional[int] = 1


class Calendar(BaseModel):
    time_from: datetime
    time_to: datetime


