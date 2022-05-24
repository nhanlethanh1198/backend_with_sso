from datetime import datetime
from typing import List, Optional

from fastapi import File, Form, UploadFile
from pydantic import BaseModel, Json


class UpdateStatusSchedule(BaseModel):
    schedule_id: int
    reason: Optional[str] = None


class CreateTaskSchedule(BaseModel):
    f_user_id: int
    f_staff_id: int
    f_task_id: int
    task_id: str
    type_task: str
    schedule_status: int
    time_from: datetime
    time_to: datetime
    note: Optional[str] = None
    cancel_reason: Optional[str] = None
    comment: Optional[str] = None


class TaskSchedule(BaseModel):
    f_user_id: int
    f_staff_id: int
    f_task_id: int
    task_id: str
    type_task: str
    schedule_status: int
    time_from: datetime
    time_to: datetime
    note: Optional[str] = None
    cancel_reason: Optional[str] = None
    comment: Optional[str] = None
