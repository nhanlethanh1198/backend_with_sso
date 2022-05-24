import enum
import math
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import redis_drivers
from app import response_models
from app.database import get_db
from app.dependencies import get_fee_ship
from app.get_current_staff import get_current_staff, CurrentStaff
from app.get_current_user import get_current_user, CurrentUser
from app.repositories import orders, users, combo, locations
from app.services import orders as order_services
from app.services.orders import check_voucher

from app.schemas import user_schemas, order_schemas
from app.backgrounds.notifications import send_notify_by_user_id

from app.constants import translate_task_status


router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    responses={404: {"description": "Not found"}},
)


@router.get("/get-list-order")
async def get_list_order(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                         current_staff: CurrentStaff = Depends(get_current_staff)):
    results = orders.get_list_order(db=db)
    return {
        "detail": "success",
        "data": results
    }


@router.post("/create-order", status_code=201, summary='Người dùng tạo order mới')
async def create_order(background_tasks: BackgroundTasks, request: order_schemas.CreateOrder, db: Session = Depends(get_db),
                       current_user: CurrentUser = Depends(get_current_user)):
    user_id = current_user.user_id
    order_items = request.items
    combo_out_of_stock = []  # Danh sach combo het hang
    out_of_stock = []  # danh sach san pham het hang
    discount_cash = 0
    discount_point = 0
    cash = 0
    total_item = 0

    task_id = "tasktest"
    created_at = "ngay test"
    data_notify = {
        "title": "Thông báo giúp việc",
        "body": 'Quý khách tạo yêu cầu giúp việc ca lẻ {} thành công vào lúc {}'.format(task_id, created_at),
        "image": "http://tiing-storage.s3.amazonaws.com/product/315870/a315870_986861"
    }
    await send_notify_by_user_id(db=db, user_id=user_id, data_notify=data_notify)

    # Danh sách mã sản phẩm dùng để check số lượng khi tạo order (số lượng bị giảm đi 10 thì cập nhật lại vào DB)
    product_code_list = []

    for item in order_items:
        # Check if combo
        if item.is_combo is True:
            # Check combo có những sản phẩm nào và có hết hàng hay ko
            # Nếu có hết hàng thì thông báo combo này đã hết hàng
            combo_code = item.code
            combo_detail = combo.get_combo_by_code(db=db, code=combo_code)

            # Check combo có tồn tại hay không?
            if combo_detail is None:
                raise HTTPException(status_code=422, detail="Combo không tồn tại")
            products_in_combo = combo_detail.get('products')

            # Check combo có những sản phẩm nào và có hết hàng hay ko
            for product in products_in_combo:
                stock = await redis_drivers.get_product_stock(code=product.get('code'))
                if stock is None:
                    combo_out_of_stock.append(combo_detail)
                else:
                    total_quantity = item.quantity * product.get('count')
                    if total_quantity > stock:
                        combo_out_of_stock.append(combo_detail)

        # Check if product
        else:
            # Check product có hết hàng hay ko

            stock = await redis_drivers.get_product_stock(code=item.code)

            if not stock:
                out_of_stock.append(item)
            else:
                total_quantity = item.quantity
                if total_quantity > stock:
                    out_of_stock.append(item)

    # return error if out of stock
    if len(combo_out_of_stock) > 0 or len(out_of_stock) > 0:
        raise HTTPException(status_code=422, detail={
            "message": "Combo hết hàng!",
            "detail": {
                "combo_out_of_stock": combo_out_of_stock,
                "out_of_stock": out_of_stock
            }
        })

    # Thực hiện tính tiền đơn hàng
    else:
        # Thực hiện thêm chi tiết vào order
        for item in order_items:
            # Check if combo
            if item.is_combo is True:
                current_combo = combo.get_combo_by_code(db=db, code=item.code)
                products_in_combo = current_combo.get('products')
                for product in products_in_combo:
                    product_code_list.append(product.get('code'))
                    product_quantity = item.quantity * product.get('count')
                    total_item += product_quantity
                    # Trừ số lượng stock của mỗi product trong combo
                    await redis_drivers.decrease_product_stock(code=product.get('code'), amount=product_quantity)

                # cash caculate for combo
                cash += current_combo.get('recommend_price') * item.quantity
            else:  # Is Product
                # check stock của product
                product_quantity = item.quantity
                await redis_drivers.decrease_product_stock(code=item.code, amount=product_quantity)
                # cash caculate for product
                product_code_list.append(item.code)
                # query product price
                current_product = await redis_drivers.get_product_price(code=item.code)
                cash += current_product.get('price_sale') * item.quantity
                total_item += product_quantity

    # Check voucher
    if request.voucher is not None:
        discount_cash = order_services.check_voucher(voucher=request.voucher)
        cash -= discount_cash

    # Check fee_ship
    ship_fee = order_services.check_fee_ship(cash=cash)
    cash_without_ship_fee = cash
    cash += ship_fee

    # Check user use point
    if request.use_point is True:
        discount_point = order_services.check_point_of_user(db=db, user_id=user_id)
        if discount_point is not None:
            cash -= (discount_point * 1000)

    # Check location_id của user
    current_location_of_user = locations.get_location_by_id(db=db, location_id=request.location_id, user_id=user_id)
    if current_location_of_user is None:
        raise HTTPException(status_code=422, detail="Địa chỉ không hợp lệ.")

    full_address = '{}, {}, {}'.format(current_location_of_user.address,
                                       current_location_of_user.district,
                                       current_location_of_user.city)

    # Cập nhật thông tin vào bảng Order

    status_history = order_services.update_order_status(status=1)

    data_create_order = {
        "fullname": current_location_of_user.fullname,
        "phone": current_location_of_user.phone,
        "address_delivery": full_address,
        "ship_fee": ship_fee,
        "product_money": cash_without_ship_fee,
        "total_money": cash,
        "total_money_sale": discount_cash,
        "count_product": total_item,
        "voucher": request.voucher,
        "status": 1,
        "status_history": [status_history],
        "user_id": user_id,
        "note": request.note,
        "method_payment": request.method_payment,
        "accumulated_point": order_services.cal_accumulated_points(cash)
    }
    new_order = orders.create_order(db=db, data=data_create_order)

    # Nếu không thì bắn lỗi không tạo được đơn hàng
    if new_order is None:
        raise HTTPException(status_code=422, detail={
            "detail": "failed to create order",
            "message": "Không thể tạo đơn hàng!"
        })
    # Nếu thêm order thành công thì nếu khách sử dụng điểm tích luỹ để trừ vào đơn hàng thì lúc này mới cập nhật điểm cho user    else:
    if request.use_point is True:
        result = users.decrease_accumulated_point(db=db, user_id=user_id, amount=discount_point | 0)
        if result is None:
            raise HTTPException(status_code=422, detail={
                "detail": "failed to decrease accumulated point",
                "message": "Không thể trừ điểm tích luỹ cho user!"
            })
    # Thực hiện thêm chi tiết order vào bảng order_detail
    new_order_id = new_order.id

    order_detail_array = []
    for item in order_items:
        if item.is_combo is True:
            current_combo = combo.get_combo_by_code(db=db, code=item.code)
            quantity_combo = item.quantity
            current_combo_data = {
                "order_id": new_order_id,
                "user_id": user_id,
                "is_combo": True,
                "code": current_combo.get('code'),
                "name": current_combo.get('name'),
                "image": current_combo.get('image'),
                "price": current_combo.get('total_money_sale'),
                "price_sale": current_combo.get('recommend_price'),
                "weight": quantity_combo,
                "unit": "combo",
                "quantity": quantity_combo,
            }
            order_detail_array.append(current_combo_data)
        else:
            code = item.code
            quantity = item.quantity
            current_product = await redis_drivers.get_product_detail(code=code)
            current_product_price = await redis_drivers.get_product_price(code=code)
            current_product_data = {
                "order_id": new_order_id,
                "user_id": user_id,
                "is_combo": False,
                "code": code,
                "name": current_product.get('name'),
                "image": current_product.get('avatar_img'),
                **current_product_price,
                "quantity": quantity,
            }
            order_detail_array.append(current_product_data)

    # Thực hiện thêm chi tiết order vào bảng order_detail
    action_add_order_detail = orders.add_order_detail(db=db, array_item=order_detail_array)

    if action_add_order_detail is True:
        return {
            "detail": "success",
            "order_id": new_order.order_id
        }
    else:
        raise HTTPException(status_code=422, detail="Có lỗi khi thêm thông tin danh sách sản phẩm của đơn hàng")


