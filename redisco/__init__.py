# -*- coding: utf-8 -*-
import redis
import redis.connection
from redis.sentinel import Sentinel, SentinelConnectionPool

default_connection_settings = {
    'host': '10.100.16.208',
    'port': 6379,
    'db': 0,
    # list of sentinels
    'sentinels': [('10.100.16.208', 5000), ('10.100.18.167', 5002), ('10.100.16.231', 5001)],
    'sentinel_name': 'master',
    'socket_timeout': 60,
    'retry_on_timeout': True

}
"""default settings for redis to connect"""

SENTINEL_SOCKET_TIMEOUT = 60


class Client(object):

    def __init__(self, **kwargs):
        self.connection_settings = kwargs or default_connection_settings
        self.sentinel_settings = self.connection_settings.get('sentinels', [])
        self.sentinel_name = self.connection_settings.get('sentinel_name', '')
        if self.sentinel_settings:
            self.connection_settings.pop('sentinels')
        if self.sentinel_name:
            self.connection_settings.get('sentinel_name')

    def redis(self):
        if self.sentinel_settings:
            sentinel = Sentinel(self.sentinel_settings,
                                socket_timeout=self.connection_settings.get('socket_timeout', SENTINEL_SOCKET_TIMEOUT))
            pool = SentinelConnectionPool(self.sentinel_name, sentinel,
                                          host=self.connection_settings.get('host'),
                                          db=self.connection_settings.get('db'))
        else:
            pool = redis.connection.ConnectionPool(**self.connection_settings)

        return redis.StrictRedis(connection_pool=pool)

    def update(self, d):
        self.connection_settings.update(d)


def connection_setup(**kwargs):
    global connection, client
    if client:
        client.update(kwargs)
    else:
        client = Client(**kwargs)
    connection = client.redis()


def get_client():
    global connection
    return connection


client = Client()
connection = client.redis()
default_expire_time = 600

__all__ = ['connection_setup', 'get_client']
