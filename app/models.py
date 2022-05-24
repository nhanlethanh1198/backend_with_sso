from datetime import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float, Text, JSON, ARRAY
from sqlalchemy.orm import relationship

from app.database import Base


# 1.User

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), nullable=True)
    dob = Column(DateTime, nullable=True)
    fullname = Column(String(100), nullable=True)
    phone = Column(String(10), unique=True, index=True)
    avatar = Column(String(100), nullable=True)
    address = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    accumulated_points = Column(Integer, default=0)
    rank = Column(String(100), nullable=True, default="Đồng")
    medal_link = Column(String(100), nullable=True,
                        default="https://tiing-storage.s3.ap-southeast-1.amazonaws.com/icons/bronze-medal.png")
    hashed_password = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

    tasks = relationship("Task", back_populates="user")
    favorites = relationship("FavoriteStaffOfUser", back_populates="user")
    devices = relationship("UserDevices", back_populates="user")
    user_favorite = relationship("UserFavorite", back_populates="user")


class FavoriteStaffOfUser(Base):
    __tablename__ = "favorite_staffs_of_user"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    staff_id = Column(Integer, ForeignKey("staffs.id"))
    is_favorite = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)
    user = relationship("User", back_populates="favorites")
    staff_is_favorite = relationship("Staff", back_populates="favorites")


# 2.Category
class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    slug = Column(String, nullable=False)
    image = Column(String, nullable=False)
    parent_id = Column(Integer, nullable=True, default=None)
    has_child = Column(Boolean, nullable=True, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


# 3.Product
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, index=True, unique=True)
    name = Column(String)
    slug = Column(String)
    avatar_img = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id"))
    price = Column(Float)
    price_sale = Column(Float, nullable=True, default=None)
    unit = Column(String)
    weight = Column(Integer)
    stock = Column(Integer)
    status = Column(Integer)
    is_active = Column(Boolean, default=True)
    image_list = Column(JSON, nullable=True, default=None)
    day_to_shipping = Column(String, nullable=True, default=None)
    description = Column(Text, nullable=True, default=None)
    note = Column(Text, nullable=True, default=None)
    tag = Column(String, nullable=True, default=None)
    type_product = Column(String, nullable=True, default=None)  # loại sản phẩm
    brand = Column(String, nullable=True, default=None)
    made_in = Column(String, nullable=True, default=None)
    made_by = Column(String, nullable=True, default=None)
    guide = Column(Text, nullable=True, default=None)  # hướng dẫn
    preserve = Column(Text, nullable=True, default=None)  # bảo quản
    location = Column(Integer, nullable=True, default=None)  # địa chỉ cửa hàng bán sản phẩm này
    total_rate = Column(Integer, nullable=True, default=0)
    comment = Column(JSON, nullable=True, default=None)  # bình luận
    belong_to_store = Column(Integer, ForeignKey("stores.id"), nullable=True, default=None)
    sale_count = Column(Integer, nullable=True, default=0)  # Đã bán
    vote_count = Column(Integer, nullable=True, default=0)  # Số lượt vote
    vote_average_score = Column(Float, nullable=True, default=0.0)  # Vote trung bình
    vote_one_star_count = Column(Integer, nullable=True, default=0)
    vote_two_star_count = Column(Integer, nullable=True, default=0)
    vote_three_star_count = Column(Integer, nullable=True, default=0)
    vote_four_star_count = Column(Integer, nullable=True, default=0)
    vote_five_star_count = Column(Integer, nullable=True, default=0)
    is_show_on_homepage = Column(Boolean, default=False)
    is_show_on_store = Column(Boolean, default=False)
    is_show_on_combo = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())
    product_user_vote = relationship(
        "ProductUserVote", back_populates="product")

    store = relationship("Store", back_populates="products")

    product_in_combo = relationship('ComboProduct', back_populates='product')
    user_favorite = relationship("UserFavorite", back_populates="product")


# 3.1. Product User Vote


class ProductUserVote(Base):
    __tablename__ = "product_user_vote"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    comment = Column(Text, nullable=True, default=None)
    vote_score = Column(Integer, nullable=True, default=0)
    tags = Column(ARRAY(Text), nullable=True, default=None)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    product = relationship("Product", back_populates="product_user_vote")


# 4.Service


class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    extra_title = Column(String, nullable=True)
    image = Column(String)
    tag = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime)
    updated_at = Column(DateTime)


# 5.Promotion
class Promotion(Base):
    __tablename__ = "promotions"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String)
    image = Column(String)
    title = Column(String)
    time_to = Column(DateTime)
    time_from = Column(DateTime)
    detail = Column(String, nullable=True)
    rule = Column(String, nullable=True)
    promotion_type = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())