@router.put("/update-order/{order_id}")
async def update_order(order_id: str, data: order_schemas.UpdateOrder, db: Session = Depends(get_db),
                       current_staff: CurrentStaff = Depends(get_current_staff)):
    list_product = []
    products = data.products

    out_of_stock = []  # danh sach san pham het hang

    for each_product in products:

        stock = await redis_drivers.get_product_stock(each_product['code'])
        if stock is None:
            out_of_stock.append(each_product)

        else:
            k = str(each_product['weight']) + str(each_product['unit'])
            if each_product['count_product'] > stock:
                out_of_stock.append(each_product)

    if len(out_of_stock) > 0:
        return {
            "detail": "failed",
            "message": "some products in out of stock",
            "data": out_of_stock
        }

    count_product = 0  # tong san pham
    product_money = 0  # tong tien hang
    for each_product in products:
        product_money += each_product['sale_price'] * \
                         each_product['count_product']
        count_product += each_product['count_product']

    ship_fee = get_fee_ship(product_money)
    total_money = product_money + ship_fee
    current_order = orders.get_order_by_id(db=db, order_id=order_id)
    total_money_sale = total_money - check_voucher(current_order.voucher)

    user_id = current_order.user_id

    new_order = orders.update_order(
        db=db,
        order_id=order_id,
        fullname=data.fullname,
        phone=data.phone,
        address_delivery=data.address_delivery,
        ship_fee=ship_fee,
        product_money=product_money,
        total_money=total_money,
        total_money_sale=total_money_sale,
        count_product=count_product
    )
    if new_order == None:
        return {
            "detail": "failed",
            "message": "can not update order",
            "data": {}
        }
    else:
        orders.delete_order_detail(db=db, order_id=order_id)
        # TODO: update order detail

        # for each_product in products:
        #     orders.add_product_order_detail(
        #         db=db,
        #         order_id=order_id,
        #         user_id=user_id,
        #         code=each_product['code'],
        #         product_name=each_product['product_name'],
        #         product_image=each_product['product_image'],
        #         original_price=each_product['original_price'],
        #         sale_price=each_product['sale_price'],
        #         weight=each_product['weight'],
        #         unit=each_product['unit'],
        #         count=each_product['count_product']
        #     )

        return {
            "detail": "success",
            "data": {
                "order_id": order_id
            }
        }


