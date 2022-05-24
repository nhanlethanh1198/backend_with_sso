import json

import redis

r = redis.StrictRedis('localhost', 6379, charset="utf-8", decode_responses=True)

PRODUCT_SALE = 'PRODUCT_SALE'
PRODUCT_TREND = 'PRODUCT_TREND'
PRODUCT_NEWEST = 'PRODUCT_NEWEST'
PRODUCT_VOTE = 'PRODUCT_VOTE'
PRODUCT = 'PRODUCT'
PRODUCT_STOCK = 'PRODUCT_STOCK'
PRODUCT_PRICE = 'PRODUCT_PRICE'
CATEGORY_INFO = 'CATEGORY_INFO'
CATEGORY_WITH_SCORE = 'CATEGORY_WITH_SCORE'
STORE_INFO = 'STORE_INFO'

# PRODUCT DATA


async def set_product_detail(code, data):
    key_redis = PRODUCT
    try:
        formatted_data = json.dumps(data)
        return r.hset(key_redis, code, formatted_data)
    except Exception as e:
        return None


async def get_product_detail(code):
    key_redis = PRODUCT
    try:
        result = r.hget(key_redis, code)
        return json.loads(result)
    except Exception as e:
        return None


async def del_product_detail():
    key_redis = PRODUCT
    try:
        result = r.delete(key_redis)
        return result
    except Exception as e:
        return False


# PRODUCT STOCK
async def set_product_stock(code: str, stock: int):
    key_redis = PRODUCT_STOCK
    try:
        return r.hset(key_redis, code, stock)
    except Exception as e:
        return None


async def get_product_stock(code: str):
    key_redis = PRODUCT_STOCK
    try:
        result = r.hget(key_redis, code)
        return json.loads(result)
    except Exception as e:
        return None


async def decrease_product_stock(code: str, amount: int):
    key_redis = PRODUCT_STOCK
    amount = int(0 - amount)
    try:
        result = r.hincrby(key_redis, code, amount)
        return result
    except Exception as e:
        return False


async def del_product_stock():
    key_redis = PRODUCT_STOCK
    try:
        result = r.delete(key_redis)
        return result
    except Exception as e:
        return False


# PRODUCT PRICE


async def set_product_price(code: str, data):
    key_redis = PRODUCT_PRICE
    try:
        formatted_data = json.dumps(data)
        return r.hset(key_redis, code, formatted_data)
    except Exception as e:
        return None


async def get_product_price(code: str):
    key_redis = PRODUCT_PRICE
    try:
        result = r.hget(key_redis, code)
        return json.loads(result)
    except Exception as e:
        return None


async def del_product_price():
    key_redis = PRODUCT_PRICE
    try:
        result = r.delete(key_redis)
        return result
    except Exception as e:
        return False


# PRODUCT SALE


async def set_product_sale(code: str, score: int):
    key_redis = PRODUCT_SALE
    try:
        result = r.zadd(key_redis, {code: score})
        return result
    except Exception as e:
        print(e)
        return False


async def get_product_sale():
    key_redis = PRODUCT_SALE
    try:
        result = r.zrange(key_redis, 0, -1)
        return result
    except Exception as e:
        return False


async def del_product_sale():
    key_redis = PRODUCT_SALE
    try:
        result = r.delete(key_redis)
        return result
    except Exception as e:
        return False


# PRODUCT TREND


async def set_product_trend(code: str, score):
    key_redis = PRODUCT_TREND
    try:
        result = r.zadd(key_redis, {code: score})
        return result
    except Exception as e:
        return False


async def get_product_trend():
    key_redis = PRODUCT_TREND
    try:
        result = r.zrange(key_redis, 0, -1)
        return result
    except Exception as e:
        return False


async def del_product_trend():
    key_redis = PRODUCT_TREND
    try:
        result = r.delete(key_redis)
        return result
    except Exception as e:
        return False


# PRODUCT NEWEST


async def set_product_newest(code: str, score: int = 1):
    key_redis = PRODUCT_NEWEST
    try:
        result = r.zadd(key_redis, {code: score})
        return result
    except Exception as e:
        return False


async def get_product_newest():
    key_redis = PRODUCT_NEWEST
    try:
        result = r.zrange(key_redis, 0, -1)
        return result
    except Exception as e:
        return False


async def del_product_newest():
    key_redis = PRODUCT_NEWEST
    try:
        result = r.delete(key_redis)
        return result
    except Exception as e:
        return False


# PRODUCT VOTE


async def set_product_vote(code: str, score: int = 1):
    key_redis = PRODUCT_VOTE
    try:
        result = r.zadd(key_redis, {code: score})
        return result
    except Exception as e:
        return False


async def get_product_vote():
    key_redis = PRODUCT_VOTE
    try:
        result = r.zrange(key_redis, 0, -1)
        return result
    except Exception as e:
        return False


async def del_product_vote():
    key_redis = PRODUCT_VOTE
    try:
        result = r.delete(key_redis)
        return result
    except Exception as e:
        return False


# CATEGORIES
async def set_category_info(category_id: int, data: dict):
    key_redis = CATEGORY_INFO
    try:
        formatted_data = json.dumps(data)
        return r.hset(key_redis, str(category_id), formatted_data)
    except Exception as e:
        return None


async def get_category_info(category_id: int):
    key_redis = CATEGORY_INFO
    try:
        result = r.hget(key_redis, str(category_id))
        return json.loads(result)
    except Exception as e:
        return None


async def del_category_info():
    key_redis = CATEGORY_INFO
    try:
        result = r.delete(key_redis)
        return result
    except Exception as e:
        return False


# CATEGORY WITH SCORE
async def set_category_with_score(category_id: int, score: int):
    key_redis = CATEGORY_WITH_SCORE
    try:
        result = r.zadd(key_redis, {str(category_id): score})
        return result
    except Exception as e:
        return False


async def get_categories_with_score():
    key_redis = CATEGORY_WITH_SCORE
    try:
        result = r.zrange(key_redis, 0, -1)
        return result
    except Exception as e:
        return False


async def del_category_with_score():
    key_redis = CATEGORY_WITH_SCORE
    try:
        result = r.delete(key_redis)
        return result
    except Exception as e:
        return False


# CATEGORY WITH STORE


# STORE
async def set_store_info(store_id: int, data: dict):
    key_redis = STORE_INFO
    try:
        formatted_data = json.dumps(data)
        return r.hset(key_redis, str(store_id), formatted_data)
    except Exception as e:
        return None


async def get_store_info(store_id: int):
    key_redis = STORE_INFO
    try:
        result = r.hget(key_redis, str(store_id))
        return json.loads(result)
    except Exception as e:
        return None


async def del_store_info():
    key_redis = STORE_INFO
    try:
        result = r.delete(key_redis)
        return result
    except Exception as e:
        return False
