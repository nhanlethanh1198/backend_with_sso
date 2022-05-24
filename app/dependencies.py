import jwt
import random
from datetime import datetime

from typing import List, Optional


async def validate_phone_number(phone: str):
    if len(phone) != 10:
        return False


async def random_otp(n: int):
    string = ''
    for x in range(n):
        num = random.randint(0, 9)
        string += str(num)
    return string


async def random_number(n: int):
    string = ''
    for x in range(n):
        num = random.randint(0, 9)
        string += str(num)
    return string


def get_fee_ship(money):
    if money < 150000:
        x = 3
    elif 150000 <= money < 200000:
        x = 2
    else:
        x = 1

    switcher = {
        1: 0,
        2: 10000,
        3: 20000,
    }
    return switcher.get(x, 20000)


def get_timestamp(date: datetime):
    str_date = date.strftime("%m/%d/%Y, %H:%M")
    object_date = datetime.strptime(str_date, "%m/%d/%Y, %H:%M")
    result_timestamp = object_date.timestamp()
    return result_timestamp


def generate_timestamp(year: int, month: int, day: int, hour: int, minute: int):
    date_dict = dict(year=year, month=month, day=day, hour=hour, minute=minute)
    result_timestamp = datetime(**date_dict).timestamp()
    return result_timestamp
