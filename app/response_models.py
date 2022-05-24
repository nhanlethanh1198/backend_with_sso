from datetime import datetime
from typing import List, Optional

from pydantic.main import BaseModel


class UserInfo(BaseModel):
    id: int
    fullname: Optional[str]
    dob = datetime
    email: Optional[str]
    phone: str
    avatar: Optional[str]
    address: Optional[str]
    is_active: bool
    accumulated_points: int
    rank: str
    medal_link: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class UserInfoResponse(BaseModel):
    detail: str
    data: Optional[UserInfo]


class UserPoint(BaseModel):
    detail: str
    message: str
    notice: str
    current_rank: str
    current_accumulated_points: int

    class Config:
        orm_mode = True


class BannedStaffByUserResponse(BaseModel):
    detail: str


class StatusHistory(BaseModel):
    status: int
    status_label: Optional[str]
    time: Optional[datetime]
    content: Optional[str]
    image: Optional[str]

    class Config:
        orm_mode = True


class FavoriteStaffResponse(BaseModel):
    id: int
    user_id: int
    staff_id: int
    is_favorite: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ProductVoteList(BaseModel):
    id: int
    fullname: str
    address: str
    vote_score: int
    comment: str
    tags: List[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "code": "111111",
                "fullname": "user fullname",
                "address": "street 123",
                "name": "product name",
                "vote_score": 5.0,
                "comment": "comment",
                "tags": ["tag1", "tag2"],
                "created_at": "2020-07-07T13:35:51.661695",
                "updated_at": "2020-07-07T13:35:51.661695"
            }
        }


class ProductVoteInfo(BaseModel):
    id: int
    code: str
    name: str
    vote_count: int
    vote_average_score: float
    vote_five_star_count: int
    vote_four_star_count: int
    vote_three_star_count: int
    vote_two_star_count: int
    vote_one_star_count: int

    class Config:
        schemas_extra = {
            "example": {
                "id": 1,
                "vote_count": 1,
                "vote_average_score": 5.0,
                "vote_five_star_count": 1,
                "vote_four_star_count": 0,
                "vote_three_star_count": 0,
                "vote_two_star_count": 0,
                "vote_one_star_count": 0
            }
        }


class ProductVote(BaseModel):
    product: Optional[ProductVoteInfo] = None
    vote_list: Optional[List[ProductVoteList]] = []

    class Config:
        orm_mode = True


class ProductInfo(BaseModel):
    id: int
    code: str
    name: str
    avatar_img: Optional[str]
    status: Optional[int]
    category_id: Optional[int]
    weight: Optional[float]
    unit: Optional[str]
    price: Optional[float]
    price_sale: Optional[float]
    belong_to_store: Optional[int]
    vote_count: Optional[int]
    vote_average_score: Optional[float]
    sale_count: Optional[int]

    class Config:
        orm_mode = True


class ResponseListProduct(BaseModel):
    detail: str
    prev_page: Optional[int]
    next_page: Optional[int]
    current_page: int
    total_page: int
    total_products: int
    limit: int
    data: List[ProductInfo]


class VoteInfo(BaseModel):
    id: int
    code: str
    fullname: str
    address: str
    name: str
    vote_score: int
    comment: str
    tags: List[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        schemas_extra = {
            "id": 1,
            "code": "111111",
            "fullname": "user fullname",
            "address": "street 123",
            "name": "product name",
            "vote_score": 5.0,
            "comment": "comment",
            "tags": ["tag1", "tag2"],
            "created_at": "2020-07-07T13:35:51.661695",
            "updated_at": "2020-07-07T13:35:51.661695"

        }


class VoteInfoResponse(BaseModel):
    detail: str
    data: Optional[VoteInfo] = None


class SearchModel(BaseModel):
    data: str
    app_search_hotkey: List[str]

    class Config:
        schema_extra = {
            "example": {
                "data": "",
                "app_search_hotkey": [
                    "key1",
                    "key2",
                    "key3",
                    "key4",
                    "key5",
                ],
            }
        }


class UserCheckReceivingSuccessFull(BaseModel):
    result: bool

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "result": True
            }
        }


