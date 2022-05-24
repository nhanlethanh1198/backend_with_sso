LOGIN_OTP = 'LOGIN_OTP'
TYPE_SMS = 2
LIMIT_PHONE_OTP_OF_DAY = 3

USER_RANK_POINT = {
    "Đồng": 1000,
    "Bạc": 5000,
    "Vàng": 10000,
}

# TYPE TASK
ODD_SHIFT = "odd_shift"
FIXED_SHIFT = "fixed_shift"


# PRICE TASK
PRICE_FOR_ODD_SHIFT = 70000
PRICE_FOR_FIXED_SHIFT = 70000

# STATUS TASk
TASK_STATUS_NEW = 1
TASK_STATUS_INVITE_STAFF = 2
TASK_STATUS_WAITTING = 3
TASK_STATUS_PROCESSING = 4
TASK_STATUS_SUCCESS = 5
TASK_STATUS_CANCEL = 6,


def translate_task_status(status: int):
    switcher = {
        1: 'Công việc mới',
        2: 'Chưa có nhân viên',
        3: 'Đang chờ thực hiện',
        4: 'Đang thực hiện',
        5: 'Đã hoàn thành',
        6: 'Đã huỷ',
    }
    return switcher.get(status, 'invalid status')


# SCHEDULE STATUS
SCHEDULE_STATUS_NEW = 1
SCHEDULE_STATUS_DOING = 2
SCHEDULE_STATUS_DONE = 3
SCHEDULE_STATUS_CANCEL = 4


def translate_schedule_status(status: int):
    switcher = {
        1: 'Chưa làm',
        2: 'Đang làm',
        3: 'Đã làm xong',
        4: 'Không làm',
    }
    return switcher.get(status, 'invalid status')
