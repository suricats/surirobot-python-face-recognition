import os
import redis
from .thread import RedisThread


class RedisAdapter:
    last_name = "Unknown"

    def init(self):
        redis_address = os.environ.get('SURIROBOT_REDIS_ADDRESS', '127.0.0.1')
        self.conn = redis.StrictRedis(redis_address)

    def process(self, data):
        names = data[2]
        if len(names) > 0:
            name = names[0]
            if self.last_name != name:
                self.last_name = name
                thread = RedisThread(self.conn, name)
                thread.start()