@router.get("/get-order-by-id/{order_id}")
async def get_order_by_id(order_id: str, db: Session = Depends(get_db),
                          current_staff: CurrentStaff = Depends(get_current_staff)):
    current_order = orders.get_order_by_id(db=db, order_id=order_id)

    if not current_order:
        raise HTTPException(status_code=422, detail="Không tìm thấy đơn hàng này!")

    else:
        order_detail = orders.get_detail_order(db=db, order_id=current_order.id)
        return {
            "detail": "success",
            "order": current_order,
            "order_detail": order_detail
        }


@router.get("/user-get-order-by-id/{order_id}")
async def user_get_order_by_id(order_id: str, db: Session = Depends(get_db),
                               current_user: CurrentUser = Depends(get_current_user)):
    user_id = current_user.user_id
    current_order = orders.user_get_order_by_id(
        db=db, order_id=order_id, user_id=user_id)

    if not current_order:
        raise HTTPException(status_code=422, detail="Không tìm thấy đơn hàng này!")

    else:
        order_detail = orders.get_detail_order(db=db, order_id=current_order.id)
        return {
            "detail": "success",
            "order": current_order,
            "order_detail": order_detail
        }


@router.post("/user-cancel-order/{order_id}", description='User can cancel order with order status is "1"',
             response_model=response_models.CancelOrder)
async def cancel_order(order_id: str, request: user_schemas.UserCancelWithReason, db: Session = Depends(get_db),
                       current_user: CurrentUser = Depends(get_current_user)):
    user_id = current_user.user_id
    current_order = orders.user_get_order_by_id(
        db=db, order_id=order_id, user_id=user_id)

    if not current_order:
        raise HTTPException(status_code=422, detail="Không tìm thấy đơn hàng này!")

    else:

        if current_order.status == 6:
            raise HTTPException(status_code=422, detail="Đơn hàng đã được hủy trước đó!")

        if current_order.status in [2, 3, 4, 5, 7]:  # only cancel order when status is 1
            raise HTTPException(status_code=422, detail="Bạn không thể hủy đơn hàng này do đang được xử lý!")

        # Only cancel order when status is 1
        current_order.status = 6  # cancel order
        status_history_array = jsonable_encoder(current_order.status_history)
        status_history_array.append(order_services.update_order_status(status=6))
        current_order.status_history = status_history_array
        current_order.cancel_reason = request.reason
        db.commit()
        db.refresh(current_order)
        return {
            "detail": 'success',
            "message": 'cancel order success',
            "reason": current_order.cancel_reason,
            "data": current_order
        }


@router.get("/get-fee-ship", summary='Get fee ship')
async def get_fee_ship_func(total_money: float, voucher: Optional[str] = None, db: Session = Depends(get_db)):
    ship_fee = get_fee_ship(total_money)
    data_voucher = check_voucher(voucher)
    return {
        "detail": "success",
        "message": "Mua thêm 80.000đ để được giảm 10.000đ phí vận chuyển",
        "data": ship_fee,
        "voucher": data_voucher
    }


