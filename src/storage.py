#!/usr/bin/python3

import redis
import json
import pandas


redis_host = "localhost"
redis_port = 6379
redis_password = ""
redis_client = redis.StrictRedis(host=redis_host,
                                 port=redis_port,
                                 password=redis_password,
                                 decode_responses=True)


def redis_load(redis_hash):

    if redis_client.hget("Connection", redis_hash) is not None:
        print("searching for connection in Redis")
        json_data = json.loads(redis_client.hget("Connection", redis_hash))
        data_frame=pandas.DataFrame(json_data)
        print(data_frame.transpose())
        return True

    else:
        return False


def redis_save(data, redis_hash):

    try:
        json_data = json.dumps(data)
        redis_client.hset("Connection", redis_hash, json_data)

    except Exception as e:
        print(e)