# 6.Staff


class Staff(Base):
    __tablename__ = "staffs"
    id = Column(Integer, primary_key=True, index=True)
    role = Column(String, default="staff")
    fullname = Column(String, unique=True)
    dob = Column(DateTime)
    gender = Column(String, default='male')
    age = Column(Integer, default=0)
    province_code = Column(Integer, ForeignKey("location_provinces.code"), nullable=False)
    district_code = Column(Integer, ForeignKey("location_districts.code"), nullable=False)
    address = Column(String)
    email = Column(String)
    phone = Column(String)
    hash_password = Column(String)
    id_card = Column(String)
    avatar_img = Column(String)
    id_card_img_1 = Column(String)
    id_card_img_2 = Column(String)
    join_from_date = Column(DateTime)
    is_active = Column(Boolean, default=True)
    status = Column(Integer)
    working_count = Column(Integer, default=0)
    vote_count = Column(Integer, default=0)
    skill_score_count = Column(Integer, default=0)
    skill_average_score = Column(Float, default=0)
    attitude_score_count = Column(Integer, default=0)
    attitude_average_score = Column(Float, default=0)
    contentment_score_count = Column(Integer, default=0)
    contentment_average_score = Column(Float, default=0)
    vote_average_score = Column(Float, default=0)
    vote_one_star_count = Column(Integer, default=0)
    vote_two_star_count = Column(Integer, default=0)
    vote_three_star_count = Column(Integer, default=0)
    vote_four_star_count = Column(Integer, default=0)
    vote_five_star_count = Column(Integer, default=0)

    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    star = relationship("StarStaff", back_populates="staff")
    staff_location = relationship("StaffLocation", back_populates="location")
    tasks = relationship("Task", back_populates="staff")
    favorites = relationship("FavoriteStaffOfUser", back_populates="staff_is_favorite")
    devices = relationship("StaffDevices", back_populates="staff")
    banned_by_user = relationship("StaffBannedByUser", back_populates="staff")

    # one-to-one
    item_store = relationship("Store", back_populates="item_staff", uselist=False)


class StaffLocation(Base):
    __tablename__ = 'staff_location'
    id = Column(Integer, primary_key=True, index=True)
    staff_id = Column(Integer, ForeignKey("staffs.id"), nullable=False)
    type_location = Column(String, nullable=False)
    title_location = Column(String, nullable=False)
    address = Column(String, nullable=True)
    district = Column(String, nullable=True)
    province = Column(String, nullable=True)
    country = Column(String, nullable=False, default="Vietnam")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())
    location = relationship("Staff", back_populates="staff_location")


class StarStaff(Base):
    __tablename__ = "star_staffs"
    id = Column(Integer, primary_key=True, index=True)
    staff_id = Column(Integer, ForeignKey("staffs.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    vote_score = Column(Integer, nullable=False, default=0)
    comment = Column(Text, nullable=True, default=None)
    tags = Column(ARRAY(Text), nullable=True, default=None)

    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    staff = relationship("Staff", back_populates="star")


# 7.Task
class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    type_task = Column(String)
    address = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    fullname = Column(String)
    phone = Column(String)
    start_time = Column(DateTime, nullable=True, default=None)
    end_time = Column(DateTime, nullable=True, default=None)
    staff_id = Column(Integer, ForeignKey('staffs.id'), default=None)
    total_price = Column(Float)
    is_choice_staff_favorite = Column(Boolean, default=False)
    fee_tool = Column(Float, nullable=True, default=None)
    status = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

    note = Column(String, nullable=True, default=None)
    voucher = Column(String, nullable=True, default=None)
    discount = Column(Float, nullable=True, default=0)
    payment_method = Column(String, nullable=True, default="cash")
    has_tool = Column(Boolean, default=False)
    packaging = Column(String, nullable=True, default=None)
    start_date = Column(DateTime, nullable=True, default=None)
    end_date = Column(DateTime, nullable=True, default=None)
    schedule = Column(ARRAY(DateTime), nullable=True, default=None)
    task_id = Column(String, nullable=True, default="T")
    status_history = Column(JSON, nullable=True, default=[])
    user_cancel_task_reason = Column(String, nullable=True, default=None)

    user = relationship("User", back_populates="tasks")
    staff = relationship("Staff", back_populates="tasks")

    # one to many
    info_schedules = relationship("TaskSchedule", back_populates="info_task")


class TaskOfStaff(Base):
    __tablename__ = "task_of_staff"
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    type_task = Column(String, nullable=True)
    task_status = Column(Integer, default=1)
    staff_id = Column(Integer, ForeignKey("staffs.id"))
    staff_accept_time = Column(DateTime, nullable=True)
    staff_start_time = Column(DateTime, nullable=True)
    staff_finish_time = Column(DateTime, nullable=True)
    staff_status = Column(Integer, default=1)
    task_start_time = Column(DateTime, nullable=True)
    task_end_time = Column(DateTime, nullable=True)


# 8. Order


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String, nullable=True, default='OD000000')
    fullname = Column(String)
    phone = Column(String)
    address_delivery = Column(String)
    count_product = Column(Integer)
    order_type = Column(String, nullable=True, default=None)
    shipper = Column(String, nullable=True, default=None)
    start_delivery = Column(DateTime, nullable=True, default=None)
    end_delivery = Column(DateTime, nullable=True, default=None)
    voucher = Column(String, nullable=True, default=None)
    total_money = Column(Float)
    total_money_sale = Column(Float)
    product_money = Column(Float)
    ship_fee = Column(Float)
    status = Column(Integer)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())
    user_id = Column(Integer)
    note = Column(Text, nullable=True)
    method_payment = Column(String)
    status_history = Column(JSON, nullable=True, default=[])
    accumulated_point = Column(Integer, default=0)
    cancel_reason = Column(String, nullable=True)

    # detail_order = relationship("OrderDetail", back_populates="order_id")