class AddStaffVote(BaseModel):
    id: int
    staff_id: int
    user_id: int
    vote_score: int
    comment: str
    tags: List[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class StaffVoteScoreInfo(BaseModel):
    id: int
    fullname: str
    avatar_img: str
    working_count: int
    vote_count: int
    vote_average_score: float
    skill_average_score: float
    attitude_average_score: float
    contentment_average_score: float
    vote_one_star_count: int
    vote_two_star_count: int
    vote_three_star_count: int
    vote_four_star_count: int
    vote_five_star_count: int

    class Config:
        orm_mode = True
        schemas_extra = {
            'id': 1,
            'fullname': "Staff fullname",
            'working_count': 1,
            'vote_count': 1,
            'vote_average_score': 5.0,
            'skill_average_score': 10.0,
            'attitude_average_score': 10.0,
            'contentment_average_score': 10.0,
            'vote_one_star_count': 0,
            'vote_two_star_count': 0,
            'vote_three_star_count': 0,
            'vote_four_star_count': 0,
            'vote_five_star_count': 5,
        }


class ElementInVoteStaffList(BaseModel):
    id: int
    fullname: str
    vote_score: int
    comment: str
    tags: List[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        schema_extra = {
            "id": 1,
            "fullname": "user fullname",
            "vote_score": 5.0,
            "working_count": 1,
            "comment": "comment",
            "tags": ["tag1", "tag2"],
            "created_at": "2020-07-07T13:35:51.661695",
            "updated_at": "2020-07-07T13:35:51.661695"
        }


class StaffVoteInfo(StaffVoteScoreInfo):
    vote_list: List[ElementInVoteStaffList]


class StaffVoteInfoResponse(BaseModel):
    detail: str
    data: Optional[StaffVoteInfo] = None


class PromotionInfo(BaseModel):
    id: int
    code: str
    title: str
    detail: Optional[str]
    image: str
    promotion_type: str
    rule: Optional[str]
    time_from: datetime
    time_to: datetime
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class Promotion(BaseModel):
    detail: str
    data: Optional[PromotionInfo] = None

    class Config:
        orm_mode = True


class StaffInfo(BaseModel):
    id: int
    fullname: str
    phone: str
    address: str
    avatar_img: str
    join_from_date: datetime
    working_count: int
    vote_count: int
    vote_average_score: float

    class Config:
        orm_mode = True
        schema_extra = {
            "id": 1,
            "fullname": "Staff fullname",
            "address": "Ho Chi Minh",
            "avatar_img": "avatar img link...",
            "join_from_date": "2021-09-21T10:19:36.455487",
            "working_count": 10,
            "vote_count": 5,
            "vote_average_score": 5.0
        }


class UserGetStaffList(BaseModel):
    detail: str
    data: List[StaffInfo]


# Store
class StoreInfo(BaseModel):
    id: int
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    avatar: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    district_code: Optional[int] = None
    province_code: Optional[int] = None
    full_address: Optional[str] = None
    product_sale_count: int
    vote_average_score: Optional[float] = 0
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class StoreInfoResponse(BaseModel):
    detail: str
    data: StoreInfo


class ListStoreResponse(BaseModel):
    detail: str
    prev_page: Optional[int]
    next_page: Optional[int]
    total_page: Optional[int]
    limit: Optional[int]
    total_stores: Optional[int]
    data: List[StoreInfo]


class ProductInfoForStore(BaseModel):
    id: int
    code: str
    name: str
    avatar_img: str
    price: float
    price_sale: float
    weight: float
    unit: str
    vote_average_score: float
    sale_count: int

    class Config:
        orm_mode = True


class ProductListInStoreResponse(BaseModel):
    detail: str
    data: List[ProductInfoForStore]
    prev_page: Optional[int]
    next_page: Optional[int]
    current_page: Optional[int]
    total_page: Optional[int]
    limit: Optional[int]

    class Config:
        orm_mode = True


class ListStoreHavePromotion(BaseModel):
    id: int
    name: str
    phone: str
    email: Optional[str]
    avatar: Optional[str]
    address: Optional[str]
    is_active: Optional[bool]
    district: Optional[str]
    city: Optional[str]
    product_sale_count: int
    vote_average_score: Optional[float] = 0
    created_at: datetime
    updated_at: datetime

    products: Optional[List[ProductInfoForStore]]

    class Config:
        orm_mode = True


class ListStoreHavePromotionResponse(BaseModel):
    detail: str
    data: List[ListStoreHavePromotion]
    prev_page: Optional[int]
    next_page: Optional[int]
    current_page: Optional[int]
    total_page: Optional[int]
    limit: Optional[int]

    class Config:
        orm_mode = True


class ProductInCombo(BaseModel):
    id: int
    combo_id: int
    product_id: int
    count: int
    code: str
    name: str
    avatar_img: str
    weight: int
    unit: str
    price: float
    price_sale: float
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ComboInfo(BaseModel):
    id: int
    code: str
    name: str
    detail: Optional[str]
    image: Optional[str]
    is_active: bool
    total_money: float
    total_money_sale: float
    recommend_price: float
    sale_count: int
    vote_average_score: Optional[float] = 0
    description: Optional[str]
    note: Optional[str]
    tag: Optional[str]
    brand: Optional[str]
    guide: Optional[str]
    preserve: Optional[str]
    made_in: Optional[str]
    made_by: Optional[str]
    day_to_shipping: Optional[str]
    created_at: datetime
    updated_at: datetime
    products: Optional[List[ProductInCombo]]

    class Config:
        orm_mode = True


class HandleComboResponse(BaseModel):
    detail: str
    data: Optional[ComboInfo]


class ComboListResponse(BaseModel):
    detail: str
    data: List[ComboInfo]


class ComboDetail(BaseModel):
    info: Optional[ComboInfo]
    products: List[ProductInCombo]


class ComboDetailResponse(BaseModel):
    detail: str
    data: Optional[ComboDetail]


class HandleVoteResponse(BaseModel):
    detail: str

    class Config:
        orm_mode = True


class VoteInfoByVoteId(BaseModel):
    id: int
    fullname: str
    address: str
    vote_score: int
    comment: Optional[str]
    tags: Optional[List[str]]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class VoteInfoByVoteIdResponse(BaseModel):
    detail: str
    data: Optional[VoteInfoByVoteId]


class VoteListInCombo(BaseModel):
    id: int
    name: str
    vote_count: int = 0
    vote_average_score: float = 0
    vote_one_star_count: int = 0
    vote_two_star_count: int = 0
    vote_three_star_count: int = 0
    vote_four_star_count: int = 0
    vote_five_star_count: int = 0
    vote_list: Optional[List[VoteInfoByVoteId]]

    class Config:
        orm_mode = True


class VoteListInComboResponse(BaseModel):
    detail: str
    data: Optional[VoteListInCombo]


class FavoriteStaffListResponse(BaseModel):
    detail: str
    data: List[StaffInfo]
    count: int
    prev_page: Optional[int]
    next_page: Optional[int]
    current_page: int
    total_page: int
    limit: int


class TaskInfo(BaseModel):
    id: int
    task_id: str
    type_task: str
    user_id: int
    fullname: Optional[str]
    phone: str
    address: str
    is_choice_staff_favorite: bool
    has_tool: bool
    fee_tool: Optional[float] = 0.0
    voucher: Optional[str]
    discount: Optional[float] = 0.0
    total_price: float
    payment_method: str
    note: Optional[str]
    packaging: Optional[str]
    is_active: bool
    status: int
    status_history: Optional[List[StatusHistory]]
    staff_id: Optional[int]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    start_time: datetime
    end_time: datetime
    schedule: Optional[List[datetime]]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    status_vi: Optional[str] = None

    class Config:
        orm_mode = True


class CreateOddShiftBase(BaseModel):
    id: int
    task_id: str
    type_task: str
    user_id: int
    fullname: Optional[str]
    phone: Optional[str]
    address: str
    is_choice_staff_favorite: bool
    has_tool: bool
    fee_tool: Optional[float] = 0.0
    voucher: Optional[str]
    discount: Optional[float] = 0.0
    total_price: float
    payment_method: str
    note: Optional[str]
    is_active: bool
    status: int
    status_history: Optional[List[StatusHistory]]
    staff_id: Optional[int]
    start_time: datetime
    end_time: datetime
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class CreateOddShiftResponse(BaseModel):
    detail: str
    data: Optional[CreateOddShiftBase]


class CreateFixedShiftResponse(BaseModel):
    detail: str
    data: Optional[TaskInfo]


class UserGetListTaskResponse(BaseModel):
    detail: str
    data: List[TaskInfo]
    total_tasks: int
    limit: int
    current_page: int
    prev_page: Optional[int]
    next_page: Optional[int]
    current_page: int


class CalculateOddShiftFeeResponse(BaseModel):
    hours: Optional[float] = 0
    fee_task: Optional[float] = 0
    fee_tool: Optional[float] = 0
    discount_price: Optional[float] = 0
    total_price: Optional[float] = 0
    price_per_hour: Optional[float] = 0

    class Config:
        orm_mode = True


class CalculateFixedShiftFeeResponse(BaseModel):
    day_count: Optional[int] = 0
    hours_per_day: Optional[float] = 0
    total_day: Optional[int] = 0
    fee_task: Optional[float] = 0
    fee_tool: Optional[float] = 0
    discount_price: Optional[float] = 0
    total_price: Optional[float] = 0
    price_per_hour: Optional[float] = 0


    class Config:
        orm_mode = True


class SystemNotification(BaseModel):
    id: int
    title: str
    message: Optional[str]
    image: Optional[str]
    created_at: datetime
    exp_at: Optional[datetime]
    notification_type: Optional[str]
    priority: Optional[str]

    class Config:
        orm_mode = True


class SystemNotificationResponse(BaseModel):
    detail: str
    data: Optional[SystemNotification]


class SystemNotificationListResponse(BaseModel):
    detail: str
    data: List[SystemNotification]
    total_notifications: int
    limit: int
    prev_page: Optional[int]
    next_page: Optional[int]
    current_page: int
    total_page: int


# Order
class OrderDetailItem(BaseModel):
    id: int
    code: str
    name: str
    quantity: int
    image: str
    price: float
    price_sale: float
    weight: float
    unit: str
    created_at: datetime
    updated_at: datetime
    order_id: int
    user_id: int

    class Config:
        orm_mode = True


class OrderDetail(BaseModel):
    id: int
    order_id: str
    user_id: int
    fullname: str
    phone: str
    address_delivery: str
    status: int
    status_history: Optional[List[StatusHistory]]
    count_product: int
    product_money: float
    total_money: float
    total_money_sale: float
    method_payment: Optional[str]
    order_type: Optional[str]
    note: Optional[str]
    voucher: Optional[str]
    ship_fee: float
    shipper: Optional[str]
    accumulated_point: Optional[int]
    start_delivery: Optional[datetime]
    end_delivery: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    order_details: Optional[List[OrderDetailItem]] = []
    status_vi: Optional[str] = None

    class Config:
        orm_mode = True


class UserGetOrdersResponse(BaseModel):
    detail: str
    data: List[OrderDetail]
    prev_page: Optional[int]
    next_page: Optional[int]
    current_page: Optional[int]
    total_page: Optional[int]
    limit: Optional[int]
    total_orders: Optional[int]


class CancelOrder(BaseModel):
    detail: str
    message: str
    reason: Optional[str]
    data: Optional[OrderDetail] = None

    class Config:
        orm_mode = True


class UserInfoLogin(BaseModel):
    user_id: int
    fullname: Optional[str]
    phone: str
    email: Optional[str]
    address: Optional[str]
    title_address: Optional[str]
    location_id: Optional[int]

    class Config:
        orm_mode = True


class UserLoginInfoResponse(BaseModel):
    detail: str
    access_token: str
    token_type: str
    is_update_user_info: bool
    user_info: UserInfoLogin

    class Config:
        orm_mode = True


class UserUpdateAvatarResponse(BaseModel):
    detail: str
    message: str
    avatar: str


class UserFavorite(BaseModel):
    id: int
    user_id: int
    product_id: Optional[int]
    combo_id: Optional[int]
    store_id: Optional[int]
    created_at: datetime

    class Config:
        orm_mode = True


class FavoriteList(BaseModel):
    products: List[ProductInfo]
    combos: List[ComboInfo]
    stores: List[StoreInfo]


class FavoriteListResponse(BaseModel):
    detail: str
    data: FavoriteList
    count: int
    current_page: int
    total_page: int
    prev_page: Optional[int]
    next_page: Optional[int]
    limit: int


class CheckUserExist(BaseModel):
    detail: str
    is_exist: bool
    message: str


class Categories(BaseModel):
    id: int
    name: str
    slug: str
    image: str
    has_child: bool
    parent_id: Optional[int]
    is_active: bool
    created_at: datetime
    updated_at: datetime


class CategoriesResponse(BaseModel):
    detail: str
    prev_page: Optional[int]
    next_page: Optional[int]
    total_page: Optional[int]
    current_page: Optional[int]
    limit: Optional[int]
    total_categories: Optional[int]
    data: List[Categories]
