# -*- coding: utf-8 -*-

import os
import redis

from error.errors import InternalErrorWithRedis
from etc.config import RedisConnectionTimeout, RedisTimeout, RedisMaxConnection


class RedisClient:

    def __init__(self):
        redis_setting = dict(
            host=os.environ.get('RedisHost'),
            port=int(os.environ.get('RedisPort')),
            password=os.environ.get('RedisPwd'),
            db=int(os.environ.get('RedisDB')),
            decode_responses=True,
            socket_timeout=RedisTimeout,
            socket_connect_timeout=RedisConnectionTimeout,
            max_connections=RedisMaxConnection,
            retry_on_timeout=True,
        )

        pool = redis.ConnectionPool(**redis_setting)
        self.client = redis.StrictRedis(connection_pool=pool)

    def __executor(self, command, **kwargs):
        response = {
            "data": None,
            "code": 0
        }
        try:
            data = command(**kwargs)
            response['data'] = data
        except Exception as e:
            raise InternalErrorWithRedis(message=str(e))
        return response

    def __executor_iterable(self, command, **kwargs):
        response = {
            "data": None,
            "code": 0
        }
        try:
            data = command(kwargs['name'], *kwargs['value'])
            response['data'] = data
        except Exception as e:
            raise InternalErrorWithRedis()
        return response

    def get(self, key):
        command = self.client.get
        inputs = dict(
            name=key
        )
        return self.__executor(command, **inputs)

    def delete(self, list_of_key):
        response = {
            "data": None,
            "code": 0
        }
        try:
            data = self.client.delete(*list_of_key)
            response['data'] = data
        except Exception as e:
            raise InternalErrorWithRedis(message=str(e))
        return response

    def zadd(self, key, score, name):
        response = {
            "data": None,
            "code": 0
        }
        try:
            data = self.client.zadd(name=key, mapping={
                name: score,
            })
            response['data'] = data
        except Exception as e:
            raise InternalErrorWithRedis(message=str(e))
        return response

    def zrangbyscore(self, key, min, max):
        response = {
            "data": None,
            "code": 0
        }
        try:
            data = self.client.zrangebyscore(name=key, min=min, max=max, withscores=True)
            response['data'] = data
        except Exception as e:
            raise InternalErrorWithRedis(message=str(e))
        return response

    def zrem(self, key, list_of_value):
        command = self.client.zrem
        inputs = dict(
            name=key,
            value=list_of_value
        )
        return self.__executor_iterable(command, **inputs)

    def hmset(self, key, mapping):
        command = self.client.hmset
        inputs = dict(
            name=key,
            mapping=mapping
        )
        return self.__executor(command, **inputs)

    def set(self, key, value):
        command = self.client.set
        inputs = dict(
            name=key,
            value=value
        )
        return self.__executor(command, **inputs)

    def smembers(self, key):
        command = self.client.smembers
        inputs = dict(
            name=key
        )
        return self.__executor(command, **inputs)

    def sadd(self, key, list_of_value):
        command = self.client.sadd
        inputs = dict(
            name=key,
            value=list_of_value
        )
        return self.__executor_iterable(command, **inputs)

    def rpush(self, key, list_of_value):
        command = self.client.rpush
        inputs = dict(
            name=key,
            value=list_of_value
        )
        return self.__executor_iterable(command, **inputs)

    def blpop(self, list_of_key, timeout):
        command = self.client.blpop
        inputs = dict(
            keys=list_of_key,
            timeout=timeout
        )
        return self.__executor(command, **inputs)

    def close(self):
        try:
            if self.client is not None:
                self.client.close()
        except Exception as e:
            pass