class OrderDetail(Base):
    __tablename__ = "order_details"
    id = Column(Integer, primary_key=True, index=True)
    is_combo = Column(Boolean, default=False)
    code = Column(String)
    name = Column(String)
    image = Column(String)
    price = Column(String)
    price_sale = Column(Float)
    weight = Column(Float)
    unit = Column(String)
    quantity = Column(Integer)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())
    order_id = Column(Integer, ForeignKey('orders.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    # order = relationship("Order", back_populates="detail_order")


# 9.location
class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    title_location = Column(String)
    address = Column(String)
    district = Column(String)
    city = Column(String)
    country = Column(String)
    type_location = Column(String)
    is_active = Column(String, nullable=True, default=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())
    fullname = Column(String, nullable=True)
    phone = Column(String, nullable=True)


# 10.Combo

class Combo(Base):
    __tablename__ = "combos"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String)
    name = Column(String)
    detail = Column(String)
    is_active = Column(Boolean)
    image = Column(String)
    total_money = Column(Float)
    total_money_sale = Column(Float)
    recommend_price = Column(Float)
    f_location = Column(Integer, nullable=True)
    description = Column(String)
    note = Column(String)
    tag = Column(String)
    brand = Column(String)
    guide = Column(String)
    preserve = Column(String)
    made_in = Column(String)
    made_by = Column(String)
    day_to_shipping = Column(String)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())
    vote_count_updated_at = Column(DateTime, default=datetime.now())
    vote_count = Column(Integer, default=0)
    vote_average_score = Column(Float, default=0.0)
    vote_one_star_count = Column(Integer, default=0)
    vote_two_star_count = Column(Integer, default=0)
    vote_three_star_count = Column(Integer, default=0)
    vote_four_star_count = Column(Integer, default=0)
    vote_five_star_count = Column(Integer, default=0)
    sale_count = Column(Integer, default=0)

    products_combo = relationship("ComboProduct", back_populates="combo")
    votes = relationship("ComboVote", back_populates="combo")
    user_favorite = relationship("UserFavorite", back_populates="combo")


