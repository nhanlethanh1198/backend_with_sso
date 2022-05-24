from datetime import datetime
from typing import Optional

import pytz
from sqlalchemy.orm import Session

from app.repositories import users

local = pytz.timezone('Asia/Ho_Chi_Minh')


def cal_accumulated_points(order_price: float) -> int:
    return int(order_price // 10000)


def check_stock_product():
    return 1


def check_voucher(voucher):
    x = 0
    if voucher == "KHUYENMAI50":
        x = 2
    elif voucher == "MOMOSHIP":
        x = 3

    switcher = {
        1: 0,
        2: 5000,
        3: 20000,
    }
    return switcher.get(x, 0)


def update_stock():
    return 1


def check_fee_ship(cash: float):
    if cash < 200000:
        return 25000
    else:
        return 0


def check_point_of_user(db: Session, user_id: int):
    user_point = users.get_point_of_user(db=db, user_id=user_id)
    return user_point


def update_order_status(status: int, estimated_time_delivery: Optional[datetime] = datetime.now(),
                        accumulated_point: Optional[int] = 0):
    now = datetime.now(local)
    now_timestamp = now.timestamp()
    str_now = str(now.strftime("%H:%M:%S %d/%m/%Y"))

    if status == 3 and estimated_time_delivery is None:
        raise ValueError("estimated_time_delivery is required when status is 3")

    if status == 5 and accumulated_point is None:
        raise ValueError("accumulated_point is required when status is 4")

    status_content = {
        1: "Đơn hàng của quý khách đã được tiếp nhận vào lúc {}".format(str_now),
        2: "Hoàn tất đóng gói sản phẩm vào lúc {}".format(str_now),
        3: "Thời gian giao hàng dự kiến: {}".format(str(estimated_time_delivery.strftime("%d/%m/%Y %H:%M:%S"))),
        4: "Hẹn lại ngày giao.",
        5: "Đơn hàng của quý khách đã được giao thành công, quý khách được cộng {} điểm tích lũy.".format(
            accumulated_point),
        6: "Đơn hàng đã được hủy bởi quý khách.",
        7: "Đơn hàng đã bị hủy bởi hệ thống, xin lỗi vì sự bất tiện này. Vui lòng liên hệ với chúng tôi để biết thêm chi tiết."
    }

    content = status_content.get(status, "Lỗi")

    def status_label_getter(status: int):
        status_label = {
            1: "Đơn hàng mới",
            2: "Đang xử lý",
            3: "Đang giao hàng",
            4: "Hẹn lại ngày giao",
            5: "Đã giao hàng thành công",
            6: "Đã hủy",
            7: "Đã hủy"
        }
        return status_label.get(status, "Lỗi")

    return {
        "status": status,
        "status_label": status_label_getter(status),
        "time": now_timestamp,
        "content": content
    }
