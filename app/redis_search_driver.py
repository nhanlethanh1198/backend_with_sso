import redis
import json

r = redis.StrictRedis('localhost', 6379, charset="utf-8",
                      decode_responses=True)


# search key redis

# Catching user search

def getUserSearchKey(user_id):
    key_redis = "USER_SEARCH_KEY:{}".format(user_id)
    try:
        result = r.zrevrange(key_redis, 0, -1)
        return result if result else []
    except Exception as e:
        print(e)
        return None


def setUserSearchKey(user_id, data=str):
    key_redis = "USER_SEARCH_KEY:{}".format(user_id)
    try:
        if data in getUserSearchKey(user_id):
            r.zincrby(key_redis, 1.0, data)
        else:
            r.zadd(key_redis, {data: 1.0})
        return getUserSearchKey(user_id)
    except Exception as e:
        print(e)
        return None


# catching search product by name
def getAppSearchKey():
    key_redis = "APP_SEARCH_KEY"
    try:
        result = r.zrevrange(key_redis, 0, -1)
        return result if result else []
    except Exception as e:
        print(e)
        return None


def setAppSearchKey(data):
    key_redis = "APP_SEARCH_KEY"
    try:
        if data in getAppSearchKey():
            r.zincrby(key_redis, 1.0, data)
        else:
            r.zadd(key_redis, {data: 1.0})
        return getAppSearchKey()
    except Exception as e:
        print(e)
        return None