@router.post('/user-get-orders', summary='User get order list', response_model=response_models.UserGetOrdersResponse)
async def user_get_order(request_body: order_schemas.UserGetListOrder, db: Session = Depends(get_db),
                         current_user: CurrentUser = Depends(get_current_user)):
    user_id = current_user.user_id
    status = request_body.status
    limit = request_body.limit
    page = request_body.page
    count_order = orders.count_order_by_user_id(db=db, user_id=user_id, status=status)
    total_page = math.ceil(count_order / limit)
    skip = limit * (page - 1)
    results = orders.get_order_by_user_id(db=db, limit=limit, skip=skip, user_id=user_id, status=status)
    list_order = []
    for item in results:
        item_encode = jsonable_encoder(item)
        temp = {
            **item_encode,
            "status_vi": translate_task_status(item_encode['status'])
        }
        list_order.append(temp)

    prev_page = page - 1
    if prev_page <= 0:
        prev_page = None
    next_page = page + 1
    if next_page > total_page:
        next_page = None

    return {
        "detail": "success",
        "data": list_order,
        "prev_page": prev_page,
        'next_page': next_page,
        'current_page': page,
        'total_page': total_page,
        'limit': limit,
        'total_orders': count_order
    }


class OrderStatus(enum.IntEnum, enum.Enum):
    PENDING = 1
    PROCESSING = 2
    SHIPPING = 3
    REDELIVERY = 4
    COMPLETED = 5
    CANCELED = 6
    SYSTEM_CANCELED = 7


@router.post('/update-order-status/{order_id}', summary='Update order status', status_code=200, description="""
# Params:

## estimated_time_delivery: Thời gian dự kiến giao hàng (chỉ áp dụng với status = 3)

### status: Trạng thái đơn hàng (1: Đã tiếp nhận đơn hàng, 2: Đã đóng gói đơn hàng, 3: Đang giao hàng (kèm thời gian dự kiến), 4: Giao hàng thành công, 5: Đã hủy bởi người dùng, 6: Đã hủy bởi hệ thống)

""")
async def update_order_status(order_id: str, status: OrderStatus, estimated_time_delivery: Optional[datetime] = None,
                              db: Session = Depends(get_db),
                              current_staff: CurrentStaff = Depends(get_current_staff)):
    current_order = orders.get_order_by_id(db=db, order_id=order_id)

    if current_order is not None:
        status_history = jsonable_encoder(current_order.status_history)
        if status == 5:  # order delivered
            user_id = current_order.user_id
            current_user = users.get_user_by_id(db=db, user_id=user_id)
            if current_user is not None:
                # set Status in current_order
                current_order.status = 5
                status_history.append(order_services.update_order_status(status=status,
                                                                         accumulated_point=current_order.accumulated_point))
                current_order.status_history = status_history
                db.commit()
                db.refresh(current_order)

                # set accumulated point (Điểm tích lũy của user)
                current_user.accumulated_point += current_order.accumulated_point
                db.commit()
                db.refresh(current_user)

                return {
                    "detail": "success",
                    "message": "Update order status success",
                    "data": current_order
                }
            else:
                return {
                    "detail": "failed",
                    "message": "Cannot find user with order",
                    "data": None
                }
        else:
            if status == 3:
                status_history.append(
                    order_services.update_order_status(status=status, estimated_time_delivery=estimated_time_delivery))
            else:
                status_history.append(order_services.update_order_status(status=status))
            current_order.status_history = status_history
            current_order.status = status
            db.commit()
            db.refresh(current_order)
            return {
                "detail": "success",
                "message": "Update order status success",
                "data": current_order
            }
    else:
        return {
            "detail": "failed",
            "message": "Order not found",
            "data": None
        }


class OrderStatusHistory(enum.IntEnum, enum.Enum):
    COMPLETE = 5
    CANCELED = 6
    SYSTEM_CANCELED = 7


# User get order history
@router.get('/user-history', summary='Get order history by user', status_code=200, description="""
Người dùng lấy danh sách lịch sử đơn hàng của mình.
""")
async def order_user_history(status: Optional[OrderStatusHistory] = None, limit: Optional[int] = 20,
                             page: Optional[int] = 1, db: Session = Depends(get_db),
                             current_user: CurrentUser = Depends(get_current_user)):
    user_id = current_user.user_id
    total_orders = orders.count_order_history_by_user_id(db=db, user_id=user_id, status=status)

    total_pages = math.ceil(total_orders / limit)
    skip = limit * (page - 1)
    results = orders.get_order_history_by_user_id(db=db, user_id=user_id, status=status, limit=limit, skip=skip)

    prev_page = page - 1
    if prev_page <= 0:
        prev_page = None
    next_page = page + 1
    if next_page > total_pages:
        next_page = None

    return {
        "detail": "success",
        "data": results,
        "prev_page": prev_page,
        'next_page': next_page,
        'current_page': page,
        'total_page': total_pages,
        'limit': limit,
        'total_orders': total_orders
    }
