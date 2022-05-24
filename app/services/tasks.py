from datetime import datetime
from typing import Optional

from app.constants import PRICE_FOR_ODD_SHIFT

import pytz

local = pytz.timezone('Asia/Ho_Chi_Minh')


def fee_odd_shift(hours):
    fee = hours * PRICE_FOR_ODD_SHIFT
    return fee


def fee_fixed_shift(hours):
    return hours * 65000


def check_fee_tool(has_tool):
    if has_tool:
        return 30000
    else:
        return 0


def discount(voucher):
    x = 0
    if voucher == "CODINH1":
        x = 2
    elif voucher == "CODINH2":
        x = 3

    switcher = {
        1: 0,
        2: 5000,
        3: 10000,
    }
    return switcher.get(x, 0)


def update_task_history_status(status: int, time: Optional[datetime] = None):
    if status not in [1, 2, 3, 4, 5, 6]:
        raise ValueError("Invalid status when update odd shift task")
    else:

        now = datetime.now(local)
        str_now = str(now.strftime("%H:%M:%S, %d/%m/%Y"))
        now_timestamp = now.timestamp()
        if time is None:
            str_time = '...'
        else:
            str_time = str(time.strftime("%H:%M:%S, %d/%m/%Y"))

        status_content = {
            1: "Lịch đặt giúp việc ca lẻ của quý khách đã được tiếp nhận vào lúc {}.".format(
                str_now),
            2: "Danh sách nhân viên nhận việc được cập nhật liên tục trong 1-3 ngày",
            3: "Công việc sẽ bắt đầu làm vào lúc {}.".format(str_time),
            4: "Danh sách theo dõi tiến độ hoàn thành công việc của nhân viên.",
            5: "Nhân viên đã hoàn thành công việc vào lúc {}. Cảm ơn quý khách đã tin tưởng dịch vụ của chúng tôi.".format(
                str_now),
            6: "Công việc này đã được hủy. Cảm ơn quý khách đã tin tưởng dịch vụ của chúng tôi."
        }

        content = status_content.get(status, 'Lỗi khi cập nhận thông tin trạng thái công việc')

        def status_label_name(status: int) -> str:
            switcher = {
                1: "Tiếp nhận lịch hẹn",
                2: "Xem danh sách nhân viên",
                3: "Đang chờ thực hiện",
                4: "Đang thực hiện",
                5: "Đã hoàn thành",
                6: "Đã huỷ"
            }
            return switcher.get(status, 'Lỗi')

        def status_image(status: int) -> str:
            switcher = {
                1: "https://tiing-storage.s3.ap-southeast-1.amazonaws.com/icons/status_icon/new.png",
                2: "https://tiing-storage.s3.ap-southeast-1.amazonaws.com/icons/status_icon/chonnhanvien.png",
                3: "https://tiing-storage.s3.ap-southeast-1.amazonaws.com/icons/status_icon/chonnhanvien.png",
                4: "https://tiing-storage.s3.ap-southeast-1.amazonaws.com/icons/status_icon/chonnhanvien.png",
                5: "https://tiing-storage.s3.ap-southeast-1.amazonaws.com/icons/status_icon/hoanthanh.png",
                6: "https://tiing-storage.s3.ap-southeast-1.amazonaws.com/icons/status_icon/huy.png"
            }
            return switcher.get(status, 'Lỗi')

        return {
            "status": status,
            "status_label": status_label_name(status),
            "time": now_timestamp,
            "content": content,
            "image": status_image(status)
        }


def change_fixed_shift_task_history_status(status: int):
    if status not in [1, 2, 3, 4]:
        raise ValueError("Invalid status when update fixed shift task")

    else:
        now = datetime.now(local)
        str_now = str(now.strftime("%H:%M:%S, %d/%m/%Y"))
        now_timestamp = now.timestamp()

        status_content = {
            1: "Lịch đặt giúp việc ca lẻ của quý khách đã được tiếp nhận vào lúc {}.".format(
                str_now),
            2: "Danh sách nhân viên nhận việc được cập nhật liên tục trong 1-3 ngày",
            3: "Nhân viên đã hoàn thành công việc vào lúc {}. Cảm ơn quý khách đã tin tưởng dịch vụ của chúng tôi.".format(
                str_now),
            4: "Công việc này đã được hủy. Cảm ơn quý khách đã tin tưởng dịch vụ của chúng tôi."
        }

        content = status_content.get(status, "Lỗi khi cập nhật thông tin trạng thái công việc")

        def status_label_name(status: int) -> str:
            switcher = {
                1: "Tiếp nhận lịch hẹn",
                2: "Chọn nhân viên giúp việc",
                3: "Hoàn thành công việc",
                4: "Đã huỷ",
            }
            return switcher.get(status, "Lỗi")

        def status_image(status: int) -> str:
            switcher = {
                1: "https://tiing-storage.s3.ap-southeast-1.amazonaws.com/icons/status_icon/new.png",
                2: "https://tiing-storage.s3.ap-southeast-1.amazonaws.com/icons/status_icon/chonnhanvien.png",
                3: "https://tiing-storage.s3.ap-southeast-1.amazonaws.com/icons/status_icon/hoanthanh.png",
                4: "https://tiing-storage.s3.ap-southeast-1.amazonaws.com/icons/status_icon/huy.png"
            }
            return switcher.get(status, 'Lỗi')

        return {
            "status": status,
            "status_label": status_label_name(status),
            "time": now_timestamp,
            "content": content,
            "image": status_image(status)
        }