class ComboProduct(Base):
    __tablename__ = "product_of_combo"
    id = Column(Integer, primary_key=True, index=True)
    combo_id = Column(Integer, ForeignKey("combos.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    count = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

    combo = relationship("Combo", back_populates="products_combo")
    product = relationship("Product", back_populates="product_in_combo")


class ComboVote(Base):
    __tablename__ = "combo_user_votes"
    id = Column(Integer, primary_key=True, index=True)
    combo_id = Column(Integer, ForeignKey("combos.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    vote_score = Column(Integer)
    comment = Column(String, default=None)
    tags = Column(ARRAY(Text), nullable=True, default=None)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

    combo = relationship("Combo", back_populates="votes")


# 11 banner


class Banner(Base):
    __tablename__ = "banners"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    image = Column(String)
    category_id = Column(Integer)
    is_active = Column(Boolean)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


# 12 store


class Store(Base):
    __tablename__ = "stores"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone = Column(String)
    email = Column(String, nullable=True, default=None)
    address = Column(String)
    district_code = Column(Integer)
    province_code = Column(Integer)
    full_address = Column(String)
    avatar = Column(String, nullable=True, default=None)
    description = Column(String, nullable=True, default=None)
    product_sale_count = Column(Integer, nullable=True, default='0')
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())
    products = relationship("Product", back_populates="store")
    user_favorite = relationship("UserFavorite", back_populates="store")

    # one-to-one
    staff_id = Column(Integer, ForeignKey('staffs.id'))
    item_staff = relationship("Staff", back_populates="item_store")


# 13 version


class Version(Base):
    __tablename__ = "versions"
    id = Column(Integer, primary_key=True, index=True)
    ios = Column(String)
    android = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class LocationProvince(Base):
    __tablename__ = 'location_provinces'
    code = Column(Integer, primary_key=True)
    name = Column(String)
    name_en = Column(String)
    fullname = Column(String)
    fullname_en = Column(String)
    code_name = Column(String)
    districts = relationship("LocationDistrict", back_populates="province")


class LocationDistrict(Base):
    __tablename__ = 'location_districts'
    code = Column(Integer, primary_key=True)
    name = Column(String)
    name_en = Column(String)
    fullname = Column(String)
    fullname_en = Column(String)
    code_name = Column(String)
    province_code = Column(Integer, ForeignKey('location_provinces.code'))
    province = relationship("LocationProvince", back_populates="districts")


# Notification

class SystemNotification(Base):
    __tablename__ = 'system_notification'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, default=None)
    message = Column(String, nullable=False, default=None)
    image = Column(String, nullable=True, default=None)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    exp_at = Column(DateTime, nullable=False)
    notification_type = Column(String, nullable=False)
    priority = Column(String, default=None, nullable=False)
    staff_id = Column(Integer, ForeignKey('staffs.id'))


class UserAndStaffNotification(Base):
    __tablename__ = 'user_and_staff_notification'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, default=None)
    message = Column(String, nullable=False, default=None)
    image = Column(String, nullable=True, default=None)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    exp_at = Column(DateTime, nullable=False)
    notification_type = Column(String, nullable=False)
    priority = Column(String, default=None, nullable=False)
    staff_id = Column(Integer, ForeignKey('staffs.id'))


class UserDevices(Base):
    __tablename__ = 'user_devices'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    device_info = Column(String, nullable=True, default=None)
    is_active = Column(Boolean, nullable=True, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now())
    FCM_token = Column(String, nullable=False, default=None)

    user = relationship("User", back_populates="devices")


class StaffDevices(Base):
    __tablename__ = 'staff_devices'
    id = Column(Integer, primary_key=True, index=True)
    staff_id = Column(Integer, ForeignKey('staffs.id'))
    device_info = Column(String, nullable=False, default=None)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now())
    FCM_token = Column(String, nullable=True, default=None)

    staff = relationship("Staff", back_populates="devices")


class StaffBannedByUser(Base):
    __tablename__ = "staff_banned_by_user"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    staff_id = Column(Integer, ForeignKey('staffs.id'))
    created_at = Column(DateTime, nullable=False, default=datetime.now())

    staff = relationship("Staff", back_populates="banned_by_user")


class UserFavorite(Base):
    __tablename__ = "user_favorites"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    combo_id = Column(Integer, ForeignKey('combos.id'))
    store_id = Column(Integer, ForeignKey('stores.id'))
    created_at = Column(DateTime, nullable=False, default=datetime.now())

    user = relationship("User", back_populates="user_favorite")
    product = relationship("Product", back_populates="user_favorite")
    combo = relationship("Combo", back_populates="user_favorite")
    store = relationship("Store", back_populates="user_favorite")


class TaskSchedule(Base):
    __tablename__ = "task_schedules"
    id = Column(Integer, primary_key=True, index=True)
    f_user_id = Column(Integer, ForeignKey('users.id'))

    f_task_id = Column(Integer, ForeignKey('tasks.id'))
    task_id = Column(String, nullable=False)
    type_task = Column(String, nullable=False)
    schedule_status = Column(Integer, nullable=False)
    time_from = Column(DateTime, nullable=False)
    time_to = Column(DateTime, nullable=False)
    note = Column(Text, nullable=True, default=None)
    cancel_reason = Column(Text, nullable=True, default=None)
    comment = Column(Text, nullable=True, default=None)
    schedule_history = Column(JSON, nullable=True, default=[])
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now())

    f_staff_id = Column(Integer, ForeignKey('staffs.id'))
    f_user_id = Column(Integer, ForeignKey('users.id'))

    f_task_id = Column(Integer, ForeignKey('tasks.id'))
    info_task = relationship("Task", back_populates="info_schedules")
